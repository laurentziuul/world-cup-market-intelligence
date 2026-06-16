from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "private" / "operator_decision_log.csv"
DEFAULT_OUTPUT = ROOT / "data" / "private" / "operator_performance_summary.md"


def clean(value: str | None) -> str:
    if value is None:
        return "unknown"

    text = str(value).strip()

    if not text:
        return "unknown"

    return text


def parse_float(value: str | None) -> float:
    text = clean(value)

    if text in {"unknown", "n/a"}:
        return 0.0

    try:
        return float(text)
    except ValueError:
        return 0.0


def is_placeholder(row: dict[str, str]) -> bool:
    date = clean(row.get("date"))
    team = clean(row.get("team_or_outcome")).lower()
    market = clean(row.get("market")).lower()

    if date == "YYYY-MM-DD":
        return True

    if "example" in team or "example" in market:
        return True

    return False


def read_rows(path: Path, include_placeholders: bool = False) -> list[dict[str, str]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = [dict(row) for row in reader]

    if include_placeholders:
        return rows

    return [row for row in rows if not is_placeholder(row)]


def summarize(rows: list[dict[str, str]]) -> str:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    total_decisions = len(rows)
    by_operator: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_signal = Counter()
    by_mode = Counter()
    by_result = Counter()
    by_status = Counter()

    for row in rows:
        operator = clean(row.get("operator_id"))
        by_operator[operator].append(row)
        by_signal[clean(row.get("signal_type"))] += 1
        by_mode[clean(row.get("mode"))] += 1
        by_result[clean(row.get("result"))] += 1
        by_status[clean(row.get("status"))] += 1

    total_pnl = sum(parse_float(row.get("pnl_units")) for row in rows)

    closed_rows = [row for row in rows if clean(row.get("status")).lower() == "closed"]
    wins = [row for row in closed_rows if parse_float(row.get("pnl_units")) > 0]
    losses = [row for row in closed_rows if parse_float(row.get("pnl_units")) < 0]

    win_rate = 0.0
    if closed_rows:
        win_rate = len(wins) / len(closed_rows) * 100

    lines = [
        "# Operator Performance Summary",
        "",
        f"Generated at: {generated_at}",
        "",
        "Source file: data/private/operator_decision_log.csv",
        "",
        "This file is private operator research output.",
        "",
        "It should not be committed to the public repository.",
        "",
        "Powered by Mayior Capital.",
        "",
        "---",
        "",
        "## Research-only note",
        "",
        "This performance summary is for internal validation only.",
        "",
        "It is not betting advice.",
        "",
        "It is not investment advice.",
        "",
        "It is not financial advice.",
        "",
        "---",
        "",
        "## High-level performance",
        "",
        f"- Total decisions: {total_decisions}",
        f"- Closed decisions: {len(closed_rows)}",
        f"- Wins: {len(wins)}",
        f"- Losses: {len(losses)}",
        f"- Win rate: {win_rate:.2f}%",
        f"- Total PnL units: {total_pnl:.4f}",
        "",
        "---",
        "",
        "## Decisions by operator",
        "",
    ]

    if not by_operator:
        lines.append("- No real operator decisions logged yet.")
    else:
        for operator, operator_rows in sorted(by_operator.items()):
            pnl = sum(parse_float(row.get("pnl_units")) for row in operator_rows)
            closed = [
                row for row in operator_rows if clean(row.get("status")).lower() == "closed"
            ]
            operator_wins = [row for row in closed if parse_float(row.get("pnl_units")) > 0]
            operator_win_rate = (len(operator_wins) / len(closed) * 100) if closed else 0.0

            lines.extend(
                [
                    f"### {operator}",
                    "",
                    f"- Decisions: {len(operator_rows)}",
                    f"- Closed: {len(closed)}",
                    f"- Win rate: {operator_win_rate:.2f}%",
                    f"- PnL units: {pnl:.4f}",
                    "",
                ]
            )

    lines.extend(
        [
            "---",
            "",
            "## Signal type distribution",
            "",
        ]
    )

    if by_signal:
        for key, count in by_signal.most_common():
            lines.append(f"- {key}: {count}")
    else:
        lines.append("- No signal data yet.")

    lines.extend(
        [
            "",
            "---",
            "",
            "## Mode distribution",
            "",
        ]
    )

    if by_mode:
        for key, count in by_mode.most_common():
            lines.append(f"- {key}: {count}")
    else:
        lines.append("- No mode data yet.")

    lines.extend(
        [
            "",
            "---",
            "",
            "## Result distribution",
            "",
        ]
    )

    if by_result:
        for key, count in by_result.most_common():
            lines.append(f"- {key}: {count}")
    else:
        lines.append("- No result data yet.")

    lines.extend(
        [
            "",
            "---",
            "",
            "## Status distribution",
            "",
        ]
    )

    if by_status:
        for key, count in by_status.most_common():
            lines.append(f"- {key}: {count}")
    else:
        lines.append("- No status data yet.")

    lines.extend(
        [
            "",
            "---",
            "",
            "## Interpretation",
            "",
        ]
    )

    if total_decisions == 0:
        lines.extend(
            [
                "No real operator decisions have been logged yet.",
                "",
                "Next step:",
                "",
                "- generate the Daily Brief",
                "- review top movers",
                "- choose paper decisions for operator accounts",
                "- log decisions in data/private/operator_decision_log.csv",
                "- rerun this script",
            ]
        )
    else:
        lines.extend(
            [
                "Use this summary to compare operator accounts.",
                "",
                "Important questions:",
                "",
                "- Which operator creates the cleanest decisions?",
                "- Which signal type has the best PnL?",
                "- Does catalyst confirmation improve outcomes?",
                "- Does liquidity confirmation reduce false positives?",
                "- Does human discretion outperform mechanical filters?",
                "- Is doing nothing better than acting?",
            ]
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## Safety reminder",
            "",
            "Do not commit private operator logs, active positions or real-money PnL.",
            "",
            "Keep private research in data/private/ or a private repo.",
            "",
            "Powered by Mayior Capital.",
            "",
        ]
    )

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze private operator decision log and generate performance summary."
    )

    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Path to private operator decision log CSV.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to private operator performance summary markdown.",
    )
    parser.add_argument(
        "--include-placeholders",
        action="store_true",
        help="Include placeholder/example rows in analysis.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.is_absolute():
        input_path = ROOT / input_path

    if not output_path.is_absolute():
        output_path = ROOT / output_path

    rows = read_rows(input_path, include_placeholders=args.include_placeholders)
    summary = summarize(rows)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(summary, encoding="utf-8")

    print("Operator performance summary generated:")
    print(f"- {output_path.relative_to(ROOT)}")
    print(f"Real operator decisions analyzed: {len(rows)}")


if __name__ == "__main__":
    main()
