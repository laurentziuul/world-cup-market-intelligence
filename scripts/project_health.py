from __future__ import annotations

import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DASHBOARDS = {
    "Landing page": "docs/index.html",
    "Stable dashboard": "docs/dashboard/index.html",
    "Polymarket dashboard": "docs/polymarket-dashboard/index.html",
    "Trends dashboard": "docs/trends-dashboard/index.html",
}


CORE_DOCS = {
    "README": "README.md",
    "v1.0.0 roadmap": "docs/v1.0.0_roadmap.md",
    "v0.9.0 roadmap": "docs/v0.9.0_roadmap.md",
    "v0.8.0 release notes": "docs/releases/v0.8.0.md",
    "v0.9.0 release notes": "docs/releases/v0.9.0.md",
    "Team intelligence docs": "docs/team_intelligence.md",
    "Catalyst workflow docs": "docs/catalyst_notes_workflow.md",
    "Narrative intelligence docs": "docs/narrative_intelligence.md",
    "Historical trends workflow docs": "docs/historical_trends_workflow.md",
}


GENERATED_OUTPUTS = {
    "Snapshot comparison": "data/processed/snapshot_comparison_latest.csv",
    "Probability deltas": "data/processed/probability_deltas_latest.csv",
    "Top movers": "data/processed/top_movers_latest.csv",
    "Signal summary": "data/processed/signal_summary_latest.csv",
    "Catalyst matches": "data/processed/catalyst_matches_latest.csv",
    "Team intelligence": "data/processed/team_intelligence_latest.csv",
}


MANUAL_INPUTS = {
    "Manual market CSV": "data/manual/world_cup_markets.csv",
    "Catalyst notes": "data/manual/catalyst_notes.csv",
    "Catalyst sample": "examples/catalyst_notes_sample.csv",
}


PUBLIC_URLS = {
    "Landing page": "https://laurentziuul.github.io/world-cup-market-intelligence/",
    "Stable dashboard": "https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/",
    "Polymarket dashboard": "https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/",
    "Trends dashboard": "https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/",
}


def exists(relative_path: str) -> bool:
    return (ROOT / relative_path).exists()


def file_size(relative_path: str) -> int:
    path = ROOT / relative_path

    if not path.exists():
        return 0

    return path.stat().st_size


def count_csv_rows(relative_path: str) -> int | None:
    path = ROOT / relative_path

    if not path.exists():
        return None

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            return sum(1 for _ in reader)
    except Exception:
        return None


def print_section(title: str) -> None:
    print("")
    print("=" * 80)
    print(title)
    print("=" * 80)


def print_status(label: str, relative_path: str) -> None:
    status = "available" if exists(relative_path) else "missing"
    size = file_size(relative_path)

    if status == "available":
        print(f"PASS  {label:<32} {status:<10} {relative_path} ({size} bytes)")
    else:
        print(f"WARN  {label:<32} {status:<10} {relative_path}")


def list_providers() -> list[str]:
    providers_dir = ROOT / "src" / "wcmi" / "providers"

    if not providers_dir.exists():
        return []

    excluded = {
        "__init__",
        "base",
    }

    providers = []

    for path in providers_dir.glob("*.py"):
        name = path.stem

        if name in excluded:
            continue

        providers.append(name)

    return sorted(providers)


def check_git_ignored(relative_path: str) -> bool:
    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-q",
            relative_path,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    return result.returncode == 0


def git_status_short() -> str:
    result = subprocess.run(
        [
            "git",
            "status",
            "--short",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    return result.stdout.strip()


def print_provider_status() -> None:
    print_section("Providers")

    providers = list_providers()

    if not providers:
        print("WARN  No providers found")
        return

    for provider in providers:
        print(f"PASS  provider available: {provider}")


def print_dashboard_status() -> None:
    print_section("Dashboards")

    for label, relative_path in DASHBOARDS.items():
        print_status(label, relative_path)


def print_documentation_status() -> None:
    print_section("Documentation")

    for label, relative_path in CORE_DOCS.items():
        print_status(label, relative_path)


def print_manual_input_status() -> None:
    print_section("Manual inputs")

    for label, relative_path in MANUAL_INPUTS.items():
        print_status(label, relative_path)

        row_count = count_csv_rows(relative_path)

        if row_count is not None:
            print(f"      rows: {row_count}")


def print_generated_output_status() -> None:
    print_section("Generated outputs")

    for label, relative_path in GENERATED_OUTPUTS.items():
        print_status(label, relative_path)

        row_count = count_csv_rows(relative_path)

        if row_count is not None:
            print(f"      rows: {row_count}")

        ignored = check_git_ignored(relative_path)
        ignored_status = "ignored by Git" if ignored else "NOT ignored by Git"
        prefix = "PASS" if ignored else "WARN"
        print(f"{prefix}  {label:<32} {ignored_status}")


def print_public_urls() -> None:
    print_section("Public URLs")

    for label, url in PUBLIC_URLS.items():
        print(f"INFO  {label:<32} {url}")


def print_git_status() -> None:
    print_section("Git status")

    status = git_status_short()

    if not status:
        print("PASS  working tree clean")
        return

    print("WARN  working tree has changes:")
    print(status)


def print_interpretation() -> None:
    print_section("Interpretation")

    print("Stable layer:")
    print("- manual_csv dashboard is the reproducible offline layer.")
    print("")
    print("Experimental layers:")
    print("- Polymarket dashboard depends on live/provider data.")
    print("- Historical trends depend on multiple snapshots.")
    print("- Catalyst notes and team intelligence are manual-first research layers.")
    print("")
    print("Research-only position:")
    print("- This project is not betting advice.")
    print("- This project is not investment advice.")
    print("- This project is not a black-box prediction engine.")


def main() -> None:
    print("World Cup Market Intelligence — Project Health Report")
    print(f"Root: {ROOT}")

    print_provider_status()
    print_dashboard_status()
    print_documentation_status()
    print_manual_input_status()
    print_generated_output_status()
    print_public_urls()
    print_git_status()
    print_interpretation()

    print("")
    print("=" * 80)
    print("Project health report complete")
    print("=" * 80)


if __name__ == "__main__":
    main()
