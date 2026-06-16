\# Polymarket Live Workflow



This document explains the experimental Polymarket live workflow in World Cup Market Intelligence.



The Polymarket provider is a live API provider.

It requires network access and may depend on DNS, Cloudflare behavior, geo access or VPN availability.



The stable default workflow remains:



```text

manual\_csv

```



\---



\## Status



Current status:



```text

experimental

```



Provider name:



```text

polymarket

```



Workflow script:



```text

scripts/run\_polymarket\_live\_workflow.py

```



\---



\## What the workflow does



The live workflow runs three steps:



```text

validate experimental Polymarket provider

&#x20;   ↓

update Polymarket live snapshot

&#x20;   ↓

generate Polymarket YES-only World Cup ranking

```



It produces live outputs based on Polymarket Gamma API data.



\---



\## Command



Run the workflow with:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



If access fails, try again later or use VPN.



During testing, Polymarket access worked with Proton VPN using a Moldova server.



\---



\## Generated outputs



The workflow may generate or update:



```text

data/processed/snapshot\_latest.csv

data/processed/snapshots/\*-polymarket.csv

data/processed/polymarket\_worldcup\_yes\_ranking.csv

data/processed/polymarket\_worldcup\_yes\_ranking\_summary.txt

```



These are generated outputs.



For development commits, do not automatically commit generated files unless the goal of the version is explicitly to update processed data.



\---



\## Stable workflow remains manual CSV



The stable offline workflow is still:



```powershell

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



This should remain the default reproducible workflow.



\---



\## Polymarket provider validation



Validate the experimental provider with:



```powershell

python scripts/validate\_providers.py --provider polymarket --include-live

```



Expected result:



```text

Result: PASS

```



If validation fails because of network, DNS, timeout, Cloudflare or geo access, this does not mean the stable project is broken.



It means the live provider is temporarily unavailable.



\---



\## Polymarket live snapshot



Generate a live Polymarket snapshot with:



```powershell

python scripts/update\_snapshot.py --provider polymarket

```



This creates a live snapshot using the experimental Polymarket provider.



The provider currently:



```text

fetches live markets from Polymarket Gamma API

filters World Cup / FIFA markets

normalizes each outcome into the provider contract

outputs rows compatible with the snapshot pipeline

```



\---



\## YES-only ranking



Generate the Polymarket World Cup YES-only ranking with:



```powershell

python scripts/generate\_polymarket\_yes\_ranking.py

```



This keeps only useful winner-market rows:



```text

outcome = Yes

market\_title = Will X win the 2026 FIFA World Cup?

```



This is useful because winner markets also contain `No` rows, and those usually dominate raw sorted tables.



\---



\## Recommended live workflow



For live Polymarket testing, use:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



For stable offline testing, use:



```powershell

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



\---



\## Current recommendation



Use `manual\_csv` for stable reproducible work.



Use `polymarket` only for experimental live market intelligence.



Do not promote `polymarket` to stable until:



\* it works repeatedly without manual intervention;

\* false-positive market filtering remains low;

\* network failure handling is tested;

\* raw response caching is implemented or planned;

\* generated live outputs are clearly separated from stable manual outputs.



