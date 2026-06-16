from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DEFAULT_FILES = {
    "Landing page": "docs/index.html",
    "Stable dashboard": "docs/dashboard/index.html",
    "Polymarket dashboard": "docs/polymarket-dashboard/index.html",
    "Trends dashboard": "docs/trends-dashboard/index.html",
    "Snapshot comparison": "data/processed/snapshot_comparison_latest.csv",
    "Probability deltas": "data/processed/probability_deltas_latest.csv",
    "Top movers": "data/processed/top_movers_latest.csv",
    "Signal summary": "data/processed/signal_summary_latest.csv",
    "Catalyst matches": "data/processed/catalyst_matches_latest.csv",
    "Team intelligence": "data/processed/team_intelligence_latest.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check freshness of dashboards and generated data outputs.",
    )
    parser.add_argument(
        "--stale-hours",
        type=float,
        default=72.0,
        help="Files older than this number of hours are marked stale.",
    )
    parser.add_argument(
        "--show-missing-only",
        action="store_true",
        help="Only show missing files.",
    )
    parser.add_argument(
        "--show-stale-only",
        action="store_true",
        help="Only show stale or missing files.",
    )
    return parser.parse_args()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def modified_time(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def format_age(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"

    minutes = seconds / 60

    if minutes < 60:
        return f"{minutes:.1f}m"

    hours = minutes / 60

    if hours < 48:
        return f"{hours:.1f}h"

    days = hours / 24
    return f"{days:.1f}d"


def freshness_status(path: Path, stale_hours: float) -> tuple[str, str, str]:
    if not path.exists():
        return "missing", "", ""

    now = utc_now()
    mtime = modified_time(path)
    age_seconds = (now - mtime).total_seconds()
    age_hours = age_seconds / 3600

    status = "fresh" if age_hours <= stale_hours else "stale"

    return (
        status,
        mtime.strftime("%Y-%m-%d %H:%M:%S UTC"),
        format_age(age_seconds),
    )


def print_header(stale_hours: float) -> None:
    print("World Cup Market Intelligence — Data Freshness Report")
    print(f"Root: {ROOT}")
    print(f"Stale threshold: {stale_hours} hours")
    print("")
    print("This report is informational:")
    print("- missing generated outputs can be normal")
    print("- stale outputs do not mean the project is broken")
    print("- stale data should not be overinterpreted")
    print("")


def should_show(
    status: str,
    show_missing_only: bool,
    show_stale_only: bool,
) -> bool:
    if show_missing_only:
        return status == "missing"

    if show_stale_only:
        return status in {"missing", "stale"}

    return True


def print_report(
    stale_hours: float,
    show_missing_only: bool,
    show_stale_only: bool,
) -> None:
    now = utc_now()
    available_count = 0
    fresh_count = 0
    stale_count = 0
    missing_count = 0

    print("=" * 110)
    print(f"{'Label':<26} {'Status':<10} {'Modified':<24} {'Age':<10} Path")
    print("=" * 110)

    for label, relative_path in DEFAULT_FILES.items():
        path = ROOT / relative_path
        status, modified, age = freshness_status(path, stale_hours)

        if path.exists():
            available_count += 1

        if status == "fresh":
            fresh_count += 1
        elif status == "stale":
            stale_count += 1
        elif status == "missing":
            missing_count += 1

        if not should_show(
            status=status,
            show_missing_only=show_missing_only,
            show_stale_only=show_stale_only,
        ):
            continue

        print(
            f"{label:<26} {status:<10} {modified:<24} {age:<10} {relative_path}"
        )

    print("=" * 110)
    print("")
    print("Summary")
    print(f"- Generated at: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"- Files tracked: {len(DEFAULT_FILES)}")
    print(f"- Available: {available_count}")
    print(f"- Fresh: {fresh_count}")
    print(f"- Stale: {stale_count}")
    print(f"- Missing: {missing_count}")
    print("")

    if missing_count > 0:
        print("Interpretation:")
        print("- Missing generated CSV outputs can be normal if workflows were not run locally.")
        print("- Public dashboard HTML files should normally exist.")
        print("")

    if stale_count > 0:
        print("Freshness warning:")
        print("- Some files are older than the configured threshold.")
        print("- This does not break the project, but public viewers should treat the data as stale.")
        print("")

    print("Result: PASS")
    print("Data freshness report completed.")


def main() -> None:
    args = parse_args()

    print_header(stale_hours=args.stale_hours)
    print_report(
        stale_hours=args.stale_hours,
        show_missing_only=bool(args.show_missing_only),
        show_stale_only=bool(args.show_stale_only),
    )


if __name__ == "__main__":
    main()
