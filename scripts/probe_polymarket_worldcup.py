from __future__ import annotations

import csv
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data" / "raw" / "polymarket"
PROBE_DIR = ROOT / "data" / "processed" / "polymarket"

BASE_MARKETS_URL = "https://gamma-api.polymarket.com/markets"

LIMIT_PER_REQUEST = 100
MAX_PAGES = 10


WORLD_CUP_KEYWORDS = [
    "world cup",
    "fifa world cup",
    "fifa",
    "2026 world cup",
    "world cup 2026",
    "2026 fifa",
]

CONTEXT_KEYWORDS = [
    "soccer",
    "football",
    "qualify",
    "qualification",
    "champion",
    "winner",
    "group",
    "group winner",
    "golden boot",
    "final",
    "semifinal",
]

TEAM_ALIASES = {
    "Mexico": ["mexico"],
    "South Africa": ["south africa"],
    "South Korea": ["south korea", "korea republic"],
    "Czechia": ["czechia", "czech republic"],
    "Canada": ["canada"],
    "Bosnia and Herzegovina": ["bosnia", "bosnia and herzegovina"],
    "Qatar": ["qatar"],
    "Switzerland": ["switzerland", "swiss"],
    "Brazil": ["brazil"],
    "Morocco": ["morocco"],
    "Haiti": ["haiti"],
    "Scotland": ["scotland"],
    "United States": ["united states", "usa", "usmnt"],
    "Paraguay": ["paraguay"],
    "Australia": ["australia"],
    "Turkey": ["turkey", "turkiye", "türkiye"],
    "Germany": ["germany"],
    "Curacao": ["curacao", "curaçao"],
    "Ivory Coast": ["ivory coast", "cote d'ivoire", "côte d'ivoire"],
    "Ecuador": ["ecuador"],
    "Netherlands": ["netherlands", "holland"],
    "Japan": ["japan"],
    "Sweden": ["sweden"],
    "Tunisia": ["tunisia"],
    "Belgium": ["belgium"],
    "Egypt": ["egypt"],
    "Iran": ["iran"],
    "New Zealand": ["new zealand"],
    "Spain": ["spain"],
    "Cape Verde": ["cape verde"],
    "Saudi Arabia": ["saudi arabia"],
    "Uruguay": ["uruguay"],
    "France": ["france"],
    "Senegal": ["senegal"],
    "Iraq": ["iraq"],
    "Norway": ["norway"],
    "Argentina": ["argentina"],
    "Algeria": ["algeria"],
    "Austria": ["austria"],
    "Jordan": ["jordan"],
    "Portugal": ["portugal"],
    "DR Congo": [
        "dr congo",
        "congo dr",
        "congo",
        "drc",
        "democratic republic of congo",
    ],
    "Uzbekistan": ["uzbekistan"],
    "Colombia": ["colombia"],
    "England": ["england"],
    "Croatia": ["croatia"],
    "Ghana": ["ghana"],
    "Panama": ["panama"],
}


def build_url(params: dict[str, Any]) -> str:
    return f"{BASE_MARKETS_URL}?{urllib.parse.urlencode(params)}"


def build_probe_urls() -> list[str]:
    urls = []

    for page in range(MAX_PAGES):
        offset = page * LIMIT_PER_REQUEST

        urls.append(
            build_url(
                {
                    "limit": LIMIT_PER_REQUEST,
                    "offset": offset,
                }
            )
        )

        urls.append(
            build_url(
                {
                    "limit": LIMIT_PER_REQUEST,
                    "offset": offset,
                    "active": "true",
                    "closed": "false",
                    "archived": "false",
                }
            )
        )

    return urls


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "world-cup-market-intelligence/0.5.7",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8")

    return json.loads(body)


def normalize_response_shape(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if isinstance(payload, dict):
        for key in ["data", "markets", "results"]:
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

    return []


def market_text(market: dict[str, Any]) -> str:
    fields = [
        market.get("question", ""),
        market.get("title", ""),
        market.get("description", ""),
        market.get("slug", ""),
        market.get("groupItemTitle", ""),
    ]

    events = market.get("events")
    if isinstance(events, list):
        for event in events:
            if isinstance(event, dict):
                fields.append(str(event.get("title", "")))
                fields.append(str(event.get("slug", "")))
                fields.append(str(event.get("description", "")))

    return " ".join(str(field) for field in fields if field).lower()


def find_keyword_matches(text: str, keywords: list[str]) -> list[str]:
    return sorted({keyword for keyword in keywords if keyword in text})


def find_team_matches(text: str) -> list[str]:
    matched_teams = []

    for team_name, aliases in TEAM_ALIASES.items():
        if any(alias in text for alias in aliases):
            matched_teams.append(team_name)

    return sorted(set(matched_teams))


def keyword_matches(market: dict[str, Any]) -> tuple[list[str], list[str]]:
    text = market_text(market)

    world_cup_matches = find_keyword_matches(text, WORLD_CUP_KEYWORDS)
    context_matches = find_keyword_matches(text, CONTEXT_KEYWORDS)
    team_matches = find_team_matches(text)

    if world_cup_matches:
        combined_matches = sorted(set(world_cup_matches + context_matches))
        return combined_matches, team_matches

    if team_matches and context_matches:
        combined_matches = sorted(set(context_matches))
        return combined_matches, team_matches

    return [], []


def parse_json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value

    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return []

        if isinstance(parsed, list):
            return parsed

    return []


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def summarize_market(
    market: dict[str, Any],
    matches: list[str],
    team_matches: list[str],
) -> dict[str, Any]:
    outcomes = parse_json_list(market.get("outcomes"))
    outcome_prices = parse_json_list(market.get("outcomePrices"))

    return {
        "id": market.get("id", ""),
        "conditionId": market.get("conditionId", ""),
        "question": market.get("question", ""),
        "slug": market.get("slug", ""),
        "matches": ", ".join(matches),
        "teamMatches": ", ".join(team_matches),
        "active": market.get("active", ""),
        "closed": market.get("closed", ""),
        "endDate": market.get("endDate", ""),
        "volumeNum": to_float(market.get("volumeNum", market.get("volume", 0))),
        "liquidityNum": to_float(market.get("liquidityNum", market.get("liquidity", 0))),
        "outcomes": json.dumps(outcomes, ensure_ascii=False),
        "outcomePrices": json.dumps(outcome_prices, ensure_ascii=False),
    }


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

    urls = build_probe_urls()

    all_markets: list[dict[str, Any]] = []
    errors: list[str] = []

    print("Polymarket World Cup discovery probe")
    print(f"Limit per request: {LIMIT_PER_REQUEST}")
    print(f"Max pages: {MAX_PAGES}")
    print(f"Total URLs to test: {len(urls)}")
    print("")

    for index, url in enumerate(urls):
        print(f"Fetching {index + 1}/{len(urls)}: {url}")

        try:
            payload = fetch_json(url)
        except urllib.error.HTTPError as exc:
            error = f"HTTP error for {url}: {exc.code} {exc.reason}"
            print(error)
            errors.append(error)
            continue
        except urllib.error.URLError as exc:
            error = f"Network/DNS error for {url}: {exc.reason}"
            print(error)
            errors.append(error)
            continue
        except TimeoutError:
            error = f"Timeout error for {url}"
            print(error)
            errors.append(error)
            continue
        except Exception as exc:
            error = f"Unexpected error for {url}: {repr(exc)}"
            print(error)
            errors.append(error)
            continue

        raw_path = RAW_DIR / f"worldcup_discovery_{timestamp}_{index}.json"
        raw_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        markets = normalize_response_shape(payload)
        print(f"Markets received: {len(markets)}")

        all_markets.extend(markets)

    unique_markets: dict[str, dict[str, Any]] = {}

    for market in all_markets:
        stable_id = str(
            market.get("conditionId")
            or market.get("id")
            or market.get("slug")
            or ""
        )

        if not stable_id:
            continue

        unique_markets[stable_id] = market

    matched_rows = []

    for market in unique_markets.values():
        matches, team_matches = keyword_matches(market)

        if matches or team_matches:
            matched_rows.append(
                summarize_market(
                    market=market,
                    matches=matches,
                    team_matches=team_matches,
                )
            )

    matched_rows.sort(
        key=lambda row: (
            to_float(row.get("volumeNum")),
            to_float(row.get("liquidityNum")),
        ),
        reverse=True,
    )

    csv_path = PROBE_DIR / f"worldcup_discovery_{timestamp}.csv"
    summary_path = PROBE_DIR / f"worldcup_discovery_summary_{timestamp}.txt"

    fieldnames = [
        "id",
        "conditionId",
        "question",
        "slug",
        "matches",
        "teamMatches",
        "active",
        "closed",
        "endDate",
        "volumeNum",
        "liquidityNum",
        "outcomes",
        "outcomePrices",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matched_rows)

    lines = []
    lines.append("Polymarket World Cup discovery probe summary")
    lines.append(f"Timestamp UTC: {timestamp}")
    lines.append(f"URLs tested: {len(urls)}")
    lines.append(f"Total markets received: {len(all_markets)}")
    lines.append(f"Unique markets: {len(unique_markets)}")
    lines.append(f"Matched markets: {len(matched_rows)}")
    lines.append("")

    lines.append("World Cup keywords:")
    for keyword in WORLD_CUP_KEYWORDS:
        lines.append(f"- {keyword}")

    lines.append("")
    lines.append("Context keywords:")
    for keyword in CONTEXT_KEYWORDS:
        lines.append(f"- {keyword}")

    lines.append("")
    lines.append("Team aliases:")
    for team_name, aliases in TEAM_ALIASES.items():
        lines.append(f"- {team_name}: {', '.join(aliases)}")

    if errors:
        lines.append("")
        lines.append("Errors:")
        for error in errors:
            lines.append(f"- {error}")

    lines.append("")
    lines.append("Top matched markets:")
    for row in matched_rows[:50]:
        lines.append(
            f"- {row['question']} | "
            f"matches={row['matches']} | "
            f"teams={row['teamMatches']} | "
            f"volume={row['volumeNum']} | "
            f"liquidity={row['liquidityNum']} | "
            f"slug={row['slug']}"
        )

    if not matched_rows:
        lines.append("No World Cup related markets found in this probe.")

    summary_path.write_text("\n".join(lines), encoding="utf-8")

    print("")
    print("\n".join(lines))
    print("")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved summary: {summary_path}")


if __name__ == "__main__":
    main()