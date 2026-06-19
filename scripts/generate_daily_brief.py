from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: jinja2. Install project dependencies first."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
DEFAULT_TEMPLATE = ROOT / "templates" / "daily_brief.md.j2"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "briefs"

MANUAL_DIR = ROOT / "data" / "manual"
MATCH_SCHEDULE_PATH = MANUAL_DIR / "world_cup_match_schedule.csv"
TEAM_ALIASES_PATH = MANUAL_DIR / "team_aliases.csv"
SNAPSHOT_DIR = PROCESSED_DIR / "snapshots"
SNAPSHOT_PLAN_PATH = PROCESSED_DIR / "snapshot_plan_latest.csv"
WINNER_PREFIX = "Will "
WINNER_SUFFIX = " win the 2026 FIFA World Cup?"


def normalize_key(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict):
        return data

    return {}


def get_field(row: dict[str, Any], aliases: list[str], default: str = "n/a") -> str:
    key_map = {normalize_key(str(key)): key for key in row.keys()}

    for alias in aliases:
        normalized = normalize_key(alias)
        if normalized in key_map:
            value = row.get(key_map[normalized])
            if value is not None and str(value).strip() != "":
                return str(value).strip()

    return default


def parse_number(value: Any) -> float:
    if value is None:
        return 0.0

    text = str(value).replace(",", "").replace("%", "").replace("pp", "")
    match = re.search(r"[-+]?\d*\.?\d+", text)

    if not match:
        return 0.0

    try:
        return float(match.group(0))
    except ValueError:
        return 0.0


def format_list(value: Any) -> str:
    if value is None:
        return "n/a"

    if isinstance(value, list):
        if not value:
            return "none"
        return ", ".join(str(item) for item in value)

    if isinstance(value, dict):
        if not value:
            return "none"
        return ", ".join(f"{key}: {val}" for key, val in value.items())

    text = str(value).strip()
    return text if text else "n/a"


def normalize_market_row(row: dict[str, Any]) -> dict[str, str]:
    team = get_field(
        row,
        [
            "team",
            "team_name",
            "entity",
            "outcome",
            "asset",
            "selection",
            "name",
        ],
    )

    return {
        "team": team,
        "market_title": get_field(
            row,
            [
                "market_title",
                "market",
                "title",
                "question",
                "event",
                "market_name",
            ],
        ),
        "outcome": get_field(
            row,
            [
                "outcome",
                "selection",
                "team",
                "team_name",
                "asset",
                "name",
            ],
        ),
        "current_probability": get_field(
            row,
            [
                "current_probability",
                "current_prob",
                "probability",
                "yes_probability",
                "price",
                "current_price",
                "current",
            ],
        ),
        "previous_probability": get_field(
            row,
            [
                "previous_probability",
                "previous_prob",
                "previous_price",
                "prior_probability",
                "prior_price",
                "previous",
            ],
        ),
        "probability_delta": get_field(
            row,
            [
                "probability_delta",
                "probability_delta_pp",
                "delta_probability",
                "prob_delta",
                "price_delta",
                "probability_change_display",
                "probability_change_pp",
                "probability_change",
                "delta",
                "change",
            ],
        ),
        "current_liquidity": get_field(
            row,
            [
                "current_liquidity",
                "liquidity",
                "current_liquidity_usd",
                "liquidity_usd",
            ],
        ),
        "previous_liquidity": get_field(
            row,
            [
                "previous_liquidity",
                "previous_liquidity_usd",
                "prior_liquidity",
            ],
        ),
        "liquidity_delta": get_field(
            row,
            [
                "liquidity_delta",
                "liquidity_change",
                "delta_liquidity",
                "liquidity_delta_usd",
            ],
        ),
        "current_volume": get_field(
            row,
            [
                "current_volume",
                "volume",
                "current_volume_usd",
                "volume_usd",
            ],
        ),
        "previous_volume": get_field(
            row,
            [
                "previous_volume",
                "previous_volume_usd",
                "prior_volume",
            ],
        ),
        "volume_delta": get_field(
            row,
            [
                "volume_delta",
                "volume_change",
                "delta_volume",
                "volume_delta_usd",
            ],
        ),
        "signal_label": get_field(
            row,
            [
                "signal_label",
                "signal",
                "classification",
                "movement_label",
            ],
        ),
        "review_priority": get_field(
            row,
            [
                "review_priority",
                "priority",
                "manual_review_priority",
                "review",
            ],
        ),
        "source_url": get_field(
            row,
            [
                "source_url",
                "url",
                "market_url",
                "polymarket_url",
            ],
        ),
    }


def normalize_team_row(row: dict[str, Any]) -> dict[str, str]:
    return {
        "team": get_field(row, ["team", "team_name", "entity", "outcome", "name"]),
        "review_priority": get_field(
            row,
            [
                "review_priority",
                "priority",
                "manual_review_priority",
                "review",
            ],
        ),
        "net_signal_score": get_field(
            row,
            [
                "net_signal_score",
                "signal_score",
                "score",
                "net_score",
            ],
        ),
        "positive_signals": get_field(
            row,
            [
                "positive_signals",
                "positive_signal_count",
                "bullish_signals",
            ],
        ),
        "negative_signals": get_field(
            row,
            [
                "negative_signals",
                "negative_signal_count",
                "bearish_signals",
            ],
        ),
        "catalyst_matches": get_field(
            row,
            [
                "catalyst_matches",
                "catalyst_match_count",
                "matched_catalysts",
            ],
        ),
        "notes": get_field(
            row,
            [
                "notes",
                "summary",
                "interpretation",
                "reason",
                "rationale",
            ],
            default="No notes available.",
        ),
    }


def normalize_catalyst_row(row: dict[str, Any]) -> dict[str, str]:
    return {
        "team": get_field(row, ["team", "team_name", "entity", "outcome", "name"]),
        "catalyst_type": get_field(
            row,
            [
                "catalyst_type",
                "type",
                "category",
                "note_type",
            ],
        ),
        "catalyst_note": get_field(
            row,
            [
                "catalyst_note",
                "note",
                "description",
                "catalyst",
                "text",
            ],
        ),
        "market_title": get_field(
            row,
            [
                "market_title",
                "market",
                "title",
                "question",
                "event",
            ],
        ),
        "signal_label": get_field(
            row,
            [
                "signal_label",
                "signal",
                "classification",
                "movement_label",
            ],
        ),
        "review_priority": get_field(
            row,
            [
                "review_priority",
                "priority",
                "manual_review_priority",
                "review",
            ],
        ),
    }


def normalize_signal_row(row: dict[str, Any]) -> dict[str, str]:
    return {
        "signal_label": get_field(
            row,
            [
                "signal_label",
                "signal",
                "classification",
                "movement_label",
            ],
        ),
        "count": get_field(row, ["count", "total", "n", "rows"]),
    }


def sort_rows_by_abs_number(
    rows: list[dict[str, str]],
    field_name: str,
    limit: int,
) -> list[dict[str, str]]:
    """Sort by abs(field), deduplicate by market_id (or team+outcome), return top N.

    top_movers_latest.csv contains multiple categories (top_positive_probability_movers,
    top_negative_probability_movers, top_volume_movers, top_liquidity_movers). The same
    market can appear in several categories, causing duplicates in the brief. We sort
    all rows together and keep only the first occurrence of each unique market.
    """
    sorted_rows = sorted(
        rows,
        key=lambda row: abs(parse_number(row.get(field_name))),
        reverse=True,
    )
    seen: set[str] = set()
    deduped: list[dict[str, str]] = []
    for row in sorted_rows:
        key = str(row.get("market_id", "")).strip()
        if not key or key in ("n/a", ""):
            team = str(row.get("team", "")).strip().lower()
            outcome = str(row.get("outcome", "")).strip().lower()
            key = f"{team}|{outcome}"
        if key not in seen:
            seen.add(key)
            deduped.append(row)
    return deduped[:limit]


def sort_team_priorities(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    priority_rank = {
        "critical": 5,
        "very high": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
        "n/a": 0,
    }

    def score(row: dict[str, str]) -> tuple[int, float]:
        priority = row.get("review_priority", "n/a").lower().strip()
        return (
            priority_rank.get(priority, 0),
            abs(parse_number(row.get("net_signal_score"))),
        )

    return sorted(rows, key=score, reverse=True)[:limit]


def summarize_metadata(metadata: dict[str, Any]) -> dict[str, str]:
    if not metadata:
        return {}

    return {
        "generated_at": str(metadata.get("generated_at", "n/a")),
        "stale_threshold_hours": str(metadata.get("stale_threshold_hours", "n/a")),
        "public_dashboard_status": str(
            metadata.get("public_dashboard_status", metadata.get("status", "n/a"))
        ),
        "dashboards_available": format_list(
            metadata.get(
                "dashboards_available",
                metadata.get("available_dashboards", metadata.get("dashboards", "n/a")),
            )
        ),
        "generated_outputs_available": format_list(
            metadata.get(
                "generated_outputs_available",
                metadata.get("available_outputs", metadata.get("outputs", "n/a")),
            )
        ),
        "missing_outputs": format_list(
            metadata.get(
                "missing_outputs",
                metadata.get("missing_generated_outputs", "n/a"),
            )
        ),
        "stale_outputs": format_list(
            metadata.get(
                "stale_outputs",
                metadata.get("stale_generated_outputs", "n/a"),
            )
        ),
    }


def build_executive_summary(
    top_probability_movers: list[dict[str, str]],
    top_liquidity_movers: list[dict[str, str]],
    top_volume_movers: list[dict[str, str]],
    team_review_priorities: list[dict[str, str]],
    catalyst_watchlist: list[dict[str, str]],
    data_freshness: dict[str, str],
) -> str:
    lines = []

    lines.append(
        "This brief summarizes the latest World Cup market-intelligence outputs generated by the local research pipeline."
    )

    if top_probability_movers:
        first = top_probability_movers[0]
        lines.append(
            f"Top probability movement to review: {first.get('team', 'Unknown team')} "
            f"with change {first.get('probability_delta', 'n/a')}."
        )

    if top_liquidity_movers:
        first = top_liquidity_movers[0]
        lines.append(
            f"Top liquidity movement to review: {first.get('team', 'Unknown team')} "
            f"with change {first.get('liquidity_delta', 'n/a')}."
        )

    if top_volume_movers:
        first = top_volume_movers[0]
        lines.append(
            f"Top volume movement to review: {first.get('team', 'Unknown team')} "
            f"with change {first.get('volume_delta', 'n/a')}."
        )

    if team_review_priorities:
        lines.append(
            f"{len(team_review_priorities)} teams are listed for manual review priority."
        )

    if catalyst_watchlist:
        lines.append(
            f"{len(catalyst_watchlist)} catalyst matches are included in the watchlist."
        )

    if data_freshness:
        lines.append(
            f"Dashboard trust status: {data_freshness.get('public_dashboard_status', 'n/a')}."
        )
    else:
        lines.append("Dashboard trust metadata was not available for this run.")

    lines.append(
        "All interpretation is research-only and should not be treated as betting, investment or financial advice."
    )

    return "\n\n".join(lines)


def collect_warnings(
    missing_files: list[Path],
    metadata: dict[str, Any],
) -> list[str]:
    warnings = []

    for path in missing_files:
        warnings.append(f"Missing optional input file: {path.as_posix()}")

    metadata_warnings = metadata.get("warnings", []) if metadata else []

    if isinstance(metadata_warnings, list):
        warnings.extend(str(item) for item in metadata_warnings)
    elif metadata_warnings:
        warnings.append(str(metadata_warnings))

    if not warnings:
        warnings.append(
            "No major generator warnings. Manual review is still required before interpretation."
        )

    return warnings


def _extract_team_from_title(title: str) -> str:
    t = str(title).strip()
    if t.startswith(WINNER_PREFIX) and t.endswith(WINNER_SUFFIX):
        return t[len(WINNER_PREFIX) : -len(WINNER_SUFFIX)].strip()
    return ""


def _load_aliases() -> dict[str, str]:
    """Return mapping: any_name_lower -> canonical Polymarket team name."""
    mapping: dict[str, str] = {}
    if not TEAM_ALIASES_PATH.exists():
        return mapping
    with TEAM_ALIASES_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            schedule_team = str(row.get("schedule_team", "")).strip()
            market_team = str(row.get("market_team", "")).strip()
            aliases_raw = str(row.get("aliases", "")).strip()
            if not market_team:
                continue
            if schedule_team:
                mapping[schedule_team.lower()] = market_team
            for alias in aliases_raw.split("|"):
                a = alias.strip()
                if a:
                    mapping[a.lower()] = market_team
    return mapping


def _load_market_index() -> dict[str, dict[str, str]]:
    """Return dict: team_name_lower -> market data from latest Polymarket snapshot."""
    candidates = sorted(SNAPSHOT_DIR.glob("*polymarket*.csv"))
    if not candidates:
        return {}
    path = candidates[-1]
    index: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            outcome = str(row.get("outcome", "")).strip().lower()
            if outcome not in ("yes", ""):
                continue
            team = _extract_team_from_title(str(row.get("market_title", "")))
            if not team:
                continue
            index[team.lower()] = {
                "team": team,
                "probability": str(row.get("price", row.get("probability", "n/a"))),
                "probability_delta": str(row.get("price_change_24h", "0.0")),
                "volume": str(row.get("volume", "n/a")),
                "liquidity": str(row.get("liquidity", "n/a")),
            }
    return index


def _resolve_team(
    raw: str,
    aliases: dict[str, str],
    index: dict[str, dict[str, str]],
) -> dict[str, str] | None:
    key = raw.lower()
    if key in index:
        return index[key]
    market_name = aliases.get(key)
    if market_name and market_name.lower() in index:
        return index[market_name.lower()]
    return None


def _fmt_prob(value: str) -> str:
    try:
        return f"{float(value) * 100:.2f}%"
    except (ValueError, TypeError):
        return str(value)


def _fmt_volume(value: str) -> str:
    try:
        v = float(value)
        if v >= 1_000_000:
            return f"${v / 1_000_000:.1f}M"
        if v >= 1_000:
            return f"${v / 1_000:.0f}K"
        return f"${v:.0f}"
    except (ValueError, TypeError):
        return str(value)


# Romania is UTC+3 (EEST) during the World Cup (June-July).
# This fixed offset is valid for the entire tournament window.
_ROMANIA_TZ = timezone(timedelta(hours=3))


def load_snapshot_plan() -> list[dict[str, str]]:
    """Load snapshot_plan_latest.csv and return only upcoming windows.

    Returns an empty list (does not crash) if the file is missing or unreadable.
    The Daily Brief gracefully degrades: it shows 'No snapshot plan generated yet.'
    """
    if not SNAPSHOT_PLAN_PATH.exists():
        return []
    try:
        with SNAPSHOT_PLAN_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
        # Return only upcoming windows; past windows are for audit in the CSV only.
        return [r for r in rows if str(r.get("status", "")).strip() == "upcoming"]
    except Exception:
        return []


def build_match_context(report_date_str: str) -> dict[str, list[dict]]:
    """
    Load schedule + snapshot + aliases. Groups matches by Romania local date.

    'today_ro'    : matches whose kickoff_romania_datetime falls on today Romania date
    'next24h_ro'  : matches whose kickoff_romania_datetime falls on tomorrow Romania date
    'missing_teams': team names with no Polymarket winner market data

    All grouping uses Romania local time (UTC+3). The field kickoff_romania_datetime
    in world_cup_match_schedule.csv is a full datetime (YYYY-MM-DD HH:MM, Romania local).
    """
    if not MATCH_SCHEDULE_PATH.exists():
        return {"today_ro": [], "next24h_ro": [], "missing_teams": []}

    # Determine today and tomorrow in Romania local time
    now_romania = datetime.now(_ROMANIA_TZ)
    today_ro = now_romania.date()
    tomorrow_ro = today_ro + timedelta(days=1)

    aliases = _load_aliases()
    market_index = _load_market_index()

    today_matches: list[dict] = []
    tomorrow_matches: list[dict] = []
    missing_teams: list[str] = []

    with MATCH_SCHEDULE_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            # Parse Romania local datetime (authoritative for grouping)
            ro_dt_str = str(row.get("kickoff_romania_datetime", "")).strip()
            try:
                ro_dt = datetime.strptime(ro_dt_str, "%Y-%m-%d %H:%M")
                ro_date = ro_dt.date()
            except ValueError:
                continue  # skip rows with unparseable datetime

            if ro_date not in (today_ro, tomorrow_ro):
                continue

            home_raw = str(row.get("home_team", "")).strip()
            away_raw = str(row.get("away_team", "")).strip()

            home_data = _resolve_team(home_raw, aliases, market_index)
            away_data = _resolve_team(away_raw, aliases, market_index)

            if not home_data:
                missing_teams.append(home_raw)
            if not away_data:
                missing_teams.append(away_raw)

            major = str(row.get("major_market_impact", "false")).strip().lower()

            entry = {
                "kickoff_romania_datetime": ro_dt_str,
                "kickoff_romania_date": ro_dt.strftime("%Y-%m-%d"),
                "kickoff_romania_time": ro_dt.strftime("%H:%M"),
                "kickoff_utc": str(row.get("kickoff_utc", "")).strip(),
                "home_team": home_raw,
                "away_team": away_raw,
                "group": str(row.get("group", "")).strip() or "--",
                "major_market_impact": major in ("true", "yes", "1"),
                "home_probability": _fmt_prob(home_data["probability"]) if home_data else "n/a",
                "away_probability": _fmt_prob(away_data["probability"]) if away_data else "n/a",
                "home_probability_delta": home_data["probability_delta"] if home_data else "n/a",
                "away_probability_delta": away_data["probability_delta"] if away_data else "n/a",
                "home_volume": _fmt_volume(home_data["volume"]) if home_data else "n/a",
                "away_volume": _fmt_volume(away_data["volume"]) if away_data else "n/a",
                "home_liquidity": _fmt_volume(home_data["liquidity"]) if home_data else "n/a",
                "away_liquidity": _fmt_volume(away_data["liquidity"]) if away_data else "n/a",
                "home_market_found": home_data is not None,
                "away_market_found": away_data is not None,
            }

            if ro_date == today_ro:
                today_matches.append(entry)
            else:
                tomorrow_matches.append(entry)

    return {
        "today_ro": today_matches,
        "next24h_ro": tomorrow_matches,
        "missing_teams": sorted(set(missing_teams)),
    }


def generate_brief(args: argparse.Namespace) -> tuple[Path, Path]:
    top_movers_path = PROCESSED_DIR / "top_movers_latest.csv"
    probability_deltas_path = PROCESSED_DIR / "probability_deltas_latest.csv"
    signal_summary_path = PROCESSED_DIR / "signal_summary_latest.csv"
    catalyst_matches_path = PROCESSED_DIR / "catalyst_matches_latest.csv"
    team_intelligence_path = PROCESSED_DIR / "team_intelligence_latest.csv"
    dashboard_metadata_path = PROCESSED_DIR / "dashboard_metadata_latest.json"

    missing_files = [
        path
        for path in [
            top_movers_path,
            signal_summary_path,
            catalyst_matches_path,
            team_intelligence_path,
            dashboard_metadata_path,
        ]
        if not path.exists()
    ]

    mover_source_rows = read_csv_rows(top_movers_path)

    if not mover_source_rows:
        mover_source_rows = read_csv_rows(probability_deltas_path)
        if probability_deltas_path.exists() and probability_deltas_path not in missing_files:
            pass
        elif not probability_deltas_path.exists():
            missing_files.append(probability_deltas_path)

    normalized_movers = [normalize_market_row(row) for row in mover_source_rows]
    normalized_signals = [
        normalize_signal_row(row) for row in read_csv_rows(signal_summary_path)
    ]
    normalized_catalysts = [
        normalize_catalyst_row(row) for row in read_csv_rows(catalyst_matches_path)
    ]
    normalized_teams = [
        normalize_team_row(row) for row in read_csv_rows(team_intelligence_path)
    ]

    # Enrich movers with signal_label (from signal_summary raw rows) and
    # review_priority (from team_intelligence raw rows). These fields are absent
    # from top_movers_latest.csv. normalize_signal_row aggregates counts only.
    _signal_by_team: dict[str, str] = {}
    for _raw in read_csv_rows(signal_summary_path):
        _t = str(_raw.get("team", "")).strip().lower()
        _lbl = str(_raw.get("signal_label", "")).strip()
        if _t and _lbl:
            _signal_by_team.setdefault(_t, _lbl)

    _priority_by_team: dict[str, str] = {}
    for _raw in read_csv_rows(team_intelligence_path):
        _t = str(_raw.get("team", "")).strip().lower()
        _pri = str(_raw.get("review_priority", "")).strip()
        if _t and _pri:
            _priority_by_team[_t] = _pri

    _MISSING = {"n/a", "", "none", "null"}
    for _mover in normalized_movers:
        _key = str(_mover.get("team", "")).strip().lower()
        if str(_mover.get("signal_label", "n/a")).lower() in _MISSING and _key in _signal_by_team:
            _mover["signal_label"] = _signal_by_team[_key]
        if str(_mover.get("review_priority", "n/a")).lower() in _MISSING and _key in _priority_by_team:
            _mover["review_priority"] = _priority_by_team[_key]

    metadata = read_json(dashboard_metadata_path)
    data_freshness = summarize_metadata(metadata)

    top_probability_movers = sort_rows_by_abs_number(
        normalized_movers,
        "probability_delta",
        args.limit,
    )
    top_liquidity_movers = sort_rows_by_abs_number(
        normalized_movers,
        "liquidity_delta",
        args.limit,
    )
    top_volume_movers = sort_rows_by_abs_number(
        normalized_movers,
        "volume_delta",
        args.limit,
    )
    team_review_priorities = sort_team_priorities(normalized_teams, args.limit)
    catalyst_watchlist = normalized_catalysts[: args.limit]

    report_date = args.report_date or datetime.now(timezone.utc).date().isoformat()
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    match_context = build_match_context(report_date)
    snapshot_windows = load_snapshot_plan()

    context = {
        "report_date": report_date,
        "generated_at": generated_at,
        "product_name": "World Cup Market Intelligence Daily Brief",
        "executive_summary": build_executive_summary(
            top_probability_movers,
            top_liquidity_movers,
            top_volume_movers,
            team_review_priorities,
            catalyst_watchlist,
            data_freshness,
        ),
        "top_probability_movers": top_probability_movers,
        "top_liquidity_movers": top_liquidity_movers,
        "top_volume_movers": top_volume_movers,
        "team_review_priorities": team_review_priorities,
        "catalyst_watchlist": catalyst_watchlist,
        "signal_summary": normalized_signals,
        "data_freshness": data_freshness,
        "warnings": collect_warnings(missing_files, metadata),
        "match_context_today": match_context["today_ro"],
        "match_context_next24h": match_context["next24h_ro"],
        "match_context_missing_teams": match_context["missing_teams"],
        "snapshot_windows": snapshot_windows,
    }

    template_path = Path(args.template)
    output_dir = Path(args.output_dir)

    if not template_path.is_absolute():
        template_path = ROOT / template_path

    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    output_dir.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_path.name)
    rendered = template.render(**context)

    dated_output = output_dir / f"{report_date}.md"
    latest_output = output_dir / "latest.md"

    dated_output.write_text(rendered, encoding="utf-8")
    latest_output.write_text(rendered, encoding="utf-8")

    return dated_output, latest_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate World Cup Market Intelligence daily brief."
    )

    parser.add_argument(
        "--template",
        default=str(DEFAULT_TEMPLATE),
        help="Path to the Jinja daily brief template.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where brief files are written.",
    )
    parser.add_argument(
        "--report-date",
        default=None,
        help="Report date in YYYY-MM-DD format. Defaults to current UTC date.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of rows to include in each section.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dated_output, latest_output = generate_brief(args)

    print(f"Daily brief generated:")
    print(f"  Dated:  {dated_output}")
    print(f"  Latest: {latest_output}")


if __name__ == "__main__":
    main()
