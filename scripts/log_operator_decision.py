from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "data" / "private" / "operator_decision_log.csv"
DEFAULT_OPERATORS = ROOT / "data" / "manual" / "operator_accounts.csv"

FIELDNAMES = [
    "date",
    "operator_id",
    "market",
    "team_or_outcome",
    "signal_type",
    "catalyst_status",
    "probability_at_decision",
    "implied_odds",
    "decision_type",
    "mode",
    "position_size_units",
    "risk_units",
    "entry_reason",
    "exit_plan",
    "status",
    "result",
    "pnl_units",
    "notes",
]


def load_operator_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return {
            str(row.get("operator_id", "")).strip()
            for row in reader
            if str(row.get("operator_id", "")).strip()
        }


def ensure_log_exists(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        return

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()


def append_decision(path: Path, row: dict[str, str]) -> None:
    ensure_log_exists(path)

    with path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append one private operator decision to data/private/operator_decision_log.csv."
    )

    parser.add_argument("--operator-id", required=True, help="Operator ID, for example operator_09.")
    parser.add_argument("--market", required=True, help="Market name.")
    parser.add_argument("--team-or-outcome", required=True, help="Team or outcome being reviewed.")
    parser.add_argument("--signal-type", required=True, help="Main signal type.")
    parser.add_argument("--catalyst-status", default="unknown", help="Catalyst status.")
    parser.add_argument("--probability", default="n/a", help="Probability at decision time.")
    parser.add_argument("--implied-odds", default="n/a", help="Implied odds at decision time.")
    parser.add_argument("--decision-type", default="paper_entry", help="paper_entry, real_entry, watchlist_only, no_trade, exit, reduce, add.")
    parser.add_argument("--mode", default="paper", choices=["paper", "real"], help="Decision mode.")
    parser.add_argument("--position-size-units", default="1", help="Position size in internal units.")
    parser.add_argument("--risk-units", default="0", help="Risk amount in internal units.")
    parser.add_argument("--entry-reason", required=True, help="Why the decision exists.")
    parser.add_argument("--exit-plan", default="review after next snapshot", help="Exit or invalidation plan.")
    parser.add_argument("--status", default="open", help="open, closed, cancelled, watchlist.")
    parser.add_argument("--result", default="unknown", help="unknown, win, loss, break_even, no_trade.")
    parser.add_argument("--pnl-units", default="0", help="PnL in internal units.")
    parser.add_argument("--notes", default="", help="Optional private notes.")
    parser.add_argument("--date", default=None, help="Decision date. Defaults to current UTC date.")
    parser.add_argument("--log-path", default=str(DEFAULT_LOG), help="Private decision log path.")
    parser.add_argument("--operators-path", default=str(DEFAULT_OPERATORS), help="Operator accounts CSV path.")
    parser.add_argument("--allow-unknown-operator", action="store_true", help="Allow operator IDs not found in operator_accounts.csv.")
    parser.add_argument("--dry-run", action="store_true", help="Print row without writing.")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    log_path = Path(args.log_path)
    operators_path = Path(args.operators_path)

    if not log_path.is_absolute():
        log_path = ROOT / log_path

    if not operators_path.is_absolute():
        operators_path = ROOT / operators_path

    operator_ids = load_operator_ids(operators_path)

    if operator_ids and args.operator_id not in operator_ids and not args.allow_unknown_operator:
        raise SystemExit(
            f"Unknown operator_id: {args.operator_id}. "
            "Use one from data/manual/operator_accounts.csv or pass --allow-unknown-operator."
        )

    decision_date = args.date or datetime.now(timezone.utc).date().isoformat()

    row = {
        "date": decision_date,
        "operator_id": args.operator_id,
        "market": args.market,
        "team_or_outcome": args.team_or_outcome,
        "signal_type": args.signal_type,
        "catalyst_status": args.catalyst_status,
        "probability_at_decision": args.probability,
        "implied_odds": args.implied_odds,
        "decision_type": args.decision_type,
        "mode": args.mode,
        "position_size_units": args.position_size_units,
        "risk_units": args.risk_units,
        "entry_reason": args.entry_reason,
        "exit_plan": args.exit_plan,
        "status": args.status,
        "result": args.result,
        "pnl_units": args.pnl_units,
        "notes": args.notes,
    }

    if args.dry_run:
        print("Dry run operator decision row:")
        for key in FIELDNAMES:
            print(f"- {key}: {row[key]}")
        return

    append_decision(log_path, row)

    print("Operator decision logged:")
    print(f"- {log_path.relative_to(ROOT)}")
    print(f"- operator_id: {args.operator_id}")
    print(f"- market: {args.market}")
    print(f"- team_or_outcome: {args.team_or_outcome}")
    print(f"- mode: {args.mode}")
    print(f"- decision_type: {args.decision_type}")


if __name__ == "__main__":
    main()
