\# Provider Status



This document tracks the current implementation status of all data providers in World Cup Market Intelligence.



The project is designed to support multiple data sources over time, while keeping one stable normalized provider contract.



\---



\## Status levels



| Status         | Meaning                                                     |

| -------------- | ----------------------------------------------------------- |

| `stable`       | Implemented, tested and safe to use in the default pipeline |

| `experimental` | Implemented but still under active testing                  |

| `planned`      | Added to the architecture, but not implemented yet          |

| `disabled`     | Implemented but intentionally turned off                    |

| `broken`       | Known to fail and should not be used                        |



\---



\## Current providers



| Provider      | Status    | Mode    | Network required | Description                                                   |

| ------------- | --------- | ------- | ---------------- | ------------------------------------------------------------- |

| `manual\_csv`  | `stable`  | offline | no               | Manual CSV provider. Default reproducible provider.           |

| `polymarket`  | `planned` | live    | yes              | Planned live API provider for Polymarket prediction markets.  |

| `predict\_fun` | `planned` | live    | yes              | Planned live API provider for Predict.fun prediction markets. |

| `kalshi`      | `planned` | live    | yes              | Planned live API provider for Kalshi prediction markets.      |

| `manifold`    | `planned` | live    | yes              | Planned live API provider for Manifold prediction markets.    |



\---



\## Current default provider



The current default provider is:



```text

manual\_csv

```



It reads data from:



```text

data/manual/world\_cup\_markets.csv

```



It can be run with:



```bash

python scripts/update\_snapshot.py --provider manual\_csv

```



The manual provider should remain the default until live providers are implemented and tested repeatedly.



\---



\## Planned live providers



The following providers exist as placeholders in the architecture:



```text

polymarket

predict\_fun

kalshi

manifold

```



They appear in the provider registry and in:



```bash

python scripts/update\_snapshot.py --list-providers

```



However, they are not implemented yet.



Trying to run one of them should return a clear error explaining that the provider is planned but not implemented.



Example:



```bash

python scripts/update\_snapshot.py --provider polymarket

```



Expected behavior:



```text

PolymarketProvider is planned but not implemented yet.

Use manual\_csv for the stable offline pipeline.

```



\---



\## Validation policy



Offline and stable providers can be validated with:



```bash

python scripts/validate\_providers.py

```



One provider can be validated directly with:



```bash

python scripts/validate\_providers.py --provider manual\_csv

```



Live providers are skipped by default because they may require:



```text

network access

API availability

authentication

geo access

rate-limit handling

schema stability

```



When live providers are implemented later, they can be tested explicitly with:



```bash

python scripts/validate\_providers.py --include-live

```



\---



\## Smoke test policy



The stable pipeline can be tested end-to-end with:



```bash

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



This verifies:



```text

provider validation

&#x20;   ↓

provider sample export

&#x20;   ↓

snapshot update

&#x20;   ↓

trend generation

&#x20;   ↓

dashboard generation

```



Before adding or modifying live providers, this smoke test should pass for `manual\_csv`.



\---



\## Provider promotion rules



A provider should move from `planned` to `experimental` only when:



\* it can fetch raw data;

\* it can normalize data into the required provider contract;

\* it passes provider validation;

\* it fails safely when the API is unavailable;

\* it does not break the manual CSV pipeline.



A provider should move from `experimental` to `stable` only when:



\* it has been tested repeatedly;

\* API schema changes are handled safely;

\* network errors produce clear messages;

\* raw response caching exists or is planned;

\* dashboard, trends and briefs work with its output.



\---



\## Current recommendation



Use:



```text

manual\_csv

```



for the stable offline workflow.



Treat all live providers as planned architecture until their API integrations are implemented and tested.



