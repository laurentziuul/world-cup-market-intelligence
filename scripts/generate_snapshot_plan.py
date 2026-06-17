"""
generate_snapshot_plan.py
-------------------------
Read the World Cup match schedule and generate recommended snapshot windows
for the next 24h / 48h (configurable via --lookahead-hours).

Output: data/processed/snapshot_plan_latest.csv

Romania local time (UTC+3 / EEST) is used for all operator-facing columns.
UTC is provided as a machine-readable reference only.

Research-only. Not betting advice. Not investment advice.
Powered by Mayior Capital.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SCHEDULE = ROOT / "data" / "manual" / "world_cup_match_schedule.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "snapshot_plan_latest.csv"

# Romania is UTC+3 (EEST) for the entire 2026 World Cup window (June-July).
_ROMANIA_TZ = timezone(timedelta(hours=3))

# Teams that always trigger extended snapshot windows regardless of the
# major_market_impact flag in the CSV.
MAJOR_TEAMS: set[str] = {
    "france",
    "spain",
    "portugal",
    "england",
    "argentina",
    "germany",
    "brazil",
    "netherlands",
}

# (timedelta offset from kickoff, label, reason)
MAJOR_OFFSETS: list[tuple[timedelta, str, str]] = [
    (timedelta(hours=-3), "T-3h", "Pre-match early: observe liquidity build-up 3h before kickoff"),
    (timedelta(hours=-1), "T-1h", "Pre-match final: last probability check before kickoff"),
    (timedelta(minutes=30), "T+30m", "In-play early repricing window"),
    (timedelta(hours=2), "T+2h", "Post-match settlement: winner probability shift"),
]

NON_MAJOR_OFFSETS: list[tuple[timedelta, str, str]] = [
    (timedelta(hours=-1), "T-1h", "Pre-match check"),
    (timedelta(hours=1), "T+1h", "Post-match repricing check"),
]

OUTPUT_FIELDS: list[str] = [
    "match",
    "home_team",
    "away_team",
    "kickoff_romania_datetime",
    "kickoff_utc_datetime",
    "major_market_impact",
    "snapshot_label",
    "snapshot_romania_datetime",
    "snapshot_utc_datetime",
    "status",
    "reason",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def is_major_match(row: dict[str, str]) -> bool:
    """Return True if the match is major-market impact.

    Criteria (OR):
    - major_market_impact field is 'true'
    - home_team or away_team is in MAJOR_TEAMS
    """
    flag = str(row.get("major_market_impact", "false")).strip().lower()
    if flag in ("true", "yes", "1"):
        return True
    home = str(row.get("home_team", "")).strip().lower()
    away = str(row.get("away_team", "")).strip().lower()
    return home in MAJOR_TEAMS or away in MAJOR_TEAMS


def build_kickoff_utc_datetime(row: dict[str, str]) -> str:
    """Derive full ISO UTC datetime from match_date_utc + kickoff_utc columns.

    match_date_utc: YYYY-MM-DD
    kickoff_utc:    HH:MM

    Returns: YYYY-MM-DDTHH:MM:SSZ
    """
    date_str = str(row.get("match_date_utc", "")).strip()
    time_str = str(row.get("kickoff_utc", "")).strip()
    try:
        utc_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(
            tzinfo=timezone.utc
        )
        return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return "n/a"


def parse_kickoff_romania(row: dict[str, str]) -> datetime | None:
    """Parse kickoff_romania_datetime (YYYY-MM-DD HH:MM) as a tz-aware datetime."""
    ro_str = str(row.get("kickoff_romania_datetime", "")).strip()
    try:
        naive = datetime.strptime(ro_str, "%Y-%m-%d %H:%M")
        return naive.replace(tzinfo=_ROMANIA_TZ)
    except ValueError:
        return None


def generate_snapshot_rows(
    row: dict[str, str],
    kickoff_ro: datetime,
    kickoff_utc_dt_str: str,
    major: bool,
    now_utc: datetime,
) -> list[dict[str, str]]:
    """Generate snapshot window rows for one match."""
    offsets = MAJOR_OFFSETS if major else NON_MAJOR_OFFSETS
    home = str(row.get("home_team", "")).strip()
    away = str(row.get("away_team", "")).strip()
    match_label = f"{home} vs {away}"
    kickoff_ro_str = kickoff_ro.strftime("%Y-%m-%d %H:%M")

    rows: list[dict[str, str]] = []
    for offset, label, reason in offsets:
        snap_ro = kickoff_ro + offset
        snap_utc = snap_ro.astimezone(timezone.utc)

        is_past = snap_utc < now_utc
        status = "past" if is_past else "upcoming"

        rows.append(
            {
                "match": match_label,
                "home_team": home,
                "away_team": away,
                "kickoff_romania_datetime": kickoff_ro_str,
                "kickoff_utc_datetime": kickoff_utc_dt_str,
                "major_market_impact": "true" if major else "false",
                "snapshot_label": label,
                "snapshot_romania_datetime": snap_ro.strftime("%Y-%m-%d %H:%M"),
                "snapshot_utc_datetime": snap_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status": status,
                "reason": reason,
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate recommended snapshot windows around upcoming World Cup matches. "
            "Output: data/processed/snapshot_plan_latest.csv. "
            "Research-only. Not betting advice."
        )
    )
    parser.add_argument(
        "--schedule",
        default=str(DEFAULT_SCHEDULE),
        help="Path to world_cup_match_schedule.csv",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Output path for snapshot_plan_latest.csv",
    )
    parser.add_argument(
        "--lookahead-hours",
        type=int,
        default=48,
        help="Hours ahead to include matches (default 48). "
        "Matches are included if kickoff Romania time is within this window.",
    )
    parser.add_argument(
        "--lookbehind-hours",
        type=int,
        default=4,
        help=(
            "Hours behind to include matches (default 4). "
            "Keeps recently-kicked-off matches visible for post-match snapshot windows."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print results without writing output file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    schedule_path = Path(args.schedule)
    output_path = Path(args.output)

    if not schedule_path.exists():
        raise SystemExit(f"Schedule file not found: {schedule_path}")

    now_utc = datetime.now(timezone.utc)
    now_ro = now_utc.astimezone(_ROMANIA_TZ)

    window_start_ro = now_ro - timedelta(hours=args.lookbehind_hours)
    window_end_ro = now_ro + timedelta(hours=args.lookahead_hours)

    rows = read_csv_rows(schedule_path)
    print(f"Schedule loaded: {len(rows)} matches")
    print(f"Now Romania:     {now_ro.strftime('%Y-%m-%d %H:%M')} (UTC+3)")
    print(f"Window:          {window_start_ro.strftime('%Y-%m-%d %H:%M')} "
          f"-> {window_end_ro.strftime('%Y-%m-%d %H:%M')} (Romania)")

    output_rows: list[dict[str, str]] = []

    for row in rows:
        kickoff_ro = parse_kickoff_romania(row)
        if kickoff_ro is None:
            continue

        # Include match if kickoff falls within the lookbehind/lookahead window
        if kickoff_ro < window_start_ro or kickoff_ro > window_end_ro:
            continue

        major = is_major_match(row)
        kickoff_utc_dt_str = build_kickoff_utc_datetime(row)

        snap_rows = generate_snapshot_rows(
            row, kickoff_ro, kickoff_utc_dt_str, major, now_utc
        )
        output_rows.extend(snap_rows)

    # Sort by snapshot UTC datetime
    output_rows.sort(key=lambda r: r["snapshot_utc_datetime"])

    upcoming = [r for r in output_rows if r["status"] == "upcoming"]
    past = [r for r in output_rows if r["status"] == "past"]

    print(f"\nMatches in window: {len(set(r['match'] for r in output_rows))}")
    print(f"Snapshot windows:  {len(output_rows)} total "
          f"({len(upcoming)} upcoming, {len(past)} past)")

    if args.dry_run:
        print("\n--- DRY RUN: upcoming snapshot windows ---")
        for r in upcoming[:20]:
            major_tag = " [MAJOR]" if r["major_market_impact"] == "true" else ""
            print(
                f"  {r['snapshot_romania_datetime']} Romania  "
                f"{r['snapshot_label']:7s}  {r['match']}{major_tag}"
            )
        if not upcoming:
            print("  (no upcoming windows in this time range)")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nSnapshot plan written: {output_path}")

    if upcoming:
        print("\nNext upcoming snapshot windows:")
        for r in upcoming[:5]:
            major_tag = " [MAJOR]" if r["major_market_impact"] == "true" else ""
            print(
                f"  {r['snapshot_romania_datetime']} Romania  "
                f"{r['snapshot_label']:7s}  {r['match']}{major_tag}"
            )
    else:
        print("No upcoming snapshot windows in this time range.")


if __name__ == "__main__":
    main()
