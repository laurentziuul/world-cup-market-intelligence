\# Polymarket Troubleshooting Guide



This guide explains how to debug the experimental Polymarket live provider.



The Polymarket provider is experimental and depends on live API access.



A Polymarket failure does not mean the stable project is broken.



The stable workflow remains:



```powershell

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



\---



\## Quick diagnosis



If the Polymarket workflow fails, first identify where it failed:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



The workflow runs:



```text

1\. validate experimental Polymarket provider

2\. update Polymarket live snapshot

3\. generate Polymarket YES-only ranking

4\. generate separate Polymarket live dashboard

```



If step 1 fails, the provider cannot load live data.



If step 2 fails, the snapshot pipeline cannot write or normalize the live data.



If step 3 fails, the YES-only ranking script cannot extract winner markets.



If step 4 fails, the dashboard generator cannot create the HTML page.



\---



\## Most common causes



Common failure causes:



```text

no internet connection

VPN not active

DNS failure

Cloudflare blocking

geo access restriction

Polymarket API timeout

Polymarket API schema change

empty or unexpected API response

```



During testing, access worked using Proton VPN with a Moldova server.



\---



\## Recommended first checks



Run the stable workflow first:



```powershell

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



Expected result:



```text

SMOKE TEST PASSED

```



If this passes, the stable project is healthy.



Then validate the Polymarket provider:



```powershell

python scripts/validate\_providers.py --provider polymarket --include-live

```



Expected result when live access works:



```text

Result: PASS

```



\---



\## API probe



Use the Polymarket Gamma API probe:



```powershell

python scripts/probe\_polymarket\_gamma.py

```



This checks whether the Gamma API responds and prints sample market fields.



Expected signs of success:



```text

HTTP 200

markets returned

fields such as conditionId, question, outcomes, outcomePrices, volumeNum, liquidityNum, slug

```



If this fails, the issue is probably network, VPN, DNS, Cloudflare or geo access.



\---



\## World Cup discovery probe



Run:



```powershell

python scripts/probe\_polymarket\_worldcup.py

```



This checks whether World Cup-related markets can be discovered.



Expected signs of success:



```text

markets received

unique markets counted

World Cup matches found

```



If this returns zero World Cup markets but the API probe works, the issue may be filtering logic or market naming changes.



\---



\## Normalized provider probe



Run:



```powershell

python scripts/probe\_polymarket\_normalized.py

```



This checks whether raw Polymarket markets can be normalized into the internal provider contract.



Expected signs of success:



```text

Normalized rows: ...

```



If this fails, the issue may be API schema change or normalization logic.



\---



\## Full live workflow



Run:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



Expected success result:



```text

POLYMARKET LIVE WORKFLOW PASSED

```



This should generate or update:



```text

data/processed/snapshot\_latest.csv

data/processed/snapshots/\*-polymarket.csv

data/processed/polymarket\_worldcup\_yes\_ranking.csv

data/processed/polymarket\_worldcup\_yes\_ranking\_summary.txt

docs/polymarket-dashboard/index.html

```



\---



\## If VPN is required



If Polymarket fails without VPN:



```text

turn on VPN

try Proton VPN Moldova server

rerun provider validation

rerun live workflow

```



Commands:



```powershell

python scripts/validate\_providers.py --provider polymarket --include-live

python scripts/run\_polymarket\_live\_workflow.py

```



\---



\## If DNS fails



Symptoms may include:



```text

connection error

name resolution error

temporary failure in name resolution

```



Possible actions:



```text

restart VPN

switch VPN server

restart terminal

try another network

try again later

```



\---



\## If Cloudflare or geo access blocks the request



Symptoms may include:



```text

403

HTML page returned instead of JSON

unexpected response format

request timeout

```



Possible actions:



```text

turn on VPN

switch VPN country

wait and retry later

do not treat this as a stable workflow failure

```



\---



\## If API schema changes



Symptoms may include missing fields such as:



```text

conditionId

question

outcomes

outcomePrices

volumeNum

liquidityNum

slug

```



Possible actions:



```text

run the Gamma API probe

inspect printed fields

update the Polymarket provider mapping

rerun provider validation

```



Relevant file:



```text

src/wcmi/providers/polymarket.py

```



\---



\## If dashboard shows too few teams



Check which dashboard you are viewing.



Stable dashboard:



```text

https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/

```



This uses:



```text

manual\_csv

```



Experimental Polymarket dashboard:



```text

https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/

```



This uses:



```text

polymarket

```



If the stable dashboard shows only manually curated teams, that is expected.



If the Polymarket dashboard shows too few teams, rerun:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



Then commit the refreshed dashboard if you want to publish it:



```powershell

git add docs\\polymarket-dashboard\\index.html

git commit -m "Refresh Polymarket dashboard"

git push

```



\---



\## Clean generated outputs



After testing, clean generated outputs unless you intentionally want to commit them:



```powershell

git restore data\\processed\\snapshot\_latest.csv

git restore data\\processed\\snapshots

Remove-Item data\\processed\\polymarket\_worldcup\_yes\_ranking.csv -ErrorAction SilentlyContinue

Remove-Item data\\processed\\polymarket\_worldcup\_yes\_ranking\_summary.txt -ErrorAction SilentlyContinue

```



If you do not want to publish a refreshed Polymarket dashboard:



```powershell

git restore docs\\polymarket-dashboard\\index.html

```



\---



\## Final rule



Stable project health is measured by:



```powershell

python scripts/smoke\_test\_pipeline.py --provider manual\_csv

```



Live provider health is measured by:



```powershell

python scripts/run\_polymarket\_live\_workflow.py

```



If `manual\_csv` passes and `polymarket` fails, the project is still healthy.



The live provider is experimental.



