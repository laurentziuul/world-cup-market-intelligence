\# API Sources Matrix



This document tracks potential external data sources for World Cup Market Intelligence.



The goal is not to depend on a single API.

The goal is to evaluate multiple sources and normalize them into the same internal provider contract.



\---



\## Current principle



Every API source may have different raw data, authentication rules, response formats and reliability risks.



But every implemented provider must eventually return the same normalized dataframe:



```text

market\_id

market\_title

outcome

price

volume

liquidity

narrative

catalyst

source\_url

notes

provider

```



\---



\## Candidate API sources



| Source              | Provider name         | Current status | Network required | Auth required | Geo risk | World Cup market support | Priority        |

| ------------------- | --------------------- | -------------- | ---------------- | ------------- | -------- | ------------------------ | --------------- |

| Manual CSV          | `manual\_csv`          | stable         | no               | no            | none     | manual                   | current default |

| Polymarket          | `polymarket`          | planned        | yes              | unknown       | possible | to verify                | high            |

| Predict.fun         | `predict\_fun`         | planned        | yes              | unknown       | unknown  | to verify                | high            |

| Kalshi              | `kalshi`              | planned        | yes              | likely        | possible | to verify                | medium          |

| Manifold            | `manifold`            | planned        | yes              | unknown       | unknown  | to verify                | medium          |

| Custom CSV          | `custom\_csv`          | planned        | no               | no            | none     | manual                   | medium          |

| Google Sheet export | `manual\_google\_sheet` | planned        | optional         | optional      | none     | manual                   | low             |



\---



\## Evaluation checklist



Before implementing a live provider, verify:



| Question                               | Why it matters                       |

| -------------------------------------- | ------------------------------------ |

| Does the API expose market prices?     | Required for `price`                 |

| Does it expose per-outcome prices?     | Required for normalized outcome rows |

| Does it expose volume?                 | Needed for signal quality            |

| Does it expose liquidity?              | Needed for market depth analysis     |

| Does it expose market URLs?            | Useful for `source\_url`              |

| Does it expose stable IDs?             | Needed for historical tracking       |

| Does it require authentication?        | Impacts reproducibility              |

| Does it have rate limits?              | Impacts automation                   |

| Does it work from the user’s location? | Avoids geo/DNS failures              |

| Does it support World Cup markets?     | Required for this project            |

| Can raw responses be cached?           | Helps debugging and reproducibility  |

| Does the schema look stable?           | Reduces maintenance risk             |



\---



\## Provider implementation priority



\### Priority 1 — Offline stability



Keep this stable at all times:



```text

manual\_csv

```



The manual CSV provider is the fallback provider and should never be broken by live API work.



\---



\### Priority 2 — First experimental live provider



Potential first choices:



```text

polymarket

predict\_fun

```



Selection criteria:



\* easiest public data access;

\* least authentication friction;

\* stable market/outcome schema;

\* direct World Cup market support;

\* clear price fields;

\* acceptable geo/network access.



\---



\### Priority 3 — Additional live providers



After one live provider works, add more sources:



```text

kalshi

manifold

other APIs

```



The goal is cross-provider comparison, not single-provider dependence.



\---



\## Normalization mapping template



For each new API provider, document the mapping before coding.



| Normalized column | Raw API field    | Notes                          |

| ----------------- | ---------------- | ------------------------------ |

| `market\_id`       | TBD              | Must be stable                 |

| `market\_title`    | TBD              | Human-readable title           |

| `outcome`         | TBD              | Team/outcome name              |

| `price`           | TBD              | Probability or price           |

| `volume`          | TBD              | Use 0 if unavailable           |

| `liquidity`       | TBD              | Use 0 if unavailable           |

| `narrative`       | manual/default   | Can be analyst-entered         |

| `catalyst`        | manual/default   | Can be analyst-entered         |

| `source\_url`      | TBD              | Direct market URL if available |

| `notes`           | generated/manual | Provider-specific notes        |



\---



\## Failure policy for live APIs



Live API providers must fail safely.



A live provider should not break the offline pipeline.



Expected behavior:



```text

manual\_csv remains stable

live providers are opt-in

network errors are clear

API schema errors are clear

missing fields are handled explicitly

raw responses can be saved for debugging

```



\---



\## Open research questions



\* Which API has the cleanest public access?

\* Which source has the most reliable World Cup markets?

\* Which provider exposes volume and liquidity clearly?

\* Which provider has the lowest geo/access risk?

\* Which provider has stable outcome IDs?

\* Should raw API responses be cached before normalization?

\* Should cross-provider disagreement be shown in the dashboard?



\---



\## Next implementation step



Before writing live provider code, choose one source and document:



```text

API endpoint

authentication requirement

example raw response

field mapping

failure modes

normalization rules

```



Only after that should a provider move from:



```text

planned

```



to:



```text

experimental

```



