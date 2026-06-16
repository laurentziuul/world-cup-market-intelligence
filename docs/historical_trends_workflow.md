\# Historical Trends Workflow



This document explains how to run the historical trends workflow in World Cup Market Intelligence.



The historical trends layer compares prediction-market snapshots over time and generates:



```text

snapshot comparison

probability deltas

top movers

signal summary

```



The goal is market intelligence, not betting advice.



\---



\## Purpose



The historical trends workflow is designed to answer questions such as:



```text

Which teams gained probability?

Which teams lost probability?

Which markets moved the most?

Which moves are supported by liquidity?

Which moves may be low-liquidity noise?

```



\---



\## Required input



The workflow requires at least two processed snapshot CSV files.



Snapshot directory:



```text

data/processed/snapshots/

```



For Polymarket, this means running the live workflow at least twice over time:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



Each run may create a new Polymarket snapshot.



\---



\## Main workflow command



Run the historical trends workflow with:



```powershell

python scripts/run\_historical\_trends\_workflow.py

```



Default behavior:



```text

provider = polymarket

outcome = Yes

status = existing

```



This is optimized for Polymarket YES-only World Cup winner markets.



\---



\## Full command example



```powershell

python scripts/run\_historical\_trends\_workflow.py --provider polymarket --outcome Yes --status existing

```



Optional parameters:



```powershell

python scripts/run\_historical\_trends\_workflow.py --provider polymarket --outcome Yes --status existing --limit 10 --min-abs-change-pp 0.25

```



\---



\## What the workflow runs



The workflow runs four steps:



```text

1\. compare latest two snapshots

2\. generate probability delta report

3\. generate top movers report

4\. generate signal summary report

```



Equivalent manual commands:



```powershell

python scripts/compare\_snapshots.py --provider polymarket

python scripts/generate\_probability\_deltas.py --provider polymarket --outcome Yes --status existing

python scripts/generate\_top\_movers.py --provider polymarket --outcome Yes

python scripts/generate\_signal\_summary.py --provider polymarket --outcome Yes

```



\---



\## Generated outputs



The workflow generates:



```text

data/processed/snapshot\_comparison\_latest.csv

data/processed/probability\_deltas\_latest.csv

data/processed/top\_movers\_latest.csv

data/processed/signal\_summary\_latest.csv

```



These are generated outputs and are ignored by Git by default.



They should not be committed unless a version explicitly requires publishing them.



\---



\## Snapshot comparison



Script:



```text

scripts/compare\_snapshots.py

```



Output:



```text

data/processed/snapshot\_comparison\_latest.csv

```



This compares the latest two snapshots for a provider.



It calculates:



```text

previous\_probability

current\_probability

probability\_change

probability\_change\_pp

previous\_volume

current\_volume

volume\_change

previous\_liquidity

current\_liquidity

liquidity\_change

```



The most important column is:



```text

probability\_change\_pp

```



This means percentage-point change.



Example:



```text

0.15 → 0.17 = +2.00 pp

```



\---



\## Probability deltas



Script:



```text

scripts/generate\_probability\_deltas.py

```



Output:



```text

data/processed/probability\_deltas\_latest.csv

```



This converts raw snapshot comparison into a cleaner probability movement report.



It adds:



```text

previous\_probability\_display

current\_probability\_display

probability\_change\_display

direction

```



Direction can be:



```text

up

down

flat

```



\---



\## Top movers



Script:



```text

scripts/generate\_top\_movers.py

```



Output:



```text

data/processed/top\_movers\_latest.csv

```



This extracts:



```text

top positive probability movers

top negative probability movers

top volume movers

top liquidity movers

```



Example categories:



```text

top\_positive\_probability\_movers

top\_negative\_probability\_movers

top\_volume\_movers

top\_liquidity\_movers

```



\---



\## Signal summary



Script:



```text

scripts/generate\_signal\_summary.py

```



Output:



```text

data/processed/signal\_summary\_latest.csv

```



This classifies movements into transparent signal labels.



Default signal rules:



```text

>= +2.00 pp        = strong\_positive\_move

+0.75 to +1.99 pp  = moderate\_positive\_move

\-0.74 to +0.74 pp  = flat\_no\_signal

\-0.75 to -1.99 pp  = moderate\_negative\_move

<= -2.00 pp        = strong\_negative\_move

```



Liquidity labels include:



```text

low\_liquidity\_noise

rising\_liquidity\_support

falling\_liquidity

normal\_liquidity

liquidity\_unknown

```



\---



\## Important interpretation rule



A probability move is more meaningful when it is supported by liquidity.



Example:



```text

large probability move + rising liquidity = stronger signal

large probability move + low liquidity = possible noise

```



The signal system is intentionally simple and transparent.



It is not a black-box trading model.



\---



\## If the workflow fails



Most common reason:



```text

not enough snapshots

```



The workflow requires at least two snapshot CSV files for the selected provider.



For Polymarket, run the live workflow more than once over time:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



Then rerun:



```powershell

python scripts/run\_historical\_trends\_workflow.py

```



\---



\## Stable vs experimental



Stable provider:



```text

manual\_csv

```



Experimental provider:



```text

polymarket

```



The historical trends workflow can support both, but the default configuration is currently optimized for:



```text

polymarket + Yes outcome + existing markets

```



\---



\## Clean generated outputs



The following trend outputs are ignored by Git:



```text

data/processed/snapshot\_comparison\_latest.csv

data/processed/probability\_deltas\_latest.csv

data/processed/top\_movers\_latest.csv

data/processed/signal\_summary\_latest.csv

```



To clean them manually:



```powershell

Remove-Item data\\processed\\snapshot\_comparison\_latest.csv -ErrorAction SilentlyContinue

Remove-Item data\\processed\\probability\_deltas\_latest.csv -ErrorAction SilentlyContinue

Remove-Item data\\processed\\top\_movers\_latest.csv -ErrorAction SilentlyContinue

Remove-Item data\\processed\\signal\_summary\_latest.csv -ErrorAction SilentlyContinue

```



\---



\## Current status



Historical trends workflow status:



```text

experimental

```



It is ready for local testing, but not yet integrated into the public dashboards.



Future work:



```text

add top movers to Polymarket dashboard

add signal labels to Polymarket dashboard

add manual catalyst notes

add historical trend release notes

```



