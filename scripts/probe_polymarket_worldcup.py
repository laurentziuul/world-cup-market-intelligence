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

EVENT_KEYWORDS = [
    "world cup",
    "fifa world cup",
    "fifa",
    "2026 world cup",
    "world cup 2026",
    "soccer",
    "football",
    "champion",
    "winner",
    "golden boot",
    "group winner",
    "qualify",
    "qualification",
    "final",
    "semifinal",
]

TEAM_KEYWORDS = [
    "mexico",
    "south africa",
    "south korea",
    "czechia",
    "czech republic",
    "canada",
    "bosnia",
    "bosnia and herzegovina",
    "qatar",
    "switzerland",
    "brazil",
    "morocco",
    "haiti",
    "scotland",
    "united states",
    "usa",
    "usmnt",
    "paraguay",
    "australia",
    "turkey",
    "germany",
    "curacao",
    "curaçao",
    "ivory coast",
    "cote d'ivoire",
    "ecuador",
    "netherlands",
    "japan",
    "sweden",
    "tunisia",
    "belgium",
    "egypt",
    "iran",
    "new zealand",
    "spain",
    "cape verde",
    "saudi arabia",
    "uruguay",
    "france",
    "senegal",
    "iraq",
    "norway",
    "argentina",
    "algeria",
    "austria",
    "jordan",
    "portugal",
    "dr congo",
    "democratic republic of congo",
    "uzbekistan",
    "colombia",
    "england",
    "croatia",
    "ghana",
    "panama",
]

CONTEXT_KEYWORDS = [
    "world cup",
    "fifa",
    "soccer",
    "football",
    "2026",
    "qualify",
    "qualification",
    "champion",
    "winner",
    "group",
]


def build_url(params: dict[str, Any]) -> str:
    return f"{BASE_MARKETS_URL}?{urllib.parse.urlencode(params)}"


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "world-cup-market-intelligence/0.5.6",
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


def keyword_matches(market: dict[str, Any]) -> list[str]:
    text = market_text(market)

    event_matches = [
        keyword for keyword in EVENT_KEYWORDS
        if keyword in text
    ]

    team_matches = [
        keyword for keyword in TEAM_KEYWORDS
        if keyword in text
    ]

    context_matches = [
        keyword for keyword in CONTEXT_KEYWORDS
        if keyword in text
    ]

    if event_matches:
        return sorted(set(event_matches + team_matches))

    if team_matches and context_matches:
        return sorted(set(team_matches + context_matches))

    return []


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


def summarize_market(market: dict[str, Any], matches: list[str]) -> dict[str, Any]:
    outcomes = parse_json_list(market.get("outcomes"))
    outcome_prices = parse_json_list(market.get("outcomePrices"))

    return {
        "id": market.get("id", ""),
        "conditionId": market.get("conditionId", ""),
        "question": market.get("question", ""),
        "slug": market.get("slug", ""),
        "matches": ", ".join(matches),
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

    urls = [
        build_url({"limit": 500}),
        build_url({"limit": 500, "active": "true", "closed": "false"}),
        build_url({"limit": 500, "archived": "false"}),
    ]

    all_markets: list[dict[str, Any]] = []
    errors: list[str] = []

    print("Polymarket World Cup discovery probe")
    print("")

    for url in urls:
        print(f"Fetching: {url}")

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

        raw_path = RAW_DIR / f"worldcup_discovery_{timestamp}_{len(all_markets)}.json"
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
        matches = keyword_matches(market)

        if matches:
            matched_rows.append(summarize_market(market, matches))

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

    lines.append("Event keywords:")
    for keyword in EVENT_KEYWORDS:
        lines.append(f"- {keyword}")

    lines.append("")
    lines.append("Team keywords:")
    for keyword in TEAM_KEYWORDS:
        lines.append(f"- {keyword}")

    lines.append("")
    lines.append("Context keywords:")
    for keyword in CONTEXT_KEYWORDS:
        lines.append(f"- {keyword}")

    if errors:
        lines.append("")
        lines.append("Errors:")
        for error in errors:
            lines.append(f"- {error}")

    lines.append("")
    lines.append("Top matched markets:")
    for row in matched_rows[:25]:
        lines.append(
            f"- {row['question']} | matches={row['matches']} | "
            f"volume={row['volumeNum']} | liquidity={row['liquidityNum']} | "
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