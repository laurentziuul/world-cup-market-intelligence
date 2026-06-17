from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SCHEDULE = ROOT / "data" / "manual" / "world_cup_match_schedule.csv"
DEFAULT_ALIASES = ROOT / "data" / "manual" / "team_aliases.csv"
DEFAULT_SNAPSHOT_DIR = ROOT / "data" / "processed" / "snapshots"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "match_context_latest.csv"

WINNER_PREFIX = "Will "
WINNER_SUFFIX = " win the 2026 FIFA World Cup?"

OUTPUT_FIELDS = [
    "kickoff_romania_datetime",
    "kickoff_romania_date",
    "kickoff_romania_time",
    "kickoff_utc",
    "home_team",
    "away_team",
    "group",
    "stage",
    "major_market_impact",
    "home_probability",
    "away_probability",
    "home_probability_delta",
    "away_probability_delta",
    "home_volume",
    "away_volume",
    "home_liquidity",
    "away_liquidity",
    "home_market_found",
    "away_market_found",
    "review_note",
]

# Romania is UTC+3 (EEST) for the duration of the 2026 World Cup (June-July).
_ROMANIA_TZ = timezone(timedelta(hours=3))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def load_aliases(path: Path) -> dict[str, str]:
    """Return mapping: name_lower -> market_team (canonical Polymarket name)."""
    rows = read_csv_rows(path)
    mapping: dict[str, str] = {}
    for row in rows:
        schedule_team = str(row.get("schedule_team", "")).strip()
        market_team = str(row.get("market_team", "")).strip()
        aliases_raw = str(row.get("aliases", "")).strip()
        if not market_team:
            continue
        if schedule_team:
            mapping[schedule_team.lower()] = market_team
        if aliases_raw:
            for alias in aliases_raw.split("|"):
                alias = alias.strip()
                if alias:
                    mapping[alias.lower()] = market_team
    return mapping


def find_latest_polymarket_snapshot(snapshot_dir: Path) -> Path | None:
    candidates = sorted(snapshot_dir.glob("*polymarket*.csv"))
    return candidates[-1] if candidates else None


def extract_team_from_title(market_title: str) -> str:
    title = str(market_title).strip()
    if title.startswith(WINNER_PREFIX) and title.endswith(WINNER_SUFFIX):
        return title[len(WINNER_PREFIX) : -len(WINNER_SUFFIX)].strip()
    return ""


def load_market_index(snapshot_path: Path) -> dict[str, dict[str, str]]:
    """Return dict: team_name_lower -> {probability, probability_delta, volume, liquidity}."""
    rows = read_csv_rows(snapshot_path)
    index: dict[str, dict[str, str]] = {}
    for row in rows:
        outcome = str(row.get("outcome", "")).strip().lower()
        if outcome not in ("yes", ""):
            continue
        title = str(row.get("market_title", "")).strip()
        team = extract_team_from_title(title)
        if not team:
            continue
        index[team.lower()] = {
            "probability": str(row.get("price", row.get("probability", "n/a"))),
            "probability_delta": str(row.get("price_change_24h", "0.0")),
            "volume": str(row.get("volume", "n/a")),
            "liquidity": str(row.get("liquidity", "n/a")),
        }
    return index


def resolve_team(
    raw_name: str,
    aliases: dict[str, str],
    market_index: dict[str, dict[str, str]],
) -> tuple[str, dict[str, str] | None]:
    """Return (resolved_display_name, data_or_None)."""
    key = raw_name.lower()

    # Direct hit (schedule name matches Polymarket name exactly)
    if key in market_index:
        return raw_name, market_index[key]

    # Alias lookup
    market_name = aliases.get(key)
    if market_name:
        if market_name.lower() in market_index:
            return market_name, market_index[market_name.lower()]

    return raw_name, None


def fmt_prob(value: str) -> str:
    try:
        return f"{float(value) * 100:.2f}%"
    except (ValueError, TypeError):
        return value


def build_review_note(
    home_found: bool,
    away_found: bool,
    home_team: str,
    away_team: str,
    major: str,
) -> str:
    if not home_found and not away_found:
        return f"No market data for {home_team} or {away_team}. Check team names or aliases."
    if not home_found:
        return f"Market data missing for {home_team}. Add to team_aliases.csv."
    if not away_found:
        return f"Market data missing for {away_team}. Add to team_aliases.csv."
    if major.strip().lower() in ("true", "yes", "1"):
        return "Major market impact match. Review probability and volume."
    return "No actionable market movement detected."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate match context by joining the World Cup match schedule "
            "with the latest Polymarket snapshot and team aliases. "
            "Output: data/processed/match_context_latest.csv"
        )
    )
    parser.add_argument("--schedule", default=str(DEFAULT_SCHEDULE))
    parser.add_argument("--aliases", default=str(DEFAULT_ALIASES))
    parser.add_argument("--snapshot-dir", default=str(DEFAULT_SNAPSHOT_DIR))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        "--lookahead-days",
        type=int,
        default=7,
        help="Number of calendar days ahead to include (default 7).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print results without writing output file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    schedule_path = Path(args.schedule)
    aliases_path = Path(args.aliases)
    snapshot_dir = Path(args.snapshot_dir)
    output_path = Path(args.output)

    if not schedule_path.exists():
        raise SystemExit(f"Schedule file not found: {schedule_path}")

    aliases = load_aliases(aliases_path) if aliases_path.exists() else {}
    print(f"Aliases loaded: {len(aliases)} entries")

    snapshot_path = find_latest_polymarket_snapshot(snapshot_dir)
    market_index: dict[str, dict[str, str]] = {}
    if snapshot_path:
        market_index = load_market_index(snapshot_path)
        print(f"Snapshot loaded: {snapshot_path.name} ({len(market_index)} winner markets)")
    else:
        print("WARNING: No Polymarket snapshot found. All market data will be missing.")

    schedule_rows = read_csv_rows(schedule_path)
    print(f"Schedule loaded: {len(schedule_rows)} matches")

    # Lookahead window is based on Romania local date (UTC+3)
    now_romania = datetime.now(_ROMANIA_TZ)
    today_ro = now_romania.date()
    cutoff_ro = today_ro + timedelta(days=args.lookahead_days)

    output_rows: list[dict[str, str]] = []
    missing_teams: list[str] = []

    for row in schedule_rows:
        ro_dt_str = str(row.get("kickoff_romania_datetime", "")).strip()

        try:
            ro_dt = datetime.strptime(ro_dt_str, "%Y-%m-%d %H:%M")
            ro_date = ro_dt.date()
        except ValueError:
            continue  # skip malformed rows

        if ro_date < today_ro or ro_date > cutoff_ro:
            continue  # outside lookahead window

        home_raw = str(row.get("home_team", "")).strip()
        away_raw = str(row.get("away_team", "")).strip()

        home_display, home_data = resolve_team(home_raw, aliases, market_index)
        away_display, away_data = resolve_team(away_raw, aliases, market_index)

        home_found = home_data is not None
        away_found = away_data is not None

        if not home_found:
            missing_teams.append(home_raw)
        if not away_found:
            missing_teams.append(away_raw)

        major = str(row.get("major_market_impact", "false")).strip()

        output_rows.append(
            {
                "kickoff_romania_datetime": ro_dt_str,
                "kickoff_romania_date": ro_dt.strftime("%Y-%m-%d"),
                "kickoff_romania_time": ro_dt.strftime("%H:%M"),
                "kickoff_utc": str(row.get("kickoff_utc", "")).strip(),
                "home_team": home_raw,
                "away_team": away_raw,
                "group": str(row.get("group", "")).strip(),
                "stage": str(row.get("stage", "")).strip(),
                "major_market_impact": major,
                "home_probability": home_data["probability"] if home_data else "n/a",
                "away_probability": away_data["probability"] if away_data else "n/a",
                "home_probability_delta": home_data["probability_delta"] if home_data else "n/a",
                "away_probability_delta": away_data["probability_delta"] if away_data else "n/a",
                "home_volume": home_data["volume"] if home_data else "n/a",
                "away_volume": away_data["volume"] if away_data else "n/a",
                "home_liquidity": home_data["liquidity"] if home_data else "n/a",
                "away_liquidity": away_data["liquidity"] if away_data else "n/a",
                "home_market_found": "yes" if home_found else "no",
                "away_market_found": "yes" if away_found else "no",
                "review_note": build_review_note(
                    home_found, away_found, home_raw, away_raw, major
                ),
            }
        )

    unique_missing = sorted(set(missing_teams))

    if args.dry_run:
        print(f"\nDry run: {len(output_rows)} matches in window")
        for r in output_rows:
            status = (
                "OK"
                if r["home_market_found"] == "yes" and r["away_market_found"] == "yes"
                else "MISSING"
            )
            print(
                f"  [{status}] {r['kickoff_romania_datetime']} Romania  "
                f"({r['kickoff_utc']} UTC)  "
                f"{r['home_team']} ({r['home_probability']}) vs "
                f"{r['away_team']} ({r['away_probability']})"
            )
        if unique_missing:
            print(f"\nTeams with missing market data: {', '.join(unique_missing)}")
        else:
            print("\nAll teams matched to Polymarket data.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nMatch context written: {output_path}")
    print(f"Matches: {len(output_rows)}")
    if unique_missing:
        print(f"Teams missing market data ({len(unique_missing)}): {', '.join(unique_missing)}")
    else:
        print("All teams matched to Polymarket data.")


if __name__ == "__main__":
    main()
