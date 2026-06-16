\# Historical Trends Architecture



This document defines the historical trends architecture for World Cup Market Intelligence.



The goal is to make the project capable of comparing prediction-market snapshots over time and extracting useful market intelligence signals.



\---



\## Purpose



The historical trends layer should answer questions such as:



```text

Which teams gained probability?

Which teams lost probability?

Which markets moved the most?

Which movements are meaningful?

Which movements may be noise?

Which markets gained or lost liquidity?

```



The goal is not to provide betting advice.



The goal is to provide transparent market intelligence.



\---



\## Current foundation



The project already has:



```text

stable manual\_csv provider

experimental Polymarket provider

processed snapshots

dashboard generation

YES-only Polymarket ranking

provider registry

stable vs experimental documentation

```



Relevant snapshot path:



```text

data/processed/snapshots/

```



Relevant latest snapshot path:



```text

data/processed/snapshot\_latest.csv

```



\---



\## Historical trends layer



The historical trends layer should sit after snapshot generation.



Conceptual flow:



```text

provider data

&#x20;   ↓

snapshot generation

&#x20;   ↓

historical snapshot archive

&#x20;   ↓

snapshot comparison

&#x20;   ↓

trend metrics

&#x20;   ↓

signal classification

&#x20;   ↓

dashboard / reports

```



\---



\## Snapshot comparison



The system should compare snapshots by matching markets across time.



Initial matching key:



```text

provider + market\_id + outcome

```



For Polymarket winner markets, this usually means:



```text

provider = polymarket

market\_id = Polymarket conditionId or market identifier

outcome = Yes

```



For manual CSV data, the matching key may use:



```text

provider + team + outcome

```



or another stable internal key depending on available columns.



\---



\## Required input columns



The trend layer should work with normalized provider output.



Expected useful columns include:



```text

provider

market\_id

market\_title

team

outcome

price

volume

liquidity

source\_url

timestamp

```



Not every provider may supply every field.



The trend layer should tolerate missing optional fields when possible.



\---



\## Core trend metrics



The first trend version should calculate:



```text

current\_probability

previous\_probability

probability\_change

probability\_change\_pp

current\_volume

previous\_volume

volume\_change

current\_liquidity

previous\_liquidity

liquidity\_change

```



The most important metric is:



```text

probability\_change\_pp

```



This means percentage-point change.



Example:



```text

France: 0.1520 → 0.1610 = +0.0090 = +0.90 percentage points

```



\---



\## Percentage-point logic



Prediction market probabilities are usually stored as decimals.



Example:



```text

0.15 = 15%

```



If a team moves from:



```text

0.15 to 0.17

```



The raw difference is:



```text

0.02

```



The percentage-point change is:



```text

+2.00 pp

```



The dashboard should show percentage-point changes because they are easier to understand.



\---



\## Comparison windows



Initial trend comparison should support:



```text

latest vs previous snapshot

latest vs first available snapshot

```



Later versions may support:



```text

1-day change

7-day change

30-day change

change since tournament start

change since last match

```



\---



\## Top movers



The trend layer should generate:



```text

top positive probability movers

top negative probability movers

top volume movers

top liquidity movers

```



Initial output can be CSV.



Later output can be dashboard sections.



\---



\## Signal classification



The system should classify probability movement using transparent rules.



Initial proposed rules:



```text

>= +2.00 pp      = strong positive move

+0.75 to +1.99 pp = moderate positive move

\-0.74 to +0.74 pp = flat / no signal

\-0.75 to -1.99 pp = moderate negative move

<= -2.00 pp      = strong negative move

```



Liquidity can modify interpretation.



Example:



```text

large probability move + low liquidity = possible noise

large probability move + rising liquidity = stronger signal

```



\---



\## Noise handling



Prediction markets can move for weak reasons.



The trend layer should avoid over-interpreting:



```text

low-liquidity moves

thin markets

stale markets

one-off API glitches

temporary wide spreads

```



Initial noise rule:



```text

if liquidity is below a minimum threshold, label movement as low-liquidity noise

```



The exact threshold can be adjusted later.



\---



\## Output files



Initial trend outputs should be written to:



```text

data/processed/trends\_latest.csv

data/processed/top\_movers\_latest.csv

data/processed/signal\_summary\_latest.csv

```



Potential future provider-specific outputs:



```text

data/processed/polymarket/trends\_latest.csv

data/processed/polymarket/top\_movers\_latest.csv

data/processed/polymarket/signal\_summary\_latest.csv

```



\---



\## Dashboard integration



The stable and experimental dashboards should remain separate.



Stable dashboard:



```text

docs/dashboard/index.html

```



Experimental Polymarket dashboard:



```text

docs/polymarket-dashboard/index.html

```



The Polymarket dashboard can later include:



```text

current YES ranking

probability change since previous snapshot

top positive movers

top negative movers

liquidity movers

signal labels

```



\---



\## Manual catalyst notes



The trend layer should prepare for manual catalyst notes.



Possible future file:



```text

data/manual/catalyst\_notes.csv

```



Potential columns:



```text

date

team

provider

market\_id

event\_type

note

source\_url

```



Example event types:



```text

match\_result

injury

squad\_announcement

manager\_change

media\_narrative

liquidity\_spike

other

```



\---



\## Non-goals



The historical trends layer should not initially include:



```text

automated news scraping

automated social media monitoring

betting recommendations

trading recommendations

black-box signal generation

closed-source logic

```



All logic should remain transparent and easy to inspect.



\---



\## Recommended implementation sequence



Suggested implementation path:



```text

1\. document historical trends architecture

2\. add snapshot comparison utility

3\. calculate probability deltas

4\. generate top movers CSV

5\. add signal classification rules

6\. generate signal summary CSV

7\. add trend section to Polymarket dashboard

8\. add manual catalyst notes structure

```



\---



\## Success criteria



The historical trends layer is useful when it can clearly show:



```text

what changed

how much it changed

whether the move is meaningful

whether liquidity supports the move

where the move appears in the dashboard

```



The system should remain transparent, reproducible and provider-agnostic.



