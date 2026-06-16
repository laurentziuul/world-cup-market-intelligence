\# Catalyst Notes Workflow



This document explains how to use catalyst notes in World Cup Market Intelligence.



Catalyst notes are manual explanations that can be linked to market movement signals.



The goal is to add context to probability changes.



The goal is not to provide betting advice.



\---



\## Purpose



The catalyst notes workflow helps answer questions such as:



```text

What event may explain this probability move?

Was there a match result?

Was there injury news?

Was there a squad announcement?

Was there a media narrative shift?

Was there a liquidity spike?

How confident are we in this explanation?

```



Catalyst notes make the historical trends layer more useful by connecting movement with possible real-world context.



\---



\## Manual catalyst notes file



Main catalyst notes file:



```text

data/manual/catalyst\_notes.csv

```



This is the working file where real catalyst notes can be added manually.



Current CSV schema:



```text

date

provider

team

market\_id

market\_title

event\_type

event\_title

note

source\_url

confidence

created\_by

```



\---



\## Sample file



Example catalyst notes are stored here:



```text

examples/catalyst\_notes\_sample.csv

```



The sample file is for reference only.



It should not be treated as real research data.



\---



\## Validate catalyst notes



Validate the main catalyst notes file:



```powershell

python scripts/validate\_catalyst\_notes.py

```



Expected result for an empty template:



```text

Result: PASS

Status: empty template

```



Expected result when notes exist:



```text

Result: PASS

Status: catalyst notes available

```



Validate the sample file:



```powershell

python scripts/validate\_catalyst\_notes.py --path examples/catalyst\_notes\_sample.csv

```



\---



\## Allowed event types



Supported event types:



```text

match\_result

injury

squad\_announcement

manager\_change

tactical\_change

media\_narrative

liquidity\_spike

bracket\_implication

market\_structure

other

```



Keep event types simple and human-readable.



Do not over-engineer them early.



\---



\## Confidence values



Allowed confidence values:



```text

low

medium

high

```



Suggested interpretation:



| Confidence | Meaning                                |

| ---------- | -------------------------------------- |

| low        | Possible connection, weak evidence     |

| medium     | Plausible connection with some context |

| high       | Stronger connection, likely relevant   |



Confidence does not mean certainty.



It only describes how strong the explanatory link appears.



\---



\## Add a catalyst note



A catalyst note row should look like this:



```text

date,provider,team,market\_id,market\_title,event\_type,event\_title,note,source\_url,confidence,created\_by

2026-06-20,polymarket,Germany,,Will Germany win the 2026 FIFA World Cup?,match\_result,Germany strong performance,"Germany probability may have moved after a strong match result and rising liquidity.",,medium,manual

```



The `market\_id` can be empty if unknown.



The `team` field is important because catalyst matching can use team matching.



\---



\## Catalyst matching



Catalyst matching links notes to signal rows.



Input files:



```text

data/processed/signal\_summary\_latest.csv

data/manual/catalyst\_notes.csv

```



Output file:



```text

data/processed/catalyst\_matches\_latest.csv

```



Run matching manually:



```powershell

python scripts/match\_catalyst\_notes.py --provider polymarket --lookback-days 7 --include-unmatched

```



The `--include-unmatched` flag keeps signal rows even when no catalyst note matches.



This is useful because the dashboard can show both matched and unmatched signals.



\---



\## Matching logic



The matching utility uses:



```text

provider

team

market\_id when available

date lookback window

```



Default lookback window:



```text

7 days

```



Basic matching idea:



```text

if provider matches

and team or market\_id matches

and catalyst date is close to signal date

then show the catalyst note beside the signal

```



\---



\## Historical trends workflow integration



Catalyst matching is included in the historical trends workflow.



Run:



```powershell

python scripts/run\_historical\_trends\_workflow.py

```



This workflow now runs:



```text

compare latest two snapshots

generate probability delta report

generate top movers report

generate signal summary report

match catalyst notes to signals

generate historical trends dashboard

```



Generated catalyst output:



```text

data/processed/catalyst\_matches\_latest.csv

```



\---



\## Trends dashboard integration



The trends dashboard reads catalyst matches from:



```text

data/processed/catalyst\_matches\_latest.csv

```



Dashboard path:



```text

docs/trends-dashboard/index.html

```



Public URL:



```text

https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

```



The trends dashboard includes a section:



```text

Catalyst matches

```



If no catalyst matches exist, the page still loads safely.



\---



\## Clean generated output



Catalyst matches output is generated and ignored by Git:



```text

data/processed/catalyst\_matches\_latest.csv

```



To remove it manually:



```powershell

Remove-Item data\\processed\\catalyst\_matches\_latest.csv -ErrorAction SilentlyContinue

```



If you do not want to publish a refreshed trends dashboard:



```powershell

git restore docs\\trends-dashboard\\index.html

```



\---



\## Recommended usage



Recommended manual workflow:



```powershell

python scripts/validate\_catalyst\_notes.py

python scripts/run\_historical\_trends\_workflow.py

python scripts/generate\_trends\_dashboard.py

start docs\\trends-dashboard\\index.html

```



If the dashboard looks useful and the goal is to publish it:



```powershell

git add docs\\trends-dashboard\\index.html

git commit -m "Refresh trends dashboard with catalyst context"

git push

```



\---



\## Interpretation rule



A catalyst note does not prove causality.



Preferred wording:



```text

may explain

possibly linked to

likely related to

appears consistent with

```



Avoid wording such as:



```text

caused by

guaranteed signal

betting edge

certain explanation

```



The project should remain transparent, research-oriented and educational.



\---



\## Current status



Catalyst notes workflow status:



```text

experimental

```



Current capabilities:



```text

manual catalyst notes template

sample catalyst notes

catalyst notes loader

catalyst notes validation

catalyst-to-signal matching

trends dashboard catalyst section

```



Future work:



```text

richer catalyst display

catalyst filtering by team

narrative intelligence documentation

v0.8.0 release notes

```



