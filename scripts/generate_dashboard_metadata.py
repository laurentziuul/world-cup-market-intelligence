from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "dashboard_metadata_latest.json"


DASHBOARDS = {
    "landing_page": "docs/index.html",
    "stable_dashboard": "docs/dashboard/index.html",
    "polymarket_dashboard": "docs/polymarket-dashboard/index.html",
    "trends_dashboard": "docs/trends-dashboard/index.html",
}


GENERATED_OUTPUTS = {
    "snapshot_comparison": "data/processed/snapshot_comparison_latest.csv",
    "probability_deltas": "data/processed/probability_deltas_latest.csv",
    "top_movers": "data/processed/top_movers_latest.csv",
    "signal_summary": "data/processed/signal_summary_latest.csv",
    "catalyst_matches": "data/processed/catalyst_matches_latest.csv",
    "team_intelligence": "data/processed/team_intelligence_latest.csv",
}


MANUAL_INPUTS = {
    "manual_market_csv": "data/manual/world_cup_markets.csv",
    "catalyst_notes": "data/manual/catalyst_notes.csv",
    "catalyst_sample": "examples/catalyst_notes_sample.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate dashboard metadata for freshness and trust status.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output metadata JSON path.",
    )
    parser.add_argument(
        "--stale-hours",
        type=float,
        default=72.0,
        help="Files older than this number of hours are marked stale.",
    )
    return parser.parse_args()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_utc(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def inspect_file(relative_path: str, stale_hours: float) -> dict[str, object]:
    path = ROOT / relative_path

    if not path.exists():
        return {
            "path": relative_path,
            "available": False,
            "status": "missing",
            "size_bytes": 0,
            "modified_at": "",
            "age_hours": None,
        }

    modified_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    age_hours = (utc_now() - modified_at).total_seconds() / 3600
    status = "fresh" if age_hours <= stale_hours else "stale"

    return {
        "path": relative_path,
        "available": True,
        "status": status,
        "size_bytes": path.stat().st_size,
        "modified_at": isoformat_utc(modified_at),
        "age_hours": round(age_hours, 2),
    }


def inspect_group(paths: dict[str, str], stale_hours: float) -> dict[str, dict[str, object]]:
    return {
        name: inspect_file(relative_path=relative_path, stale_hours=stale_hours)
        for name, relative_path in paths.items()
    }


def available_count(group: dict[str, dict[str, object]]) -> int:
    return sum(1 for item in group.values() if bool(item["available"]))


def stale_items(group: dict[str, dict[str, object]]) -> list[str]:
    return [
        name
        for name, item in group.items()
        if item["status"] == "stale"
    ]


def missing_items(group: dict[str, dict[str, object]]) -> list[str]:
    return [
        name
        for name, item in group.items()
        if item["status"] == "missing"
    ]


def build_warnings(
    dashboards: dict[str, dict[str, object]],
    generated_outputs: dict[str, dict[str, object]],
    manual_inputs: dict[str, dict[str, object]],
) -> list[str]:
    warnings = []

    missing_dashboards = missing_items(dashboards)
    stale_dashboards = stale_items(dashboards)
    missing_outputs = missing_items(generated_outputs)
    stale_outputs = stale_items(generated_outputs)
    missing_manual_inputs = missing_items(manual_inputs)

    if missing_dashboards:
        warnings.append(
            "Missing dashboard HTML files: " + ", ".join(missing_dashboards)
        )

    if stale_dashboards:
        warnings.append(
            "Stale dashboard HTML files: " + ", ".join(stale_dashboards)
        )

    if missing_outputs:
        warnings.append(
            "Missing generated outputs: " + ", ".join(missing_outputs)
        )

    if stale_outputs:
        warnings.append(
            "Stale generated outputs: " + ", ".join(stale_outputs)
        )

    if missing_manual_inputs:
        warnings.append(
            "Missing manual inputs: " + ", ".join(missing_manual_inputs)
        )

    return warnings


def build_metadata(stale_hours: float) -> dict[str, object]:
    dashboards = inspect_group(DASHBOARDS, stale_hours=stale_hours)
    generated_outputs = inspect_group(GENERATED_OUTPUTS, stale_hours=stale_hours)
    manual_inputs = inspect_group(MANUAL_INPUTS, stale_hours=stale_hours)

    trend_output_keys = [
        "snapshot_comparison",
        "probability_deltas",
        "top_movers",
        "signal_summary",
    ]

    trend_outputs_available = all(
        bool(generated_outputs[key]["available"])
        for key in trend_output_keys
    )

    catalyst_outputs_available = bool(
        generated_outputs["catalyst_matches"]["available"]
    )

    team_intelligence_available = bool(
        generated_outputs["team_intelligence"]["available"]
    )

    warnings = build_warnings(
        dashboards=dashboards,
        generated_outputs=generated_outputs,
        manual_inputs=manual_inputs,
    )

    public_dashboard_status = "ready"

    if missing_items(dashboards):
        public_dashboard_status = "incomplete"
    elif stale_items(dashboards):
        public_dashboard_status = "stale"

    # Trends data freshness — reflects only generated CSV outputs, not HTML page ages.
    # Used by the trends dashboard summary card to avoid showing "stale" when only
    # auxiliary HTML pages (landing page, stable dashboard) are old.
    trend_output_statuses = [
        generated_outputs[key]["status"]
        for key in trend_output_keys
        if bool(generated_outputs[key]["available"])
    ]
    missing_trend_outputs = [
        key for key in trend_output_keys
        if not bool(generated_outputs[key]["available"])
    ]
    if missing_trend_outputs:
        trends_data_status = "missing"
    elif all(s == "fresh" for s in trend_output_statuses):
        trends_data_status = "fresh"
    elif any(s == "stale" for s in trend_output_statuses):
        trends_data_status = "stale"
    else:
        trends_data_status = "unknown"

    # Auxiliary pages stale — dashboard HTML files excluding trends_dashboard itself.
    auxiliary_dashboard_keys = [k for k in DASHBOARDS if k != "trends_dashboard"]
    auxiliary_pages_stale = [
        k for k in auxiliary_dashboard_keys
        if dashboards[k]["status"] in ("stale", "missing")
    ]

    return {
        "generated_at": isoformat_utc(utc_now()),
        "stale_threshold_hours": stale_hours,
        "public_dashboard_status": public_dashboard_status,
        "stable_dashboard_available": bool(dashboards["stable_dashboard"]["available"]),
        "polymarket_dashboard_available": bool(dashboards["polymarket_dashboard"]["available"]),
        "trends_dashboard_available": bool(dashboards["trends_dashboard"]["available"]),
        "trend_outputs_available": trend_outputs_available,
        "catalyst_outputs_available": catalyst_outputs_available,
        "team_intelligence_available": team_intelligence_available,
        "dashboard_count": len(dashboards),
        "dashboard_available_count": available_count(dashboards),
        "generated_output_count": len(generated_outputs),
        "generated_output_available_count": available_count(generated_outputs),
        "manual_input_count": len(manual_inputs),
        "manual_input_available_count": available_count(manual_inputs),
        "trends_data_status": trends_data_status,
        "auxiliary_pages_stale": auxiliary_pages_stale,
        "stale_dashboards": stale_items(dashboards),
        "missing_dashboards": missing_items(dashboards),
        "stale_outputs": stale_items(generated_outputs),
        "missing_outputs": missing_items(generated_outputs),
        "warnings": warnings,
        "dashboards": dashboards,
        "generated_outputs": generated_outputs,
        "manual_inputs": manual_inputs,
        "interpretation": {
            "research_only": True,
            "not_betting_advice": True,
            "not_investment_advice": True,
            "live_provider_layers_are_experimental": True,
            "missing_generated_outputs_can_be_normal": True,
        },
        "powered_by": "Mayior Capital",
    }


def main() -> None:
    args = parse_args()

    output_path = Path(args.output)
    metadata = build_metadata(stale_hours=float(args.stale_hours))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print("Dashboard metadata")
    print(f"Output: {output_path}")
    print(f"Generated at: {metadata['generated_at']}")
    print(f"Public dashboard status: {metadata['public_dashboard_status']}")
    print(f"Dashboards available: {metadata['dashboard_available_count']}/{metadata['dashboard_count']}")
    print(f"Generated outputs available: {metadata['generated_output_available_count']}/{metadata['generated_output_count']}")
    print(f"Warnings: {len(metadata['warnings'])}")

    for warning in metadata["warnings"]:
        print(f"- {warning}")

    print("Result: PASS")


if __name__ == "__main__":
    main()
