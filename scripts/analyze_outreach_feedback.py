from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "manual" / "outreach_feedback.csv"
DEFAULT_OUTPUT = ROOT / "docs" / "outreach_feedback_summary.md"


def clean(value: str | None) -> str:
    if value is None:
        return "unknown"

    text = str(value).strip()

    if not text:
        return "unknown"

    return text


def is_placeholder_row(row: dict[str, str]) -> bool:
    date = clean(row.get("date"))
    contact = clean(row.get("contact_or_community")).lower()

    if date == "YYYY-MM-DD":
        return True

    if contact.startswith("example"):
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

    return [row for row in rows if not is_placeholder_row(row)]


def count_field(rows: Iterable[dict[str, str]], field: str) -> Counter[str]:
    counter: Counter[str] = Counter()

    for row in rows:
        counter[clean(row.get(field))] += 1

    return counter


def format_counter(counter: Counter[str], empty_label: str = "No data yet.") -> list[str]:
    if not counter:
        return [f"- {empty_label}"]

    lines = []

    for key, count in counter.most_common():
        lines.append(f"- {key}: {count}")

    return lines


def count_positive_signals(rows: list[dict[str, str]]) -> dict[str, int]:
    interest_values = [clean(row.get("interest_level")).lower() for row in rows]
    payment_values = [clean(row.get("payment_intent")).lower() for row in rows]
    status_values = [clean(row.get("response_status")).lower() for row in rows]

    wants_more = sum(
        1
        for value in interest_values + status_values
        if value in {"wants more", "payment intent", "custom report lead", "payment discussion"}
    )

    payment_intent = sum(
        1
        for value in payment_values + interest_values
        if value in {
            "maybe",
            "yes 19 eur",
            "yes 49 eur",
            "yes custom report",
            "payment intent",
            "custom report lead",
            "wants free trial first",
        }
    )

    custom_report_leads = sum(
        1
        for value in interest_values + status_values + payment_values
        if value in {"custom report lead", "yes custom report"}
    )

    replies = sum(
        1
        for value in status_values
        if value
        in {
            "replied",
            "interested",
            "wants more",
            "payment discussion",
            "custom report lead",
        }
    )

    return {
        "replies": replies,
        "wants_more": wants_more,
        "payment_intent": payment_intent,
        "custom_report_leads": custom_report_leads,
    }


def build_summary(rows: list[dict[str, str]], source_path: Path) -> str:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    response_status = count_field(rows, "response_status")
    interest_level = count_field(rows, "interest_level")
    profile_type = count_field(rows, "profile_type")
    channel = count_field(rows, "channel")
    useful_section = count_field(rows, "useful_section")
    payment_intent = count_field(rows, "payment_intent")
    preferred_delivery = count_field(rows, "preferred_delivery")

    signals = count_positive_signals(rows)

    total = len(rows)

    if total == 0:
        validation_status = "No real outreach data yet."
    elif signals["payment_intent"] >= 2 or signals["custom_report_leads"] >= 1:
        validation_status = "Strong early validation signal."
    elif signals["wants_more"] >= 3 or signals["payment_intent"] >= 1:
        validation_status = "Promising early validation signal."
    elif signals["replies"] >= 5:
        validation_status = "Feedback available, but demand not yet proven."
    else:
        validation_status = "Too early to judge."

    lines = [
        "# Outreach Feedback Summary",
        "",
        f"Generated at: {generated_at}",
        "",
        f"Source file: {source_path.relative_to(ROOT).as_posix()}",
        "",
        "Powered by Mayior Capital.",
        "",
        "---",
        "",
        "## Research-only note",
        "",
        "This summary is used for product validation.",
        "",
        "It is not betting advice.",
        "",
        "It is not investment advice.",
        "",
        "It is not financial advice.",
        "",
        "---",
        "",
        "## High-level status",
        "",
        f"- Real outreach entries: {total}",
        f"- Replies: {signals['replies']}",
        f"- Wants more reports: {signals['wants_more']}",
        f"- Payment-intent signals: {signals['payment_intent']}",
        f"- Custom report leads: {signals['custom_report_leads']}",
        f"- Validation status: {validation_status}",
        "",
        "---",
        "",
        "## Response status",
        "",
        *format_counter(response_status),
        "",
        "---",
        "",
        "## Interest level",
        "",
        *format_counter(interest_level),
        "",
        "---",
        "",
        "## Profile types",
        "",
        *format_counter(profile_type),
        "",
        "---",
        "",
        "## Channels",
        "",
        *format_counter(channel),
        "",
        "---",
        "",
        "## Useful sections",
        "",
        *format_counter(useful_section),
        "",
        "---",
        "",
        "## Payment intent",
        "",
        *format_counter(payment_intent),
        "",
        "---",
        "",
        "## Preferred delivery",
        "",
        *format_counter(preferred_delivery),
        "",
        "---",
        "",
        "## Interpretation",
        "",
    ]

    if total == 0:
        lines.extend(
            [
                "No real outreach data has been added yet.",
                "",
                "Next step:",
                "",
                "- send the sample brief to 10 warm contacts",
                "- use aliases instead of private names",
                "- log responses in data/manual/outreach_feedback.csv",
                "- rerun this script",
            ]
        )
    else:
        lines.extend(
            [
                "Use this summary to decide what to build next.",
                "",
                "Strongest next-build signals:",
                "",
                "- people ask for the next report",
                "- people prefer Telegram or Discord delivery",
                "- people show payment intent",
                "- communities ask for custom reports",
                "- one section repeatedly appears as useful",
            ]
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## Privacy reminder",
            "",
            "If this repository is public, do not store private names, phone numbers, emails or personal details in the CSV.",
            "",
            "Use aliases such as:",
            "",
            "- crypto_contact_01",
            "- telegram_group_01",
            "- football_creator_01",
            "",
            "Powered by Mayior Capital.",
            "",
        ]
    )

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze outreach feedback CSV and generate a validation summary."
    )

    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Path to outreach feedback CSV.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to markdown summary output.",
    )
    parser.add_argument(
        "--include-placeholders",
        action="store_true",
        help="Include placeholder example rows in the analysis.",
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
    summary = build_summary(rows, input_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(summary, encoding="utf-8")

    print("Outreach feedback summary generated:")
    print(f"- {output_path.relative_to(ROOT)}")
    print(f"Real outreach entries analyzed: {len(rows)}")


if __name__ == "__main__":
    main()
