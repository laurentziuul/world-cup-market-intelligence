\# Provider Architecture



World Cup Market Intelligence is designed to be provider-agnostic.



The intelligence layer should not depend on a single market-data source.

Every provider should output the same normalized schema so that snapshots, dashboards and briefs can be generated consistently.



\## Why provider-agnostic design matters



Prediction-market and odds data can be fragile.



Common failure modes:



\* API downtime;

\* geographic restrictions;

\* DNS blocking;

\* rate limits;

\* schema changes;

\* missing liquidity fields;

\* closed or archived markets;

\* provider-specific naming differences;

\* unavailable historical data.



For this reason, the core pipeline should work even without external APIs.



The default v0 provider is the manual CSV provider.



\## Current v0 architecture



```text

manual CSV provider

&#x20;       ↓

normalized snapshot

&#x20;       ↓

brief generator

&#x20;       ↓

Markdown output

```



The manual CSV provider reads:



```text

data/manual/world\_cup\_markets.csv

```



and generates:



```text

data/processed/snapshot\_latest.csv

```



This snapshot becomes the standard input for downstream outputs:



```text

briefs/

dashboard/

analysis/

```



\## Normalized schema



Every provider should output at least the following fields:



| Field               | Description                               |

| ------------------- | ----------------------------------------- |

| `market\_id`         | Unique identifier for the market          |

| `market\_title`      | Human-readable market name                |

| `outcome`           | Outcome being tracked                     |

| `price`             | Market-implied probability or price       |

| `volume`            | Market volume, if available               |

| `liquidity`         | Available liquidity, if available         |

| `price\_change\_24h`  | 24h probability or price change           |

| `volume\_change\_24h` | 24h volume change                         |

| `narrative`         | Human-entered narrative label             |

| `catalyst`          | Event or reason that may explain the move |

| `source\_url`        | Source reference or provider URL          |

| `notes`             | Manual research notes                     |

| `snapshot\_time\_utc` | Timestamp of snapshot creation            |

| `provider`          | Data provider name                        |



\## Provider types



\### 1. Manual CSV provider



Status: active in v0



Purpose:



\* always available;

\* works offline;

\* useful for research and testing;

\* avoids external API dependency;

\* enables manual analyst judgment.



Input:



```text

data/manual/world\_cup\_markets.csv

```



Script:



```text

scripts/update\_snapshot\_manual.py

```



Output:



```text

data/processed/snapshot\_latest.csv

```



\### 2. Polymarket provider



Status: experimental / optional



Purpose:



\* fetch prediction-market data;

\* track price, liquidity and volume;

\* useful where API access is available.



Risks:



\* geographic restrictions;

\* DNS blocking;

\* endpoint changes;

\* availability issues;

\* provider-specific schema.



The Polymarket provider should never be required for the core project to run.



\### 3. Generic API provider



Status: planned



Purpose:



\* make it easy to add new event-market data sources;

\* map external fields into the normalized schema;

\* support future providers without changing the intelligence layer.



Possible future providers:



\* Kalshi;

\* Manifold;

\* sportsbook odds APIs;

\* custom CSV exports;

\* internal research databases.



\## Desired future structure



```text

src/wcmi/providers/

&#x20;   ├── base.py

&#x20;   ├── manual\_csv.py

&#x20;   ├── polymarket.py

&#x20;   ├── generic\_api.py

&#x20;   └── \_\_init\_\_.py

```



Each provider should implement the same high-level behavior:



```text

fetch raw data

&#x20;       ↓

normalize to common schema

&#x20;       ↓

write snapshot

```



\## Design principle



Providers collect data.

The intelligence engine interprets data.



These should remain separate.



```text

data providers

&#x20;       ↓

normalized schema

&#x20;       ↓

scoring / interpretation

&#x20;       ↓

briefs / dashboards

```



This separation makes the framework easier to test, extend and reuse across different event types.



\## Failure handling



Provider failures should not crash the entire system without explanation.



A good provider should return clear messages for:



\* DNS failure;

\* HTTP error;

\* empty response;

\* schema mismatch;

\* missing fields;

\* rate limit;

\* unavailable provider.



The system should degrade gracefully.



Example:



```text

Polymarket provider unavailable.

Use manual CSV provider instead:



python scripts/update\_snapshot\_manual.py

```



\## Open-source rule



The repository should never require users to bypass geographic restrictions or violate provider terms.



Manual mode should remain the default safe fallback.



\## Long-term goal



The provider architecture should allow the same intelligence workflow to support multiple event types:



```text

World Cup 2026

FOMC meetings

CPI releases

crypto unlocks

AI conferences

elections

court decisions

geopolitical deadlines

```



The core question remains the same:



```text

How do markets, narratives and liquidity evolve around scheduled uncertainty?

```



