from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the historical trends workflow.",
    )
    parser.add_argument(
        "--provider",
        default="polymarket",
        help="Provider to analyze, for example: polymarket or manual_csv.",
    )
    parser.add_argument(
        "--outcome",
        default="Yes",
        help="Outcome to analyze, for example: Yes.",
    )
    parser.add_argument(
        "--status",
        default="existing",
        help="Comparison status to analyze: existing, new or removed.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of rows per top movers category.",
    )
    parser.add_argument(
        "--min-abs-change-pp",
        type=float,
        default=0.0,
        help="Minimum absolute probability change in percentage points.",
    )
    parser.add_argument(
        "--strong-threshold-pp",
        type=float,
        default=2.0,
        help="Absolute percentage-point move required for a strong signal.",
    )
    parser.add_argument(
        "--moderate-threshold-pp",
        type=float,
        default=0.75,
        help="Absolute percentage-point move required for a moderate signal.",
    )
    parser.add_argument(
        "--min-liquidity",
        type=float,
        default=1000.0,
        help="Minimum liquidity before a move is treated as better supported.",
    )
    parser.add_argument(
        "--catalyst-lookback-days",
        type=int,
        default=7,
        help="Lookback window used when matching catalyst notes to signals.",
    )
    return parser.parse_args()


def run_step(name: str, command: list[str]) -> None:
    print("")
    print("=" * 80)
    print(f"RUNNING: {name}")
    print("=" * 80)
    print(" ".join(command))
    print("")

    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
    )

    if result.returncode != 0:
        print("")
        print(f"FAILED: {name}")
        print(f"Exit code: {result.returncode}")
        raise SystemExit(result.returncode)

    print("")
    print(f"PASS: {name}")


def main() -> None:
    args = parse_args()

    provider = str(args.provider).strip()
    outcome = str(args.outcome).strip()
    status = str(args.status).strip()

    print("World Cup Market Intelligence — Historical Trends Workflow")
    print(f"Provider: {provider}")
    print(f"Outcome:  {outcome}")
    print(f"Status:   {status}")
    print("")
    print("This workflow requires at least two processed snapshot CSV files.")
    print("For Polymarket, generate multiple live snapshots over time first.")
    print("")

    steps = [
        {
            "name": "Compare latest two snapshots",
            "command": [
                sys.executable,
                "scripts/compare_snapshots.py",
                "--provider",
                provider,
            ],
        },
        {
            "name": "Generate probability delta report",
            "command": [
                sys.executable,
                "scripts/generate_probability_deltas.py",
                "--provider",
                provider,
                "--outcome",
                outcome,
                "--status",
                status,
                "--min-abs-change-pp",
                str(args.min_abs_change_pp),
            ],
        },
        {
            "name": "Generate top movers report",
            "command": [
                sys.executable,
                "scripts/generate_top_movers.py",
                "--provider",
                provider,
                "--outcome",
                outcome,
                "--limit",
                str(args.limit),
                "--min-abs-change-pp",
                str(args.min_abs_change_pp),
            ],
        },
        {
            "name": "Generate signal summary report",
            "command": [
                sys.executable,
                "scripts/generate_signal_summary.py",
                "--provider",
                provider,
                "--outcome",
                outcome,
                "--strong-threshold-pp",
                str(args.strong_threshold_pp),
                "--moderate-threshold-pp",
                str(args.moderate_threshold_pp),
                "--min-liquidity",
                str(args.min_liquidity),
            ],
        },
        {
            "name": "Match catalyst notes to signals",
            "command": [
                sys.executable,
                "scripts/match_catalyst_notes.py",
                "--provider",
                provider,
                "--lookback-days",
                str(args.catalyst_lookback_days),
                "--include-unmatched",
            ],
        },
        {
            "name": "Generate historical trends dashboard",
            "command": [
                sys.executable,
                "scripts/generate_trends_dashboard.py",
            ],
        },
    ]

    for step in steps:
        run_step(step["name"], step["command"])

    print("")
    print("=" * 80)
    print("HISTORICAL TRENDS WORKFLOW PASSED")
    print("=" * 80)
    print("")
    print("Generated outputs:")
    print("- data/processed/snapshot_comparison_latest.csv")
    print("- data/processed/probability_deltas_latest.csv")
    print("- data/processed/top_movers_latest.csv")
    print("- data/processed/signal_summary_latest.csv")
    print("- data/processed/catalyst_matches_latest.csv")
    print("- docs/trends-dashboard/index.html")
    print("")
    print("Public dashboard path after commit/push:")
    print("- https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/")


if __name__ == "__main__":
    main()
