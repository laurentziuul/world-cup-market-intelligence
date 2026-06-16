# First Experimental API Provider Selection

This document records the first live API provider selected for experimental implementation.

The goal is not to depend on one API.
The goal is to choose the first provider carefully, implement it safely, and keep the offline `manual_csv` provider stable.

---

## Selected provider

```text
polymarket
```

Polymarket is selected as the first experimental live provider.

---

## Why Polymarket first

Polymarket is a strong first candidate because:

* it has public market data endpoints;
* the public market-data workflow can start without API-key authentication;
* market discovery can be done through public market endpoints;
* outcome prices can potentially be mapped into normalized outcome rows;
* it has official documentation for markets, prices, price history and order books;
* it is highly relevant to prediction-market intelligence.

---

## Important risk

Polymarket may still have access issues depending on:

```text
location
DNS resolution
Cloudflare behavior
rate limits
API changes
schema changes
geo restrictions
```

The provider must therefore be implemented as:

```text
experimental
```

not stable.

The stable default provider remains:

```text
manual_csv
```

---

## Relevant public endpoints to investigate

Potential starting endpoints:

```text
https://gamma-api.polymarket.com/markets
https://clob.polymarket.com/price
https://clob.polymarket.com/book
```

The first implementation should probably start with:

```text
Gamma API /markets
```

because it is useful for market discovery and does not require authentication for basic market-data exploration.

---

## Normalization mapping draft

| Normalized column | Polymarket field candidate   | Notes                                |
| ----------------- | ---------------------------- | ------------------------------------ |
| `market_id`       | `id` or `conditionId`        | Need stable identifier               |
| `market_title`    | `question`                   | Human-readable market question       |
| `outcome`         | `outcomes` array item        | Needs one normalized row per outcome |
| `price`           | `outcomePrices` array item   | Convert to numeric probability       |
| `volume`          | `volume` / `volumeNum`       | Use best numeric field available     |
| `liquidity`       | `liquidity` / `liquidityNum` | Use best numeric field available     |
| `narrative`       | default/manual               | Can start empty or generated         |
| `catalyst`        | default/manual               | Can start empty                      |
| `source_url`      | `slug` or constructed URL    | Use market or event URL if possible  |
| `notes`           | generated                    | Include provider and endpoint note   |

---

## First implementation rules

The first Polymarket provider must:

* not break `manual_csv`;
* be opt-in only;
* be registered as `experimental`;
* fail with a clear error if the API is unreachable;
* return the same normalized dataframe contract as `manual_csv`;
* pass provider validation when network access works;
* keep raw response caching as a near-term follow-up if not included in the first spike.

---

## Proposed command

When implemented, the provider should run with:

```powershell
python scripts/update_snapshot.py --provider polymarket
```

The stable offline pipeline should continue to run with:

```powershell
python scripts/update_snapshot.py --provider manual_csv
```

---

## Decision

First experimental live API provider:

```text
polymarket
```

Second likely candidate after Polymarket:

```text
predict_fun
```

Reason: Predict.fun also appears to expose market-related endpoints, but should be evaluated after the Polymarket experimental adapter is working.
