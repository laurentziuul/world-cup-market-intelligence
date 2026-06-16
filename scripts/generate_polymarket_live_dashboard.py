from **future** import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from wcmi.providers.polymarket import PolymarketProvider

ROOT = Path(**file**).resolve().parents[1]

OUTPUT_DIR = ROOT / "docs" / "polymarket-dashboard"
OUTPUT_PATH = OUTPUT_DIR / "index.html"

TREND_OUTPUTS = {
"Snapshot comparison": ROOT / "data" / "processed" / "snapshot_comparison_latest.csv",
"Probability deltas": ROOT / "data" / "processed" / "probability_deltas_latest.csv",
"Top movers": ROOT / "data" / "processed" / "top_movers_latest.csv",
"Signal summary": ROOT / "data" / "processed" / "signal_summary_latest.csv",
}

WINNER_MARKET_PATTERN = re.compile(
r"^Will (.+) win the 2026 FIFA World Cup?$",
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

def extract_team_name(market_title: str) -> str:
match = WINNER_MARKET_PATTERN.match(str(market_title).strip())

```
if not match:
    return ""

return match.group(1).strip()
```

def format_probability(value: float) -> str:
return f"{value * 100:.2f}%"

def format_number(value: float) -> str:
return f"{value:,.0f}"

def build_yes_ranking(dataframe: pd.DataFrame) -> pd.DataFrame:
if dataframe.empty:
return pd.DataFrame(columns=OUTPUT_COLUMNS)

```
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
```

def render_trend_status() -> str:
rows = []

```
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
```

def render_table_rows(ranking: pd.DataFrame) -> str:
rows = []

```
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
```

def render_html(
ranking: pd.DataFrame,
provider_rows: int,
generated_at: str,
) -> str:
top_team = "N/A"
top_probability = "N/A"

```
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
```

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

```
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
```

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

```
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
        Provider rows loaded: <strong>{provider_rows}</strong>.
        This dashboard requires live Polymarket access when regenerated.
        During testing, access worked using Proton VPN with a Moldova server.
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
```

</body>
</html>
"""

def main() -> None:
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

```
generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

print("Generating experimental Polymarket live dashboard...")
print("Fetching Polymarket provider data...")

provider = PolymarketProvider()
dataframe = provider.load()
ranking = build_yes_ranking(dataframe)

html_content = render_html(
    ranking=ranking,
    provider_rows=len(dataframe),
    generated_at=generated_at,
)

OUTPUT_PATH.write_text(html_content, encoding="utf-8")

print(f"Provider rows loaded: {len(dataframe)}")
print(f"YES ranking rows: {len(ranking)}")
print(f"Dashboard saved: {OUTPUT_PATH}")
```

if **name** == "**main**":
main()
