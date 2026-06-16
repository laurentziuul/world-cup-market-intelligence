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
    "Public MVP docs": "docs/public_mvp.md",
    "Documentation map": "docs/documentation_map.md",
    "v1.1.0 roadmap": "docs/v1.1.0_roadmap.md",
    "v1.0.0 roadmap": "docs/v1.0.0_roadmap.md",
    "v0.9.0 roadmap": "docs/v0.9.0_roadmap.md",
    "v1.0.0 release notes": "docs/releases/v1.0.0.md",
    "v0.9.0 release notes": "docs/releases/v0.9.0.md",
    "v0.8.0 release notes": "docs/releases/v0.8.0.md",
    "Team intelligence docs": "docs/team_intelligence.md",
    "Catalyst workflow docs": "docs/catalyst_notes_workflow.md",
    "Narrative intelligence docs": "docs/narrative_intelligence.md",
    "Historical trends workflow docs": "docs/historical_trends_workflow.md",
    "Provider docs": "docs/providers.md",
    "Provider status docs": "docs/provider_status.md",
}


GENERATED_OUTPUTS = {
    "Snapshot comparison": "data/processed/snapshot_comparison_latest.csv",
    "Probability deltas": "data/processed/probability_deltas_latest.csv",
    "Top movers": "data/processed/top_movers_latest.csv",
    "Signal summary": "data/processed/signal_summary_latest.csv",
    "Catalyst matches": "data/processed/catalyst_matches_latest.csv",
    "Team intelligence": "data/processed/team_intelligence_latest.csv",
    "Dashboard metadata": "data/processed/dashboard_metadata_latest.json",
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


PROVIDER_CLASSIFICATION = {
    "manual_csv": "stable",
    "polymarket": "experimental",
    "predict_fun": "experimental",
    "kalshi": "experimental",
    "manifold": "experimental",
}


PROVIDER_DESCRIPTIONS = {
    "manual_csv": "Offline manual CSV provider. Reproducible baseline.",
    "polymarket": "Experimental live provider for Polymarket-style market data.",
    "predict_fun": "Experimental provider placeholder / integration surface.",
    "kalshi": "Experimental provider placeholder / integration surface.",
    "manifold": "Experimental provider placeholder / integration surface.",
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


def list_provider_files() -> list[str]:
    providers_dir = ROOT / "src" / "wcmi" / "providers"

    if not providers_dir.exists():
        return []

    excluded = {
        "__init__",
        "base",
        "registry",
    }

    providers = []

    for path in providers_dir.glob("*.py"):
        name = path.stem

        if name in excluded:
            continue

        providers.append(name)

    return sorted(providers)


def provider_file_path(provider: str) -> str:
    return f"src/wcmi/providers/{provider}.py"


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


def run_provider_validation() -> tuple[int, str, str]:
    script_path = ROOT / "scripts" / "validate_providers.py"

    if not script_path.exists():
        return 999, "", "scripts/validate_providers.py not found"

    result = subprocess.run(
        [
            "python",
            "scripts/validate_providers.py",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    return result.returncode, result.stdout.strip(), result.stderr.strip()


def print_provider_health_summary() -> None:
    print_section("Provider health summary")

    providers = list_provider_files()

    if not providers:
        print("WARN  No provider files found in src/wcmi/providers")
        return

    stable_providers = []
    experimental_providers = []

    for provider in providers:
        classification = PROVIDER_CLASSIFICATION.get(provider, "experimental")
        description = PROVIDER_DESCRIPTIONS.get(provider, "No description available.")
        relative_path = provider_file_path(provider)
        status = "available" if exists(relative_path) else "missing"

        if classification == "stable":
            stable_providers.append(provider)
        else:
            experimental_providers.append(provider)

        prefix = "PASS" if status == "available" else "WARN"

        print(
            f"{prefix}  {provider:<18} {classification:<14} {status:<10} {relative_path}"
        )
        print(f"      {description}")

    print("")
    print("Provider summary:")
    print(f"- Stable providers: {len(stable_providers)}")
    print(f"- Experimental providers: {len(experimental_providers)}")

    if stable_providers:
        print(f"- Stable: {', '.join(stable_providers)}")

    if experimental_providers:
        print(f"- Experimental: {', '.join(experimental_providers)}")

    print("")
    print("Provider docs:")

    provider_docs = {
        "Provider overview": "docs/providers.md",
        "Provider status": "docs/provider_status.md",
        "API provider strategy": "docs/api_provider_strategy.md",
        "Provider failure modes": "docs/provider_failure_modes.md",
        "Polymarket troubleshooting": "docs/polymarket_troubleshooting.md",
    }

    for label, relative_path in provider_docs.items():
        print_status(label, relative_path)

    print("")
    print("Provider validation:")

    code, stdout, stderr = run_provider_validation()

    if code == 0:
        print("PASS  scripts/validate_providers.py completed successfully")
    elif code == 999:
        print("WARN  Provider validation skipped")
    else:
        print(f"WARN  Provider validation returned exit code {code}")

    if stdout:
        print("")
        print(stdout)

    if stderr:
        print("")
        print(stderr)

    print("")
    print("Live provider caution:")
    print("- manual_csv is the stable reproducible baseline.")
    print("- live providers are experimental and may fail because of API, network, schema or availability changes.")
    print("- public dashboards should not overclaim live-provider reliability.")


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
    print("- Freshness and metadata reports improve trust, but do not make stale data predictive.")
    print("")
    print("Research-only position:")
    print("- This project is not betting advice.")
    print("- This project is not investment advice.")
    print("- This project is not a black-box prediction engine.")


def main() -> None:
    print("World Cup Market Intelligence — Project Health Report")
    print(f"Root: {ROOT}")

    print_provider_health_summary()
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
