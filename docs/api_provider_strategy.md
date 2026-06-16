\# API Provider Strategy



World Cup Market Intelligence is designed as a multi-source market intelligence system.



The goal is not to depend on one prediction market API.

The goal is to normalize data from multiple sources into the same internal format.



\---



\## Core principle



Every external API can have different raw data, but every provider must return the same normalized dataframe.



```text

external API

&#x20;   ↓

provider adapter

&#x20;   ↓

normalized dataframe

&#x20;   ↓

snapshot pipeline

&#x20;   ↓

trend engine

&#x20;   ↓

dashboard / brief

```



The rest of the pipeline should not care whether the data came from:



```text

manual\_csv

polymarket

predict\_fun

kalshi

manifold

other APIs

```



\---



\## Planned provider types



\### Offline providers



Offline providers work without network access.



Examples:



```text

manual\_csv

custom\_csv

manual\_google\_sheet\_export

```



These should remain reproducible and stable.



\### Live API providers



Live providers require network access and may fail because of:



```text

API downtime

rate limits

geo restrictions

DNS issues

schema changes

authentication changes

```



Examples:



```text

polymarket

predict\_fun

kalshi

manifold

other prediction market APIs

```



Live providers should be optional and should fail safely.



\---



\## Provider contract



All providers must return these normalized columns:



| Column         | Meaning                             |

| -------------- | ----------------------------------- |

| `market\_id`    | Stable market identifier            |

| `market\_title` | Human-readable market title         |

| `outcome`      | Outcome/team/player being tracked   |

| `price`        | Market-implied probability or price |

| `volume`       | Market volume, if available         |

| `liquidity`    | Market liquidity, if available      |

| `narrative`    | Analyst narrative label             |

| `catalyst`     | Main catalyst or reason to watch    |

| `source\_url`   | Source URL or provider reference    |

| `notes`        | Analyst notes                       |



The snapshot pipeline adds:



| Column                 | Meaning                                   |

| ---------------------- | ----------------------------------------- |

| `provider`             | Provider name                             |

| `snapshot\_time\_utc`    | Snapshot timestamp                        |

| `snapshot\_date\_utc`    | Snapshot date                             |

| `price\_change\_24h`     | Change versus previous snapshot           |

| `volume\_change\_24h`    | Volume change versus previous snapshot    |

| `liquidity\_change\_24h` | Liquidity change versus previous snapshot |



\---



\## API provider design



Each live API provider should have its own file:



```text

src/wcmi/providers/polymarket.py

src/wcmi/providers/predict\_fun.py

src/wcmi/providers/kalshi.py

src/wcmi/providers/manifold.py

```



Each provider should do four things:



```text

1\. fetch raw data

2\. parse provider-specific response

3\. map raw fields to normalized fields

4\. return normalized dataframe

```



The provider should not generate briefs, dashboards or trends directly.



\---



\## Failure policy



Live providers must fail safely.



A live provider should not break the whole project if an API is unavailable.



Preferred behavior:



```text

manual\_csv remains default

live providers are opt-in

network errors are clear

schema errors are clear

provider validation catches broken output

smoke tests can be run per provider

```



Example command:



```powershell

python scripts/update\_snapshot.py --provider polymarket

```



If the API fails, the error should explain the issue clearly.



\---



\## Provider registry status levels



Suggested status values:



| Status         | Meaning                                   |

| -------------- | ----------------------------------------- |

| `stable`       | Works reliably and can be used by default |

| `experimental` | Works but may change                      |

| `planned`      | Not implemented yet                       |

| `disabled`     | Implemented but intentionally inactive    |

| `broken`       | Known to be failing                       |



Live API providers should start as:



```text

experimental

```



until they are tested repeatedly.



\---



\## Multi-source intelligence goal



Long term, the system should support comparing multiple providers.



Example:



```text

Polymarket says France 16%

Predict.fun says France 15%

Kalshi says France 17%

Manual analyst baseline says France 16%

```



The useful intelligence is not just the price.



The useful intelligence is:



```text

provider disagreement

liquidity concentration

narrative divergence

stale markets

fast-moving markets

cross-provider confirmation

```



\---



\## Future normalized multi-source output



A later version may add fields such as:



| Column                | Meaning                                 |

| --------------------- | --------------------------------------- |

| `source\_market\_id`    | Original provider market ID             |

| `source\_outcome\_id`   | Original provider outcome ID            |

| `source\_provider\_url` | Direct source market URL                |

| `last\_traded\_at`      | Provider timestamp, if available        |

| `raw\_price\_type`      | yes/no, decimal odds, probability, etc. |

| `confidence\_score`    | Internal confidence score               |



These should not be added until at least two live providers exist.



\---



\## Near-term roadmap



\### v0.5.0



Create API provider strategy.



\### v0.5.1



Add placeholder provider files for planned APIs.



\### v0.5.2



Add provider status documentation and registry entries.



\### v0.5.3



Add one experimental live provider.



\### v0.5.4



Add raw response caching for live API providers.



\### v0.5.5



Add cross-provider comparison layer.



\---



\## Principle



Do not optimize for one API.



Optimize for a durable market-intelligence system that can survive API changes, provider failures and source disagreement.



