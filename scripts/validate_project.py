from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "README.md",
    "docs/index.html",
    "docs/dashboard/index.html",
    "docs/polymarket-dashboard/index.html",
    "docs/trends-dashboard/index.html",
    "docs/v1.0.0_roadmap.md",
    "docs/v0.9.0_roadmap.md",
    "docs/team_intelligence.md",
    "docs/catalyst_notes_workflow.md",
    "docs/narrative_intelligence.md",
    "docs/releases/v0.9.0.md",
    "docs/releases/v0.8.0.md",
    "data/manual/catalyst_notes.csv",
    "examples/catalyst_notes_sample.csv",
    "src/wcmi/catalyst_notes.py",
    "scripts/validate_catalyst_notes.py",
    "scripts/match_catalyst_notes.py",
    "scripts/generate_team_intelligence.py",
    "scripts/run_historical_trends_workflow.py",
    "scripts/generate_trends_dashboard.py",
]


PYTHON_FILES_TO_COMPILE = [
    "src/wcmi/catalyst_notes.py",
    "scripts/validate_catalyst_notes.py",
    "scripts/match_catalyst_notes.py",
    "scripts/generate_team_intelligence.py",
    "scripts/run_historical_trends_workflow.py",
    "scripts/generate_trends_dashboard.py",
]


GENERATED_OUTPUTS_THAT_SHOULD_BE_IGNORED = [
    "data/processed/snapshot_comparison_latest.csv",
    "data/processed/probability_deltas_latest.csv",
    "data/processed/top_movers_latest.csv",
    "data/processed/signal_summary_latest.csv",
    "data/processed/catalyst_matches_latest.csv",
    "data/processed/team_intelligence_latest.csv",
]


DASHBOARD_CONTENT_CHECKS = {
    "docs/index.html": [
        "World Cup Market Intelligence",
        "Mayior Capital",
    ],
    "docs/dashboard/index.html": [
        "World Cup",
        "Mayior Capital",
    ],
    "docs/polymarket-dashboard/index.html": [
        "Polymarket",
        "Mayior Capital",
    ],
    "docs/trends-dashboard/index.html": [
        "Historical Trends",
        "Team intelligence",
        "Catalyst matches",
        "Mayior Capital",
    ],
}


class ValidationState:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []

    def pass_check(self, message: str) -> None:
        print(f"PASS: {message}")

    def fail_check(self, message: str) -> None:
        print(f"FAIL: {message}")
        self.failures.append(message)

    def warn_check(self, message: str) -> None:
        print(f"WARN: {message}")
        self.warnings.append(message)


def run_command(
    state: ValidationState,
    name: str,
    command: list[str],
    required: bool = True,
) -> None:
    print("")
    print("-" * 80)
    print(name)
    print("-" * 80)
    print(" ".join(command))

    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout.strip():
        print(result.stdout.strip())

    if result.stderr.strip():
        print(result.stderr.strip())

    if result.returncode == 0:
        state.pass_check(name)
        return

    message = f"{name} failed with exit code {result.returncode}"

    if required:
        state.fail_check(message)
    else:
        state.warn_check(message)


def check_required_files(state: ValidationState) -> None:
    print("")
    print("=" * 80)
    print("Checking required files")
    print("=" * 80)

    for relative_path in REQUIRED_FILES:
        path = ROOT / relative_path

        if path.exists():
            state.pass_check(f"Found {relative_path}")
        else:
            state.fail_check(f"Missing {relative_path}")


def compile_python_files(state: ValidationState) -> None:
    print("")
    print("=" * 80)
    print("Compiling Python files")
    print("=" * 80)

    for relative_path in PYTHON_FILES_TO_COMPILE:
        run_command(
            state=state,
            name=f"Compile {relative_path}",
            command=[
                sys.executable,
                "-m",
                "py_compile",
                relative_path,
            ],
            required=True,
        )


def validate_catalyst_notes(state: ValidationState) -> None:
    print("")
    print("=" * 80)
    print("Validating catalyst notes")
    print("=" * 80)

    run_command(
        state=state,
        name="Validate main catalyst notes template",
        command=[
            sys.executable,
            "scripts/validate_catalyst_notes.py",
        ],
        required=True,
    )

    run_command(
        state=state,
        name="Validate catalyst notes sample file",
        command=[
            sys.executable,
            "scripts/validate_catalyst_notes.py",
            "--path",
            "examples/catalyst_notes_sample.csv",
        ],
        required=True,
    )


def validate_provider_registry_if_available(state: ValidationState) -> None:
    print("")
    print("=" * 80)
    print("Checking provider registry validation")
    print("=" * 80)

    provider_validation_script = ROOT / "scripts" / "validate_providers.py"

    if not provider_validation_script.exists():
        state.warn_check("scripts/validate_providers.py not found; provider validation skipped")
        return

    run_command(
        state=state,
        name="Run provider validation",
        command=[
            sys.executable,
            "scripts/validate_providers.py",
        ],
        required=False,
    )


def check_generated_outputs_are_ignored(state: ValidationState) -> None:
    print("")
    print("=" * 80)
    print("Checking Git ignore rules for generated outputs")
    print("=" * 80)

    for relative_path in GENERATED_OUTPUTS_THAT_SHOULD_BE_IGNORED:
        result = subprocess.run(
            [
                "git",
                "check-ignore",
                "-v",
                relative_path,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            output = result.stdout.strip()
            state.pass_check(f"Ignored generated output: {relative_path}")
            if output:
                print(output)
        else:
            state.fail_check(f"Generated output is not ignored by Git: {relative_path}")


def check_dashboard_content(state: ValidationState) -> None:
    print("")
    print("=" * 80)
    print("Checking dashboard content")
    print("=" * 80)

    for relative_path, required_strings in DASHBOARD_CONTENT_CHECKS.items():
        path = ROOT / relative_path

        if not path.exists():
            state.fail_check(f"Dashboard missing: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8", errors="ignore")

        for required_string in required_strings:
            if required_string in content:
                state.pass_check(f"{relative_path} contains: {required_string}")
            else:
                state.fail_check(f"{relative_path} missing: {required_string}")


def check_dashboard_generator_help(state: ValidationState) -> None:
    print("")
    print("=" * 80)
    print("Checking safe command help")
    print("=" * 80)

    run_command(
        state=state,
        name="Team intelligence help",
        command=[
            sys.executable,
            "scripts/generate_team_intelligence.py",
            "--help",
        ],
        required=True,
    )

    run_command(
        state=state,
        name="Historical trends workflow help",
        command=[
            sys.executable,
            "scripts/run_historical_trends_workflow.py",
            "--help",
        ],
        required=True,
    )

    run_command(
        state=state,
        name="Catalyst matching help",
        command=[
            sys.executable,
            "scripts/match_catalyst_notes.py",
            "--help",
        ],
        required=True,
    )


def print_summary(state: ValidationState) -> None:
    print("")
    print("=" * 80)
    print("PROJECT VALIDATION SUMMARY")
    print("=" * 80)

    print(f"Failures: {len(state.failures)}")
    print(f"Warnings: {len(state.warnings)}")

    if state.warnings:
        print("")
        print("Warnings:")
        for warning in state.warnings:
            print(f"- {warning}")

    if state.failures:
        print("")
        print("Failures:")
        for failure in state.failures:
            print(f"- {failure}")

        print("")
        print("Result: FAIL")
        raise SystemExit(1)

    print("")
    print("Result: PASS")
    print("")
    print("The project passed the safe local validation checks.")


def main() -> None:
    print("World Cup Market Intelligence — Project Validation")
    print(f"Root: {ROOT}")
    print("")
    print("This validation is safe:")
    print("- no live API calls")
    print("- no full historical workflow")
    print("- no automated scraping")
    print("- no generated CSV commit required")
    print("")

    state = ValidationState()

    check_required_files(state)
    compile_python_files(state)
    validate_catalyst_notes(state)
    validate_provider_registry_if_available(state)
    check_generated_outputs_are_ignored(state)
    check_dashboard_content(state)
    check_dashboard_generator_help(state)

    print_summary(state)


if __name__ == "__main__":
    main()
