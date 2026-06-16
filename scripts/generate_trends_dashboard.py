from __future__ import annotations

import html
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = ROOT / "docs" / "trends-dashboard"
OUTPUT_PATH = OUTPUT_DIR / "index.html"

TOP_MOVERS_PATH = ROOT / "data" / "processed" / "top_movers_latest.csv"
SIGNAL_SUMMARY_PATH = ROOT / "data" / "processed" / "signal_summary_latest.csv"
PROBABILITY_DELTAS_PATH = ROOT / "data" / "processed" / "probability_deltas_latest.csv"


def read_optional_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def format_value(value: object) -> str:
    if pd.isna(value):
        return ""

    return str(value)


def render_file_status() -> str:
    files = {
        "Probability deltas": PROBABILITY_DELTAS_PATH,
        "Top movers": TOP_MOVERS_PATH,
        "Signal summary": SIGNAL_SUMMARY_PATH,
    }

    rows = []

    for label, path in files.items():
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


def render_top_movers(top_movers: pd.DataFrame) -> str:
    if top_movers.empty:
        return """
        <tr>
            <td colspan="8">No top movers output found yet. Run the historical trends workflow first.</td>
        </tr>
        """

    columns = [
        "category",
        "rank",
        "team",
        "outcome",
        "probability_change_display",
        "direction",
        "current_liquidity",
        "source_url",
    ]

    for column in columns:
        if column not in top_movers.columns:
            top_movers[column] = ""

    rows = []

    for _, row in top_movers.head(40).iterrows():
        source_url = html.escape(format_value(row["source_url"]))
        source_cell = ""

        if source_url:
            source_cell = (
                f'<a href="{source_url}" target="_blank" '
                f'rel="noopener noreferrer">Source</a>'
            )

        rows.append(
            f"""
            <tr>
                <td>{html.escape(format_value(row["category"]))}</td>
                <td>{html.escape(format_value(row["rank"]))}</td>
                <td class="team">{html.escape(format_value(row["team"]))}</td>
                <td>{html.escape(format_value(row["outcome"]))}</td>
                <td class="change">{html.escape(format_value(row["probability_change_display"]))}</td>
                <td>{html.escape(format_value(row["direction"]))}</td>
                <td>{html.escape(format_value(row["current_liquidity"]))}</td>
                <td>{source_cell}</td>
            </tr>
            """
        )

    return "\n".join(rows)


def render_signal_summary(signal_summary: pd.DataFrame) -> str:
    if signal_summary.empty:
        return """
        <tr>
            <td colspan="8">No signal summary output found yet. Run the historical trends workflow first.</td>
        </tr>
        """

    columns = [
        "team",
        "outcome",
        "probability_change_display",
        "signal_label",
        "signal_strength",
        "liquidity_label",
        "signal_reason",
        "source_url",
    ]

    for column in columns:
        if column not in signal_summary.columns:
            signal_summary[column] = ""

    rows = []

    filtered = signal_summary[
        signal_summary["signal_label"].astype(str) != "flat_no_signal"
    ].copy()

    if filtered.empty:
        filtered = signal_summary.copy()

    for _, row in filtered.head(40).iterrows():
        source_url = html.escape(format_value(row["source_url"]))
        source_cell = ""

        if source_url:
            source_cell = (
                f'<a href="{source_url}" target="_blank" '
                f'rel="noopener noreferrer">Source</a>'
            )

        rows.append(
            f"""
            <tr>
                <td class="team">{html.escape(format_value(row["team"]))}</td>
                <td>{html.escape(format_value(row["outcome"]))}</td>
                <td class="change">{html.escape(format_value(row["probability_change_display"]))}</td>
                <td>{html.escape(format_value(row["signal_label"]))}</td>
                <td>{html.escape(format_value(row["signal_strength"]))}</td>
                <td>{html.escape(format_value(row["liquidity_label"]))}</td>
                <td class="reason">{html.escape(format_value(row["signal_reason"]))}</td>
                <td>{source_cell}</td>
            </tr>
            """
        )

    return "\n".join(rows)


def render_html(
    top_movers: pd.DataFrame,
    signal_summary: pd.DataFrame,
    generated_at: str,
) -> str:
    file_status_rows = render_file_status()
    top_movers_rows = render_top_movers(top_movers)
    signal_summary_rows = render_signal_summary(signal_summary)

    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>World Cup Market Intelligence — Historical Trends</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
        }}

        .container {{
            max-width: 1220px;
            margin: 0 auto;
            padding: 32px 20px;
        }}

        .label {{
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            background: #1e293b;
            color: #cbd5e1;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 12px;
        }}

        h1 {{
            margin: 0 0 8px 0;
            font-size: 34px;
        }}

        h2 {{
            margin: 30px 0 10px 0;
            font-size: 24px;
        }}

        .subtitle {{
            color: #cbd5e1;
            max-width: 820px;
            line-height: 1.5;
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
            margin-top: 12px;
        }}

        th, td {{
            padding: 12px;
            border-bottom: 1px solid #334155;
            text-align: left;
            vertical-align: top;
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

        .team {{
            font-weight: 700;
        }}

        .change {{
            font-weight: 700;
            color: #facc15;
        }}

        .reason {{
            color: #94a3b8;
            max-width: 380px;
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
            margin-top: 28px;
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.5;
        }}

        @media (max-width: 900px) {{
            table {{
                display: block;
                overflow-x: auto;
            }}

            h1 {{
                font-size: 28px;
            }}
        }}
    </style>
</head>
<body>
    <main class="container">
        <section>
            <div class="label">Experimental historical trends</div>
            <h1>World Cup Market Intelligence — Historical Trends</h1>
            <p class="subtitle">
                Experimental preview of probability movement, top movers and signal classification
                generated from historical prediction-market snapshots.
            </p>
        </section>

        <section class="notice">
            Generated at <strong>{html.escape(generated_at)}</strong> UTC.
            These outputs are created by <code>scripts/run_historical_trends_workflow.py</code>.
            The trend system is experimental and should not be treated as betting or investment advice.
        </section>

        <section>
            <h2>Trend output status</h2>
            <table>
                <thead>
                    <tr>
                        <th>Output</th>
                        <th>Status</th>
                        <th>Path</th>
                    </tr>
                </thead>
                <tbody>
                    {file_status_rows}
                </tbody>
            </table>
        </section>

        <section>
            <h2>Top movers</h2>
            <p class="subtitle">
                Largest positive and negative probability moves, plus volume and liquidity movers,
                when available.
            </p>

            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Rank</th>
                        <th>Team</th>
                        <th>Outcome</th>
                        <th>Change</th>
                        <th>Direction</th>
                        <th>Current liquidity</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    {top_movers_rows}
                </tbody>
            </table>
        </section>

        <section>
            <h2>Signal summary</h2>
            <p class="subtitle">
                Transparent rule-based signal classification. This is not a black-box model.
            </p>

            <table>
                <thead>
                    <tr>
                        <th>Team</th>
                        <th>Outcome</th>
                        <th>Change</th>
                        <th>Signal</th>
                        <th>Strength</th>
                        <th>Liquidity label</th>
                        <th>Reason</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    {signal_summary_rows}
                </tbody>
            </table>
        </section>

        <section class="footer">
            <p>
                Main page:
                <a href="../">World Cup Market Intelligence</a>.
                Stable dashboard:
                <a href="../dashboard/">manual_csv dashboard</a>.
                Polymarket dashboard:
                <a href="../polymarket-dashboard/">Polymarket live dashboard</a>.
            </p>
            <p>
                Powered by <strong>Mayior Capital</strong>.
            </p>
            <p>
                This page is experimental and for research and education only.
            </p>
        </section>
    </main>
</body>
</html>
"""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    top_movers = read_optional_csv(TOP_MOVERS_PATH)
    signal_summary = read_optional_csv(SIGNAL_SUMMARY_PATH)

    html_content = render_html(
        top_movers=top_movers,
        signal_summary=signal_summary,
        generated_at=generated_at,
    )

    OUTPUT_PATH.write_text(html_content, encoding="utf-8")

    print("Historical trends dashboard")
    print(f"Top movers rows:     {len(top_movers)}")
    print(f"Signal summary rows: {len(signal_summary)}")
    print(f"Dashboard saved:     {OUTPUT_PATH}")


if __name__ == "__main__":
    main()