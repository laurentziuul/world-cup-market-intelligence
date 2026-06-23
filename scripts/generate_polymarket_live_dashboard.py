from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from wcmi.providers.polymarket import PolymarketProvider

ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = ROOT / "docs" / "polymarket-dashboard"
OUTPUT_PATH = OUTPUT_DIR / "index.html"

# Pre-processed YES ranking produced by generate_polymarket_yes_ranking.py (Step 2 of pipeline).
# The dashboard reads from this CSV when available — avoids a duplicate live API call.
YES_RANKING_PATH = ROOT / "data" / "processed" / "polymarket_worldcup_yes_ranking.csv"

TREND_OUTPUTS = {
    "Snapshot comparison": ROOT / "data" / "processed" / "snapshot_comparison_latest.csv",
    "Probability deltas": ROOT / "data" / "processed" / "probability_deltas_latest.csv",
    "Top movers": ROOT / "data" / "processed" / "top_movers_latest.csv",
    "Signal summary": ROOT / "data" / "processed" / "signal_summary_latest.csv",
}

WINNER_MARKET_PATTERN = re.compile(
    r"^Will (.+) win the 2026 FIFA World Cup\?$",
    re.IGNORECASE,
)

OUTPUT_COLUMNS = [
    "rank",
    "team",
    "yes_probability",
    "yes_probability_display",
    "market_title",
    "volume",
    "liquidity",
    "source_url",
]

# Known team name corrections for Polymarket API mojibake.
# The API has returned Unicode escape sequences that map to wrong codepoints
# (e.g. U+0102 U+00A7 instead of U+00E7 for c-cedilla in Curacao).
TEAM_NAME_CORRECTIONS: dict[str, str] = {
    "CuraĂ§ao": "Curaçao",  # literal string key
}


def normalize_team_name(name: str) -> str:
    """Fix known Polymarket API mojibake in team names."""
    return TEAM_NAME_CORRECTIONS.get(name, name)


def extract_team_name(market_title: str) -> str:
    match = WINNER_MARKET_PATTERN.match(str(market_title).strip())

    if not match:
        return ""

    return normalize_team_name(match.group(1).strip())


def format_probability(value: float) -> str:
    return f"{value * 100:.2f}%"


def format_number(value: float) -> str:
    return f"{value:,.0f}"


def load_from_ranking_csv() -> pd.DataFrame | None:
    """Read the pre-processed YES ranking CSV produced by generate_polymarket_yes_ranking.py.

    Returns a DataFrame with OUTPUT_COLUMNS, or None if the file does not exist.
    Using the CSV avoids a duplicate live API call inside the daily pipeline.
    """
    if not YES_RANKING_PATH.exists():
        return None

    try:
        df = pd.read_csv(YES_RANKING_PATH, encoding="utf-8")
    except Exception as exc:
        print(f"Warning: could not read {YES_RANKING_PATH}: {exc}")
        return None

    if df.empty:
        return None

    # Ensure required columns exist
    for col in OUTPUT_COLUMNS:
        if col not in df.columns:
            print(f"Warning: column '{col}' missing from {YES_RANKING_PATH} — falling back to live API.")
            return None

    # Apply team-name encoding corrections to both team and market_title columns
    df = df.copy()
    df["team"] = df["team"].astype(str).apply(normalize_team_name)
    # Replace known bad substrings inside market_title without destroying the full title
    def normalize_market_title(title: str) -> str:
        for bad, good in TEAM_NAME_CORRECTIONS.items():
            title = title.replace(bad, good)
        return title
    df["market_title"] = df["market_title"].astype(str).apply(normalize_market_title)

    # Ensure numeric types
    df["yes_probability"] = pd.to_numeric(df["yes_probability"], errors="coerce").fillna(0.0)
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0.0)
    df["liquidity"] = pd.to_numeric(df["liquidity"], errors="coerce").fillna(0.0)
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce").fillna(0).astype(int)

    return df[OUTPUT_COLUMNS]


def build_yes_ranking(dataframe: pd.DataFrame) -> pd.DataFrame:
    if dataframe.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    working = dataframe.copy()
    working["team"] = working["market_title"].apply(extract_team_name)

    ranking = working[
        (working["team"] != "")
        & (working["outcome"].astype(str).str.lower() == "yes")
    ].copy()

    if ranking.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    ranking["yes_probability"] = pd.to_numeric(
        ranking["price"],
        errors="coerce",
    ).fillna(0.0)

    ranking["volume"] = pd.to_numeric(
        ranking["volume"],
        errors="coerce",
    ).fillna(0.0)

    ranking["liquidity"] = pd.to_numeric(
        ranking["liquidity"],
        errors="coerce",
    ).fillna(0.0)

    ranking = ranking.sort_values(
        by=["yes_probability", "volume", "liquidity"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    ranking["rank"] = ranking.index + 1
    ranking["yes_probability_display"] = ranking["yes_probability"].apply(
        format_probability
    )

    return ranking[OUTPUT_COLUMNS]


def render_trend_status() -> str:
    rows = []

    for label, path in TREND_OUTPUTS.items():
        exists = path.exists()
        status = "available" if exists else "missing"
        css_class = "status-ok" if exists else "status-missing"

        rows.append(
            f"""
            <tr>
                <td>{html.escape(label)}</td>
                <td class="{css_class}">{status}</td>
                <td><code>{html.escape(str(path.relative_to(ROOT)))}</code></td>
            </tr>
            """
        )

    return "\n".join(rows)


def render_table_rows(ranking: pd.DataFrame) -> str:
    rows = []

    for _, row in ranking.iterrows():
        probability = float(row["yes_probability"])
        bar_width = max(0.0, min(100.0, probability * 100.0))

        team = html.escape(str(row["team"]))
        market_title = html.escape(str(row["market_title"]))
        source_url = html.escape(str(row["source_url"]))
        probability_display = html.escape(str(row["yes_probability_display"]))

        rows.append(
            f"""
            <tr>
                <td class="rank">{int(row["rank"])}</td>
                <td class="team">{team}</td>
                <td class="probability">
                    <div class="probability-value">{probability_display}</div>
                    <div class="bar">
                        <div class="bar-fill" style="width: {bar_width:.2f}%"></div>
                    </div>
                </td>
                <td>{format_number(float(row["volume"]))}</td>
                <td>{format_number(float(row["liquidity"]))}</td>
                <td>
                    <a href="{source_url}" target="_blank" rel="noopener noreferrer">
                        Polymarket
                    </a>
                </td>
                <td class="market-title">{market_title}</td>
            </tr>
            """
        )

    return "\n".join(rows)


def render_html(
    ranking: pd.DataFrame,
    provider_rows: int,
    generated_at: str,
    data_source: str = "live_api",
) -> str:
    top_team = "N/A"
    top_probability = "N/A"

    if not ranking.empty:
        top_team = str(ranking.iloc[0]["team"])
        top_probability = str(ranking.iloc[0]["yes_probability_display"])

    table_rows = render_table_rows(ranking)
    trend_status_rows = render_trend_status()

    if ranking.empty:
        table_rows = """
        <tr>
            <td colspan="7">No Polymarket YES winner markets found.</td>
        </tr>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Polymarket World Cup 2026 Live Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
        }}

        .container {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 32px 20px;
        }}

        .header {{
            margin-bottom: 24px;
        }}

        .label {{
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            background: #7c2d12;
            color: #fed7aa;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 12px;
        }}

        h1 {{
            margin: 0 0 8px 0;
            font-size: 34px;
        }}

        h2 {{
            margin: 0 0 10px 0;
            font-size: 24px;
        }}

        .subtitle {{
            color: #cbd5e1;
            max-width: 780px;
            line-height: 1.5;
        }}

        .cards {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
            margin: 28px 0;
        }}

        .card {{
            background: #111827;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 18px;
        }}

        .card-title {{
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 8px;
        }}

        .card-value {{
            font-size: 24px;
            font-weight: 800;
        }}

        .notice {{
            background: #1e293b;
            border: 1px solid #475569;
            border-radius: 14px;
            padding: 16px;
            margin: 22px 0;
            color: #cbd5e1;
            line-height: 1.5;
        }}

        .warning-notice {{
            background: #1c1408;
            border: 1px solid #d97706;
            border-radius: 14px;
            padding: 16px;
            margin: 22px 0;
            color: #fde68a;
            line-height: 1.5;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: #111827;
            border: 1px solid #334155;
            border-radius: 14px;
            overflow: hidden;
        }}

        th, td {{
            padding: 13px 12px;
            border-bottom: 1px solid #334155;
            text-align: left;
            vertical-align: middle;
            font-size: 14px;
        }}

        th {{
            background: #1e293b;
            color: #cbd5e1;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        tr:hover {{
            background: #172033;
        }}

        a {{
            color: #93c5fd;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        code {{
            color: #93c5fd;
        }}

        .rank {{
            width: 52px;
            font-weight: 700;
            color: #facc15;
        }}

        .team {{
            font-weight: 700;
            font-size: 15px;
        }}

        .probability {{
            min-width: 180px;
        }}

        .probability-value {{
            font-weight: 700;
            margin-bottom: 6px;
        }}

        .bar {{
            width: 100%;
            height: 8px;
            background: #334155;
            border-radius: 999px;
            overflow: hidden;
        }}

        .bar-fill {{
            height: 100%;
            background: #22c55e;
            border-radius: 999px;
        }}

        .market-title {{
            color: #94a3b8;
            max-width: 340px;
        }}

        .trend-section {{
            margin-top: 28px;
        }}

        .status-ok {{
            color: #86efac;
            font-weight: 700;
        }}

        .status-missing {{
            color: #fdba74;
            font-weight: 700;
        }}

        .footer {{
            margin-top: 24px;
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.5;
        }}

        @media (max-width: 900px) {{
            .cards {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}

            table {{
                display: block;
                overflow-x: auto;
            }}
        }}

        @media (max-width: 560px) {{
            .cards {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 26px;
            }}
        }}
    </style>
</head>
<body>
    <main class="container">
        <section class="header">
            <div class="label">Experimental live provider</div>
            <h1>Polymarket World Cup 2026 Live Dashboard</h1>
            <p class="subtitle">
                YES-only ranking for Polymarket markets matching:
                <strong>Will X win the 2026 FIFA World Cup?</strong>
                This page is separate from the stable manual CSV dashboard.
            </p>
        </section>

        <section class="warning-notice">
            <strong>Experimental.</strong>
            This dashboard requires live Polymarket API access each time it is regenerated.
            Data may be stale, incomplete, or unavailable if the API is unreachable.
            Probabilities, volume, and liquidity are sourced directly from Polymarket
            and may not match other data layers.
            <strong>This is not betting advice, investment advice, or a prediction engine.</strong>
            Research-only.
        </section>

        <section class="cards">
            <div class="card">
                <div class="card-title">Provider</div>
                <div class="card-value">polymarket</div>
            </div>
            <div class="card">
                <div class="card-title">Status</div>
                <div class="card-value">experimental</div>
            </div>
            <div class="card">
                <div class="card-title">Teams ranked</div>
                <div class="card-value">{len(ranking)}</div>
            </div>
            <div class="card">
                <div class="card-title">Top market</div>
                <div class="card-value">{html.escape(top_team)} {html.escape(top_probability)}</div>
            </div>
        </section>

        <section class="notice">
            Generated at <strong>{html.escape(generated_at)}</strong> UTC.
            Teams ranked: <strong>{provider_rows}</strong>.
            Data source: <strong>{html.escape(data_source)}</strong>.
        </section>

        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Team</th>
                    <th>YES probability</th>
                    <th>Volume</th>
                    <th>Liquidity</th>
                    <th>Source</th>
                    <th>Market</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>

        <section class="trend-section">
            <h2>Historical trends status</h2>
            <p class="subtitle">
                These files are generated only when the Polymarket workflow is run with
                <code>--include-trends</code>. Missing files are normal if historical
                trends have not been generated yet.
            </p>

            <table>
                <thead>
                    <tr>
                        <th>Trend output</th>
                        <th>Status</th>
                        <th>Path</th>
                    </tr>
                </thead>
                <tbody>
                    {trend_status_rows}
                </tbody>
            </table>
        </section>

        <section class="footer">
            <p>
                Stable dashboard:
                <a href="../dashboard/">manual_csv dashboard</a>.
                Intelligence dashboard:
                <a href="../trends-dashboard/">Historical trends</a>.
            </p>
            <p>
                Powered by <strong>Mayior Capital</strong>.
            </p>
            <p>
                This page is generated by
                <code>scripts/generate_polymarket_live_dashboard.py</code>.
                It is experimental and should not be treated as betting or investment advice.
            </p>
        </section>
    </main>
</body>
</html>
"""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    print("Generating experimental Polymarket live dashboard...")

    # Prefer the pre-processed YES ranking CSV (produced by generate_polymarket_yes_ranking.py
    # earlier in the same pipeline run) over a duplicate live API call.
    ranking = load_from_ranking_csv()
    data_source: str

    if ranking is not None:
        data_source = f"ranking_csv ({YES_RANKING_PATH.name})"
        print(f"Using cached ranking CSV: {YES_RANKING_PATH}")
    else:
        print("Ranking CSV not found — fetching from live Polymarket API...")
        provider = PolymarketProvider()
        dataframe = provider.load()
        ranking = build_yes_ranking(dataframe)
        data_source = "live_api (polymarket)"
        print(f"Provider rows loaded: {len(dataframe)}")

    html_content = render_html(
        ranking=ranking,
        provider_rows=len(ranking),
        generated_at=generated_at,
        data_source=data_source,
    )

    OUTPUT_PATH.write_text(html_content, encoding="utf-8")

    print(f"YES ranking rows: {len(ranking)}")
    print(f"Data source: {data_source}")
    print(f"Dashboard saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
