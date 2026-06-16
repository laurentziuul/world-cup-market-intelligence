from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


STEPS = [
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
    print("World Cup Market Intelligence — Polymarket Live Workflow")
    print("Provider: polymarket")
    print("Status: experimental")
    print("")
    print("This workflow requires live network access.")
    print("Polymarket may require VPN depending on DNS, Cloudflare or geo access.")
    print("")

    for step in STEPS:
        run_step(step["name"], step["command"])

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


if __name__ == "__main__":
    main()