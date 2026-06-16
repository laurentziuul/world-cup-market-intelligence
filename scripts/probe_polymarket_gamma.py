from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data" / "raw" / "polymarket"
PROBE_DIR = ROOT / "data" / "processed" / "polymarket"

MARKETS_URL = "https://gamma-api.polymarket.com/markets?limit=20"


def fetch_json(url: str):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "world-cup-market-intelligence/0.5.5",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        status_code = response.status
        body = response.read().decode("utf-8")

    return status_code, json.loads(body)


def normalize_response_shape(payload):
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in ["data", "markets", "results"]:
            value = payload.get(key)
            if isinstance(value, list):
                return value

    return []


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

    raw_path = RAW_DIR / f"gamma_markets_probe_{timestamp}.json"
    summary_path = PROBE_DIR / f"gamma_markets_probe_summary_{timestamp}.txt"

    print("Polymarket Gamma API probe")
    print(f"URL: {MARKETS_URL}")
    print("")

    try:
        status_code, payload = fetch_json(MARKETS_URL)
    except urllib.error.HTTPError as exc:
        print("HTTP error")
        print(f"Status: {exc.code}")
        print(f"Reason: {exc.reason}")
        raise SystemExit(1)
    except urllib.error.URLError as exc:
        print("Network/DNS error")
        print(f"Reason: {exc.reason}")
        raise SystemExit(1)
    except TimeoutError:
        print("Timeout error")
        raise SystemExit(1)
    except Exception as exc:
        print("Unexpected error")
        print(repr(exc))
        raise SystemExit(1)

    raw_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    markets = normalize_response_shape(payload)

    lines = []
    lines.append("Polymarket Gamma API probe summary")
    lines.append(f"Timestamp UTC: {timestamp}")
    lines.append(f"URL: {MARKETS_URL}")
    lines.append(f"HTTP status: {status_code}")
    lines.append(f"Raw file: {raw_path.relative_to(ROOT)}")
    lines.append(f"Markets detected: {len(markets)}")
    lines.append("")

    if markets:
        first = markets[0]

        lines.append("First market keys:")
        for key in sorted(first.keys()):
            lines.append(f"- {key}")

        lines.append("")
        lines.append("Candidate normalized fields from first market:")

        candidate_fields = [
            "id",
            "conditionId",
            "question",
            "title",
            "slug",
            "outcomes",
            "outcomePrices",
            "volume",
            "volumeNum",
            "liquidity",
            "liquidityNum",
            "active",
            "closed",
            "endDate",
        ]

        for field in candidate_fields:
            value = first.get(field, None)

            if isinstance(value, (dict, list)):
                value_preview = json.dumps(value, ensure_ascii=False)[:300]
            else:
                value_preview = str(value)[:300]

            lines.append(f"- {field}: {value_preview}")
    else:
        lines.append("No markets detected in response.")

    summary_path.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    print("")
    print(f"Saved raw response: {raw_path}")
    print(f"Saved summary: {summary_path}")


if __name__ == "__main__":
    main()