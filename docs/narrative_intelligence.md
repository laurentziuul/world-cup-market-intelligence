\# Narrative Intelligence



Narrative intelligence is the layer that connects market movement with possible real-world explanations.



In World Cup Market Intelligence, the goal is not only to show that probabilities changed.



The goal is to help explain what may have changed in the world, in the market, or in the public narrative.



This layer is experimental.



It is for research and education only.



It is not betting advice.



\---



\## Core idea



Raw market data can answer:



```text

What moved?

How much did it move?

Was the move supported by liquidity?

```



Narrative intelligence tries to answer:



```text

Why might it have moved?

What event may explain it?

Was there a real-world catalyst?

Was there a narrative shift?

Was the move likely signal or noise?

```



\---



\## System layers



The project currently has four intelligence layers:



```text

1\. Market data

2\. Historical trends

3\. Signal classification

4\. Catalyst and narrative context

```



\---



\## 1. Market data



Market data comes from providers.



Current providers:



```text

manual\_csv

polymarket

```



Market data includes:



```text

team

market title

outcome

probability

volume

liquidity

source URL

timestamp

```



This is the base layer.



It tells us the current state of the market.



\---



\## 2. Historical trends



Historical trends compare snapshots over time.



This layer answers:



```text

Which teams gained probability?

Which teams lost probability?

Which markets had the largest moves?

Which moves happened with rising liquidity?

Which moves happened with low liquidity?

```



Generated outputs:



```text

snapshot\_comparison\_latest.csv

probability\_deltas\_latest.csv

top\_movers\_latest.csv

```



This is the movement layer.



It tells us what changed.



\---



\## 3. Signal classification



Signal classification turns probability movement into simple labels.



Examples:



```text

strong\_positive\_move

moderate\_positive\_move

flat\_no\_signal

moderate\_negative\_move

strong\_negative\_move

```



Liquidity labels help separate stronger moves from possible noise:



```text

rising\_liquidity\_support

low\_liquidity\_noise

falling\_liquidity

normal\_liquidity

liquidity\_unknown

```



This is the interpretation layer.



It tells us whether a move deserves attention.



\---



\## 4. Catalyst and narrative context



Catalyst notes are manual observations that may explain a signal.



Examples:



```text

match result

injury

squad announcement

manager change

tactical change

media narrative

liquidity spike

bracket implication

market structure

```



Catalyst notes live here:



```text

data/manual/catalyst\_notes.csv

```



They are matched to signals by:



```text

provider

team

market\_id when available

date lookback window

```



Generated output:



```text

catalyst\_matches\_latest.csv

```



This is the narrative layer.



It helps explain why a move may have happened.



\---



\## Why manual-first



The catalyst system is manual-first by design.



The project does not automatically scrape news or invent explanations.



This avoids several problems:



```text

hallucinated explanations

unsourced narratives

low-quality scraped content

false causality

overfitting stories to price movement

```



Manual notes keep the system transparent.



Every narrative explanation should be inspectable.



\---



\## Good narrative language



Preferred wording:



```text

may explain

possibly linked to

appears consistent with

likely related to

may have contributed to

```



Avoid wording such as:



```text

caused by

guaranteed

certain

proves that

betting edge

```



A catalyst note does not prove causality.



It adds context.



\---



\## Example



Market movement:



```text

Germany probability increases by +2.4 percentage points.

Liquidity also rises.

Signal label: strong\_positive\_move.

Liquidity label: rising\_liquidity\_support.

```



Possible catalyst note:



```text

Germany had a strong group-stage result.

Public expectations improved.

Market liquidity increased after the match.

Confidence: medium.

```



Narrative interpretation:



```text

The probability move may be linked to Germany's strong performance,

especially because the move was supported by rising liquidity.

```



This is stronger than simply saying:



```text

Germany went up.

```



But it is still not proof.



\---



\## What makes a narrative useful



A useful narrative has:



```text

clear event

clear team or market

date

source when available

confidence level

short explanation

transparent uncertainty

```



A weak narrative has:



```text

vague explanation

no date

no team

no source

overconfident wording

forced causality

```



\---



\## Current implementation



Current files:



```text

data/manual/catalyst\_notes.csv

examples/catalyst\_notes\_sample.csv

src/wcmi/catalyst\_notes.py

scripts/validate\_catalyst\_notes.py

scripts/match\_catalyst\_notes.py

scripts/run\_historical\_trends\_workflow.py

scripts/generate\_trends\_dashboard.py

docs/catalyst\_notes\_architecture.md

docs/catalyst\_notes\_workflow.md

```



Current generated output:



```text

data/processed/catalyst\_matches\_latest.csv

```



Current public dashboard section:



```text

Catalyst matches

```



Public trends dashboard:



```text

https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

```



\---



\## Relationship to prediction markets



Prediction markets can react to:



```text

real events

public narratives

information asymmetry

liquidity changes

market maker behavior

thin-market noise

speculation

```



Narrative intelligence should not assume every move is rational.



It should help separate:



```text

event-driven movement

liquidity-driven movement

noise-driven movement

narrative-driven movement

```



\---



\## Future direction



Possible future improvements:



```text

team-level catalyst pages

catalyst filters in the dashboard

confidence-weighted narrative summaries

manual source links

signal labels inside the Polymarket dashboard

richer event taxonomy

timeline view per team

```



The long-term goal is to build a transparent market-intelligence layer that combines:



```text

probability movement

liquidity context

manual catalyst notes

public narrative tracking

```



without pretending to be a black-box prediction model.



\---



\## Status



Narrative intelligence status:



```text

experimental

```



Current role:



```text

research layer

context layer

explanation layer

dashboard enhancement

```



Not current role:



```text

betting model

investment system

automated news scraper

causal inference engine

```



Powered by Mayior Capital.



