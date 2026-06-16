\# Provider Failure Modes



This document explains how to interpret provider failures in World Cup Market Intelligence.



The project separates providers into three practical categories:



```text

stable

experimental

planned

```



Not every provider failure means the project is broken.



\---



\## Provider categories



Current provider categories:



| Provider    | Status       | Expected reliability | Meaning of failure                       |

| ----------- | ------------ | -------------------: | ---------------------------------------- |

| manual\_csv  | stable       |                 high | Possible project/pipeline issue          |

| polymarket  | experimental |      medium/variable | Possible live API/network/provider issue |

| predict\_fun | planned      |           not active | Expected until implemented               |

| kalshi      | planned      |           not active | Expected until implemented               |

| manifold    | planned      |           not active | Expected until implemented               |



\---



\## Stable provider failure



The stable provider is:



```text

manual\_csv

```



Stable command:



```powershell

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



Expected result:



```text

SMOKE TEST PASSED

```



A `manual\_csv` failure is important because this provider should work offline and reproducibly.



Possible causes:



```text

CSV schema changed

required column missing

snapshot generation broke

trend generation broke

dashboard generation broke

path or file structure changed

Python code regression

```



A stable provider failure should be treated as a project issue.



\---



\## Experimental provider failure



The experimental live provider is:



```text

polymarket

```



Live workflow command:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



Expected result when live access works:



```text

POLYMARKET LIVE WORKFLOW PASSED

```



A Polymarket failure does not automatically mean the project is broken.



Possible causes:



```text

internet connection issue

VPN not active

DNS failure

Cloudflare block

geo access restriction

provider timeout

provider API schema change

provider returns empty or unexpected data

market naming changed

filtering logic needs update

```



Polymarket failures should be interpreted as experimental live-provider failures unless the stable `manual\_csv` workflow also fails.



\---



\## Planned provider failure



Planned providers currently include:



```text

predict\_fun

kalshi

manifold

```



These providers are placeholders.



They are not expected to behave like stable providers yet.



Failure or lack of live output from planned providers is expected until they are implemented.



\---



\## Recommended diagnosis order



When something fails, diagnose in this order:



```text

1\. Check stable project health

2\. Check provider registry status

3\. Check provider-specific validation

4\. Check live network/API conditions

5\. Check generated outputs

```



\---



\## 1. Check stable project health



Run:



```powershell

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



If this passes, the stable core is healthy.



If this fails, fix the stable pipeline before debugging live providers.



\---



\## 2. Check provider registry status



Run:



```powershell

python scripts/validate\_providers.py

```



This validates the non-live providers.



For live providers, run with:



```powershell

python scripts/validate\_providers.py --provider polymarket --include-live

```



\---



\## 3. Check Polymarket live workflow



Run:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



This runs:



```text

provider validation

live snapshot generation

YES-only ranking generation

separate Polymarket dashboard generation

```



If this fails but `manual\_csv` passes, the project is still healthy.



The experimental live provider needs debugging.



\---



\## 4. Check Polymarket probes



Useful probe scripts:



```powershell

python scripts/probe\_polymarket\_gamma.py

python scripts/probe\_polymarket\_worldcup.py

python scripts/probe\_polymarket\_normalized.py

```



Use these to isolate whether the issue is:



```text

API access

market discovery

normalization

filtering

provider contract mapping

```



\---



\## 5. Check dashboard expectations



Stable dashboard:



```text

docs/dashboard/index.html

```



Public URL:



```text

https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/

```



Provider:



```text

manual\_csv

```



Experimental dashboard:



```text

docs/polymarket-dashboard/index.html

```



Public URL:



```text

https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/

```



Provider:



```text

polymarket

```



If the stable dashboard shows only manually curated teams, that is expected.



If the experimental dashboard shows too few teams, rerun the Polymarket live workflow and inspect provider/filtering behavior.



\---



\## Failure interpretation matrix



| Situation                               | Interpretation                              | Action                                |

| --------------------------------------- | ------------------------------------------- | ------------------------------------- |

| `manual\_csv` passes, `polymarket` fails | Stable project healthy, live provider issue | Debug Polymarket/network              |

| `manual\_csv` fails, `polymarket` passes | Stable pipeline issue                       | Fix stable workflow first             |

| both fail                               | Possible shared code/path issue             | Debug core scripts and recent commits |

| planned provider fails                  | Expected                                    | Implement provider first              |

| dashboard stable has 5 rows             | Expected manual CSV behavior                | No action                             |

| Polymarket dashboard has 0 rows         | Live provider/filtering issue               | Run probes and workflow               |



\---



\## Final rule



Stable project health is measured by:



```powershell

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



Experimental live provider health is measured by:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



Do not treat experimental live provider instability as stable project failure.



This separation is part of the project architecture.



