from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the experimental Polymarket live workflow.",
    )
    parser.add_argument(
        "--include-trends",
        action="store_true",
        help=(
            "Also run the historical trends workflow after generating the live "
            "Polymarket snapshot. Requires at least two Polymarket snapshots."
        ),
    )
    return parser.parse_args()


def build_steps(include_trends: bool) -> list[dict[str, list[str] | str]]:
    steps: list[dict[str, list[str] | str]] = [
        {
            "name": "Validate experimental Polymarket provider",
            "command": [
                sys.executable,
                "scripts/validate_providers.py",
                "--provider",
                "polymarket",
                "--include-live",
            ],
        },
        {
            "name": "Update Polymarket live snapshot",
            "command": [
                sys.executable,
                "scripts/update_snapshot.py",
                "--provider",
                "polymarket",
            ],
        },
        {
            "name": "Generate Polymarket YES-only World Cup ranking",
            "command": [
                sys.executable,
                "scripts/generate_polymarket_yes_ranking.py",
            ],
        },
    ]

    if include_trends:
        steps.append(
            {
                "name": "Generate historical trends and signal intelligence",
                "command": [
                    sys.executable,
                    "scripts/run_historical_trends_workflow.py",
                    "--provider",
                    "polymarket",
                    "--outcome",
                    "Yes",
                    "--status",
                    "existing",
                ],
            }
        )

    steps.append(
        {
            "name": "Generate separate Polymarket live dashboard",
            "command": [
                sys.executable,
                "scripts/generate_polymarket_live_dashboard.py",
            ],
        }
    )

    return steps


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

    print("World Cup Market Intelligence — Polymarket Live Workflow")
    print("Provider: polymarket")
    print("Status: experimental")
    print(f"Include trends: {args.include_trends}")
    print("")
    print("This workflow requires live network access.")
    print("Polymarket may require VPN depending on DNS, Cloudflare or geo access.")
    print("")

    if args.include_trends:
        print("Historical trends are enabled.")
        print("This requires at least two processed Polymarket snapshot CSV files.")
        print("")

    for step in build_steps(include_trends=bool(args.include_trends)):
        run_step(
            name=str(step["name"]),
            command=list(step["command"]),
        )

    print("")
    print("=" * 80)
    print("POLYMARKET LIVE WORKFLOW PASSED")
    print("=" * 80)
    print("")
    print("Generated outputs:")
    print("- data/processed/snapshot_latest.csv")
    print("- data/processed/snapshots/*-polymarket.csv")
    print("- data/processed/polymarket_worldcup_yes_ranking.csv")
    print("- data/processed/polymarket_worldcup_yes_ranking_summary.txt")

    if args.include_trends:
        print("- data/processed/snapshot_comparison_latest.csv")
        print("- data/processed/probability_deltas_latest.csv")
        print("- data/processed/top_movers_latest.csv")
        print("- data/processed/signal_summary_latest.csv")

    print("- docs/polymarket-dashboard/index.html")
    print("")
    print("Public dashboard path after commit/push:")
    print("- https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/")


if __name__ == "__main__":
    main()