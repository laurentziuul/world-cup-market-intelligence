from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_command(label: str, command: list[str]) -> None:
    print("")
    print("=" * 80)
    print(f"RUNNING: {label}")
    print("=" * 80)
    print(" ".join(command))
    print("")

    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
    )

    if result.returncode != 0:
        raise SystemExit(
            f"\nFAILED: {label}\n"
            f"Exit code: {result.returncode}"
        )

    print("")
    print(f"PASS: {label}")


def build_commands(provider: str) -> list[tuple[str, list[str]]]:
    python = sys.executable

    return [
        (
            "Validate providers",
            [
                python,
                "scripts/validate_providers.py",
                "--provider",
                provider,
            ],
        ),
        (
            "Export provider sample",
            [
                python,
                "scripts/export_provider_sample.py",
                "--provider",
                provider,
            ],
        ),
        (
            "Update snapshot",
            [
                python,
                "scripts/update_snapshot.py",
                "--provider",
                provider,
            ],
        ),
        (
            "Generate trends",
            [
                python,
                "scripts/generate_trends.py",
            ],
        ),
        (
            "Generate dashboard",
            [
                python,
                "scripts/generate_dashboard.py",
            ],
        ),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a full local smoke test for the World Cup Market Intelligence pipeline."
    )

    parser.add_argument(
        "--provider",
        default="manual_csv",
        help="Provider to test through the full pipeline.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("World Cup Market Intelligence — Pipeline Smoke Test")
    print(f"Provider: {args.provider}")

    commands = build_commands(args.provider)

    for label, command in commands:
        run_command(label, command)

    print("")
    print("=" * 80)
    print("SMOKE TEST PASSED")
    print("=" * 80)
    print("")
    print("Pipeline verified successfully:")
    print("- provider validation")
    print("- provider sample export")
    print("- snapshot update")
    print("- trend generation")
    print("- dashboard generation")


if __name__ == "__main__":
    main()