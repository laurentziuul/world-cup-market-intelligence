from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

import pandas as pd

from wcmi.providers.base import MarketProvider


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


NORMALIZED_COLUMNS = [
    "market_id",
    "market_title",
    "outcome",
    "price",
    "volume",
    "liquidity",
    "narrative",
    "catalyst",
    "source_url",
    "notes",
]


class PolymarketProvider(MarketProvider):
    name = "polymarket"

    def load(self) -> pd.DataFrame:
        markets = fetch_polymarket_markets()
        unique_markets = deduplicate_markets(markets)

        worldcup_markets = [
            market for market in unique_markets
            if is_worldcup_market(market)
        ]

        rows: list[dict[str, Any]] = []

        for market in worldcup_markets:
            rows.extend(normalize_market(market))

        dataframe = pd.DataFrame(rows, columns=NORMALIZED_COLUMNS)

        if dataframe.empty:
            return dataframe

        dataframe["price"] = pd.to_numeric(dataframe["price"], errors="coerce").fillna(0.0)
        dataframe["volume"] = pd.to_numeric(dataframe["volume"], errors="coerce").fillna(0.0)
        dataframe["liquidity"] = pd.to_numeric(dataframe["liquidity"], errors="coerce").fillna(0.0)

        dataframe = dataframe.sort_values(
            by=["volume", "liquidity", "price"],
            ascending=[False, False, False],
        ).reset_index(drop=True)

        return dataframe


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
            "User-Agent": "world-cup-market-intelligence-polymarket-provider/0.5.9",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"Polymarket API HTTP error: {exc.code} {exc.reason}. "
            "The provider is experimental. Try again later or use manual_csv."
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Polymarket API network/DNS error: {exc.reason}. "
            "The provider is experimental. Try VPN or use manual_csv."
        ) from exc
    except TimeoutError as exc:
        raise RuntimeError(
            "Polymarket API timeout. "
            "The provider is experimental. Try again later or use manual_csv."
        ) from exc

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


def fetch_polymarket_markets() -> list[dict[str, Any]]:
    all_markets: list[dict[str, Any]] = []

    for url in build_probe_urls():
        payload = fetch_json(url)
        all_markets.extend(normalize_response_shape(payload))

    return all_markets


def deduplicate_markets(markets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique_markets: dict[str, dict[str, Any]] = {}

    for market in markets:
        stable_id = str(
            market.get("conditionId")
            or market.get("id")
            or market.get("slug")
            or ""
        )

        if stable_id:
            unique_markets[stable_id] = market

    return list(unique_markets.values())


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


def is_worldcup_market(market: dict[str, Any]) -> bool:
    text = market_text(market)

    world_cup_matches = find_keyword_matches(text, WORLD_CUP_KEYWORDS)

    if world_cup_matches:
        return True

    return False


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


def build_source_url(market: dict[str, Any]) -> str:
    slug = str(market.get("slug", "")).strip()

    if slug:
        return f"https://polymarket.com/event/{slug}"

    market_id = str(market.get("conditionId") or market.get("id") or "").strip()

    if market_id:
        return f"polymarket:{market_id}"

    return "polymarket:unknown"


def normalize_market(market: dict[str, Any]) -> list[dict[str, Any]]:
    outcomes = parse_json_list(market.get("outcomes"))
    outcome_prices = parse_json_list(market.get("outcomePrices"))

    if not outcomes:
        return []

    market_id = str(
        market.get("conditionId")
        or market.get("id")
        or market.get("slug")
        or ""
    )

    market_title = str(market.get("question") or market.get("title") or "")
    volume = to_float(market.get("volumeNum", market.get("volume", 0)))
    liquidity = to_float(market.get("liquidityNum", market.get("liquidity", 0)))
    source_url = build_source_url(market)

    rows = []

    for index, outcome in enumerate(outcomes):
        if index < len(outcome_prices):
            price = to_float(outcome_prices[index])
        else:
            price = 0.0

        rows.append(
            {
                "market_id": market_id,
                "market_title": market_title,
                "outcome": str(outcome),
                "price": price,
                "volume": volume,
                "liquidity": liquidity,
                "narrative": "World Cup market",
                "catalyst": "FIFA World Cup 2026",
                "source_url": source_url,
                "notes": "Experimental Polymarket Gamma API provider.",
            }
        )

    return rows