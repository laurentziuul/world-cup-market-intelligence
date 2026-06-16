\# Stable vs Experimental Workflows



World Cup Market Intelligence separates stable reproducible workflows from experimental live workflows.



This separation is intentional.



It prevents live API instability, network failures, provider schema changes or experimental filtering issues from breaking the stable project.



\---



\## Stable workflow



The stable workflow uses:



```text

manual\_csv

```



Status:



```text

stable

```



Main command:



```powershell

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



Stable dashboard:



```text

docs/dashboard/index.html

```



Public URL:



```text

https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/

```



The stable workflow is:



```text

offline

reproducible

manual-data based

safe for default demos

safe for documentation

safe for CI-style smoke testing

```



Use this workflow when the goal is to show that the core project works reliably.



\---



\## Experimental live workflow



The experimental live workflow uses:



```text

polymarket

```



Status:



```text

experimental

```



Main command:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



Experimental dashboard:



```text

docs/polymarket-dashboard/index.html

```



Public URL:



```text

https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/

```



The experimental workflow is:



```text

live API based

network-dependent

provider-dependent

sensitive to API schema changes

sensitive to DNS, Cloudflare, timeout or geo-access issues

not guaranteed to run offline

```



Use this workflow when the goal is to test live market intelligence from Polymarket.



\---



\## Why they are separate



The stable dashboard should not depend on live API access.



The experimental Polymarket dashboard should not overwrite or replace the stable dashboard.



This gives the project two clean layers:



```text

stable layer       = manual\_csv

experimental layer = polymarket

```



The stable layer proves the framework.



The experimental layer proves that the framework can connect to live market data.



\---



\## Current provider status



| Provider    | Status       | Type     | Notes                           |

| ----------- | ------------ | -------- | ------------------------------- |

| manual\_csv  | stable       | offline  | Default reproducible provider   |

| polymarket  | experimental | live API | First live provider integration |

| predict\_fun | planned      | live API | Placeholder                     |

| kalshi      | planned      | live API | Placeholder                     |

| manifold    | planned      | live API | Placeholder                     |



\---



\## Current recommendation



Use `manual\_csv` for stable reproducible work.



Use `polymarket` only for experimental live market intelligence.



Do not treat live provider failure as a stable project failure.



If Polymarket fails because of network, DNS, Cloudflare, timeout, geo access or API changes, the stable project is still valid as long as the `manual\_csv` workflow passes.



\---



\## Promotion criteria



A live provider should not be promoted from experimental to stable until:



```text

it works repeatedly without manual intervention

network failure handling is robust

false-positive filtering remains low

raw response caching exists or is planned

generated outputs are clearly separated

documentation explains expected failures

dashboard generation is reliable across multiple runs

```



Until then, live providers should remain experimental.



