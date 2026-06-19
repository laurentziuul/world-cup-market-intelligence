from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = ROOT / "docs" / "trends-dashboard"
OUTPUT_PATH = OUTPUT_DIR / "index.html"

TOP_MOVERS_PATH = ROOT / "data" / "processed" / "top_movers_latest.csv"
SIGNAL_SUMMARY_PATH = ROOT / "data" / "processed" / "signal_summary_latest.csv"
PROBABILITY_DELTAS_PATH = ROOT / "data" / "processed" / "probability_deltas_latest.csv"
CATALYST_MATCHES_PATH = ROOT / "data" / "processed" / "catalyst_matches_latest.csv"
TEAM_INTELLIGENCE_PATH = ROOT / "data" / "processed" / "team_intelligence_latest.csv"
DASHBOARD_METADATA_PATH = ROOT / "data" / "processed" / "dashboard_metadata_latest.json"


def read_optional_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def read_optional_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def format_value(value: object) -> str:
    if pd.isna(value):
        return ""

    return str(value)


def render_file_status() -> str:
    files = {
        "Probability deltas": PROBABILITY_DELTAS_PATH,
        "Top movers": TOP_MOVERS_PATH,
        "Signal summary": SIGNAL_SUMMARY_PATH,
        "Catalyst matches": CATALYST_MATCHES_PATH,
        "Team intelligence": TEAM_INTELLIGENCE_PATH,
        "Dashboard metadata": DASHBOARD_METADATA_PATH,
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


def render_freshness_panel(metadata: dict[str, object]) -> str:
    if not metadata:
        return """
        <section>
            <h2>Data freshness and trust status</h2>
            <div class="notice warning-box">
                <strong>Metadata missing.</strong>
                Run <code>python scripts/generate_dashboard_metadata.py</code> before generating this dashboard
                to show freshness and trust information.
            </div>
        </section>
        """

    public_status = str(metadata.get("public_dashboard_status", "unknown"))
    generated_at = str(metadata.get("generated_at", ""))
    stale_threshold = str(metadata.get("stale_threshold_hours", ""))
    dashboard_available = str(metadata.get("dashboard_available_count", ""))
    dashboard_count = str(metadata.get("dashboard_count", ""))
    output_available = str(metadata.get("generated_output_available_count", ""))
    output_count = str(metadata.get("generated_output_count", ""))
    warnings = metadata.get("warnings", [])

    status_class = "status-ok"

    if public_status == "stale":
        status_class = "status-warning"
    elif public_status == "incomplete":
        status_class = "status-missing"

    if not isinstance(warnings, list):
        warnings = []

    if warnings:
        warning_items = "\n".join(
            f"<li>{html.escape(str(warning))}</li>"
            for warning in warnings
        )
    else:
        warning_items = "<li>No metadata warnings.</li>"

    return f"""
        <section>
            <h2>Data freshness and trust status</h2>
            <p class="subtitle">
                Metadata-generated trust layer showing dashboard availability, generated output status
                and stale/missing output warnings.
            </p>

            <div class="trust-grid">
                <div class="trust-card">
                    <div class="trust-label">Public dashboard status</div>
                    <div class="trust-value {status_class}">{html.escape(public_status)}</div>
                </div>

                <div class="trust-card">
                    <div class="trust-label">Metadata generated at</div>
                    <div class="trust-value">{html.escape(generated_at)}</div>
                </div>

                <div class="trust-card">
                    <div class="trust-label">Stale threshold</div>
                    <div class="trust-value">{html.escape(stale_threshold)} hours</div>
                </div>

                <div class="trust-card">
                    <div class="trust-label">Dashboards available</div>
                    <div class="trust-value">{html.escape(dashboard_available)} / {html.escape(dashboard_count)}</div>
                </div>

                <div class="trust-card">
                    <div class="trust-label">Generated outputs available</div>
                    <div class="trust-value">{html.escape(output_available)} / {html.escape(output_count)}</div>
                </div>

                <div class="trust-card">
                    <div class="trust-label">Interpretation</div>
                    <div class="trust-value">research-only</div>
                </div>
            </div>

            <div class="notice">
                <strong>Warnings:</strong>
                <ul>
                    {warning_items}
                </ul>
            </div>
        </section>
    """


def render_team_intelligence(team_intelligence: pd.DataFrame) -> str:
    if team_intelligence.empty:
        return """
        <tr>
            <td colspan="12">No team intelligence output found yet. Run the historical trends workflow first.</td>
        </tr>
        """

    columns = [
        "review_priority",
        "team",
        "provider",
        "total_signals",
        "positive_signals",
        "negative_signals",
        "matched_catalysts",
        "unmatched_signals",
        "strongest_signal",
        "summary_label",
        "latest_signal_date",
        "latest_catalyst_date",
    ]

    for column in columns:
        if column not in team_intelligence.columns:
            team_intelligence[column] = ""

    rows = []

    for _, row in team_intelligence.head(40).iterrows():
        priority = format_value(row["review_priority"]).lower()
        priority_class = "priority-low"

        if priority == "high":
            priority_class = "priority-high"
        elif priority == "medium":
            priority_class = "priority-medium"

        rows.append(
            f"""
            <tr>
                <td class="{priority_class}">{html.escape(format_value(row["review_priority"]))}</td>
                <td class="team">{html.escape(format_value(row["team"]))}</td>
                <td>{html.escape(format_value(row["provider"]))}</td>
                <td>{html.escape(format_value(row["total_signals"]))}</td>
                <td>{html.escape(format_value(row["positive_signals"]))}</td>
                <td>{html.escape(format_value(row["negative_signals"]))}</td>
                <td>{html.escape(format_value(row["matched_catalysts"]))}</td>
                <td>{html.escape(format_value(row["unmatched_signals"]))}</td>
                <td>{html.escape(format_value(row["strongest_signal"]))}</td>
                <td>{html.escape(format_value(row["summary_label"]))}</td>
                <td>{html.escape(format_value(row["latest_signal_date"]))}</td>
                <td>{html.escape(format_value(row["latest_catalyst_date"]))}</td>
            </tr>
            """
        )

    return "\n".join(rows)


DIRECTION_BADGE = {
    "up": '<span class="badge badge-up">UP</span>',
    "down": '<span class="badge badge-down">DOWN</span>',
    "flat": '<span class="badge badge-flat">FLAT</span>',
    "watch": '<span class="badge badge-watch">WATCH</span>',
}


def render_direction_badge(direction: str) -> str:
    key = str(direction).strip().lower()
    if key in DIRECTION_BADGE:
        return DIRECTION_BADGE[key]
    if key in ("positive", "rising"):
        return DIRECTION_BADGE["up"]
    if key in ("negative", "falling", "declining"):
        return DIRECTION_BADGE["down"]
    if key in ("flat_no_signal", "unchanged"):
        return DIRECTION_BADGE["flat"]
    if key:
        return f'<span class="badge badge-watch">{html.escape(direction.upper())}</span>'
    return ""


def render_summary_cards(
    top_movers: pd.DataFrame,
    team_intelligence: pd.DataFrame,
    metadata: dict[str, object],
    generated_at: str,
) -> str:
    top_positive = "\u2014"
    top_positive_change = ""
    top_negative = "\u2014"
    top_negative_change = ""

    if not top_movers.empty and "direction" in top_movers.columns:
        pos = top_movers[
            top_movers["direction"].astype(str).str.lower().isin(["up", "positive", "rising"])
        ]
        neg = top_movers[
            top_movers["direction"].astype(str).str.lower().isin(["down", "negative", "falling", "declining"])
        ]
        if not pos.empty:
            r = pos.iloc[0]
            top_positive = str(r.get("team", "\u2014"))
            top_positive_change = str(r.get("probability_change_display", ""))
        if not neg.empty:
            r = neg.iloc[0]
            top_negative = str(r.get("team", "\u2014"))
            top_negative_change = str(r.get("probability_change_display", ""))

    top_priority_team = "\u2014"
    if not team_intelligence.empty and "review_priority" in team_intelligence.columns:
        high = team_intelligence[
            team_intelligence["review_priority"].astype(str).str.lower() == "high"
        ]
        if not high.empty and "team" in high.columns:
            top_priority_team = str(high.iloc[0]["team"])
        elif "team" in team_intelligence.columns:
            top_priority_team = str(team_intelligence.iloc[0]["team"])

    freshness = str(metadata.get("public_dashboard_status", "unknown")) if metadata else "unknown"
    freshness_class = "status-ok" if freshness == "ok" else ("status-warning" if freshness == "stale" else "status-missing")

    pos_change_html = (
        f' <span style="color:#86efac;font-size:13px;">{html.escape(top_positive_change)}</span>'
        if top_positive_change else ""
    )
    neg_change_html = (
        f' <span style="color:#fca5a5;font-size:13px;">{html.escape(top_negative_change)}</span>'
        if top_negative_change else ""
    )

    return f"""
        <div class="summary-cards">
            <div class="summary-card">
                <div class="summary-label">Top positive mover</div>
                <div class="summary-value">{html.escape(top_positive)}{pos_change_html}</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">Top negative mover</div>
                <div class="summary-value">{html.escape(top_negative)}{neg_change_html}</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">Highest priority team</div>
                <div class="summary-value">{html.escape(top_priority_team)}</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">Freshness status</div>
                <div class="summary-value {freshness_class}">{html.escape(freshness)}</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">Last generated</div>
                <div class="summary-value" style="font-size:14px;">{html.escape(generated_at)} UTC</div>
            </div>
        </div>
    """


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
                <td>{render_direction_badge(format_value(row["direction"]))}</td>
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


def render_catalyst_matches(catalyst_matches: pd.DataFrame) -> str:
    if catalyst_matches.empty:
        return """
        <tr>
            <td colspan="9">No catalyst matches found yet. Run the historical trends workflow after adding catalyst notes.</td>
        </tr>
        """

    columns = [
        "team",
        "signal_label",
        "probability_change_display",
        "event_type",
        "event_title",
        "catalyst_confidence",
        "match_type",
        "match_reason",
        "catalyst_source_url",
    ]

    for column in columns:
        if column not in catalyst_matches.columns:
            catalyst_matches[column] = ""

    rows = []

    useful = catalyst_matches[
        catalyst_matches["match_type"].astype(str) != "unmatched"
    ].copy()

    if useful.empty:
        useful = catalyst_matches.copy()

    for _, row in useful.head(40).iterrows():
        source_url = html.escape(format_value(row["catalyst_source_url"]))
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
                <td>{html.escape(format_value(row["signal_label"]))}</td>
                <td class="change">{html.escape(format_value(row["probability_change_display"]))}</td>
                <td>{html.escape(format_value(row["event_type"]))}</td>
                <td>{html.escape(format_value(row["event_title"]))}</td>
                <td>{html.escape(format_value(row["catalyst_confidence"]))}</td>
                <td>{html.escape(format_value(row["match_type"]))}</td>
                <td class="reason">{html.escape(format_value(row["match_reason"]))}</td>
                <td>{source_cell}</td>
            </tr>
            """
        )

    return "\n".join(rows)


def render_html(
    metadata: dict[str, object],
    team_intelligence: pd.DataFrame,
    top_movers: pd.DataFrame,
    signal_summary: pd.DataFrame,
    catalyst_matches: pd.DataFrame,
    generated_at: str,
) -> str:
    file_status_rows = render_file_status()
    freshness_panel = render_freshness_panel(metadata)
    team_intelligence_rows = render_team_intelligence(team_intelligence)
    top_movers_rows = render_top_movers(top_movers)
    signal_summary_rows = render_signal_summary(signal_summary)
    catalyst_matches_rows = render_catalyst_matches(catalyst_matches)
    summary_cards_html = render_summary_cards(top_movers, team_intelligence, metadata, generated_at)

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
            max-width: 1280px;
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
            max-width: 880px;
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

        .warning-box {{
            border-color: #f59e0b;
        }}

        .trust-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin-top: 14px;
        }}

        .trust-card {{
            background: #111827;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 14px;
        }}

        .trust-label {{
            color: #94a3b8;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 8px;
        }}

        .trust-value {{
            font-weight: 800;
            color: #e5e7eb;
            word-break: break-word;
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

        .status-warning {{
            color: #fde68a;
            font-weight: 700;
        }}

        .status-missing {{
            color: #fdba74;
            font-weight: 700;
        }}

        .priority-high {{
            color: #fca5a5;
            font-weight: 800;
        }}

        .priority-medium {{
            color: #fde68a;
            font-weight: 800;
        }}

        .priority-low {{
            color: #86efac;
            font-weight: 800;
        }}

        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 14px;
            margin: 22px 0;
        }}

        .summary-card {{
            background: #111827;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 16px;
        }}

        .summary-label {{
            color: #94a3b8;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 8px;
        }}

        .summary-value {{
            font-weight: 800;
            font-size: 16px;
            color: #e5e7eb;
            word-break: break-word;
        }}

        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        .badge-up {{
            background: #14532d;
            color: #86efac;
        }}

        .badge-down {{
            background: #450a0a;
            color: #fca5a5;
        }}

        .badge-flat {{
            background: #1e293b;
            color: #94a3b8;
        }}

        .badge-watch {{
            background: #713f12;
            color: #fde68a;
        }}

        .footer {{
            margin-top: 28px;
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.5;
        }}

        @media (max-width: 1200px) {{
            .summary-cards {{
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }}
        }}

        @media (max-width: 900px) {{
            table {{
                display: block;
                overflow-x: auto;
            }}

            .trust-grid {{
                grid-template-columns: 1fr;
            }}

            .summary-cards {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}

            h1 {{
                font-size: 28px;
            }}
        }}

        @media (max-width: 560px) {{
            .summary-cards {{
                grid-template-columns: 1fr;
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
                Experimental preview of probability movement, top movers, signal classification,
                catalyst-note matching, team-level intelligence and dashboard freshness metadata.
            </p>
        </section>

        <section class="notice">
            Generated at <strong>{html.escape(generated_at)}</strong> UTC.
            These outputs are created by <code>scripts/run_historical_trends_workflow.py</code>
            and <code>scripts/generate_dashboard_metadata.py</code>.
            The trend, catalyst, team-intelligence and trust system is experimental and should not be treated as betting or investment advice.
        </section>

        {summary_cards_html}

        {freshness_panel}

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
            <h2>Team intelligence</h2>
            <p class="subtitle">
                Team-level summary combining signals and catalyst matches. This section helps identify
                which teams deserve manual review first.
            </p>

            <table>
                <thead>
                    <tr>
                        <th>Priority</th>
                        <th>Team</th>
                        <th>Provider</th>
                        <th>Total signals</th>
                        <th>Positive</th>
                        <th>Negative</th>
                        <th>Matched catalysts</th>
                        <th>Unmatched signals</th>
                        <th>Strongest signal</th>
                        <th>Summary label</th>
                        <th>Latest signal</th>
                        <th>Latest catalyst</th>
                    </tr>
                </thead>
                <tbody>
                    {team_intelligence_rows}
                </tbody>
            </table>
        </section>

        <section>
            <h2>Top movers <span style="font-size:15px;font-weight:400;color:#94a3b8;">— UP / DOWN / FLAT / WATCH</span></h2>
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

        <section>
            <h2>Catalyst matches</h2>
            <p class="subtitle">
                Manual catalyst notes matched to generated signal rows by team or market identifier
                and a configurable lookback window.
            </p>

            <table>
                <thead>
                    <tr>
                        <th>Team</th>
                        <th>Signal</th>
                        <th>Change</th>
                        <th>Event type</th>
                        <th>Event title</th>
                        <th>Confidence</th>
                        <th>Match type</th>
                        <th>Match reason</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    {catalyst_matches_rows}
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

    metadata = read_optional_json(DASHBOARD_METADATA_PATH)
    team_intelligence = read_optional_csv(TEAM_INTELLIGENCE_PATH)
    top_movers = read_optional_csv(TOP_MOVERS_PATH)
    signal_summary = read_optional_csv(SIGNAL_SUMMARY_PATH)
    catalyst_matches = read_optional_csv(CATALYST_MATCHES_PATH)

    html_content = render_html(
        metadata=metadata,
        team_intelligence=team_intelligence,
        top_movers=top_movers,
        signal_summary=signal_summary,
        catalyst_matches=catalyst_matches,
        generated_at=generated_at,
    )

    OUTPUT_PATH.write_text(html_content, encoding="utf-8")

    print("Historical trends dashboard")
    print(f"Metadata available:      {bool(metadata)}")
    print(f"Team intelligence rows: {len(team_intelligence)}")
    print(f"Top movers rows:        {len(top_movers)}")
    print(f"Signal summary rows:    {len(signal_summary)}")
    print(f"Catalyst matches rows:  {len(catalyst_matches)}")
    print(f"Dashboard saved:        {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
