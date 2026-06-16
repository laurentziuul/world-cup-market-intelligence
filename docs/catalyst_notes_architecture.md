\# Catalyst Notes Architecture



This document defines the catalyst notes architecture for World Cup Market Intelligence.



The goal is to connect market movement with possible real-world context.



The project should not only show that a probability changed.



It should also help explain why the move may have happened.



\---



\## Purpose



The catalyst notes layer is designed to answer questions such as:



```text

What event may have caused this market move?

Was there a match result?

Was there injury news?

Was there a squad announcement?

Was there a media narrative shift?

Was there a liquidity spike?

Was this move likely meaningful or just noise?

```



The goal is market intelligence, not betting advice.



\---



\## Current foundation



As of `v0.7.0`, the project already supports:



```text

stable manual CSV workflow

experimental Polymarket live provider

snapshot comparison

probability deltas

top movers

signal summary

historical trends dashboard

```



This creates the base for catalyst analysis.



The next step is to attach context to the movements.



\---



\## Conceptual flow



Catalyst notes should sit after trend detection.



Conceptual flow:



```text

provider data

&#x20;   ↓

snapshot generation

&#x20;   ↓

historical trend workflow

&#x20;   ↓

probability deltas

&#x20;   ↓

top movers

&#x20;   ↓

signal summary

&#x20;   ↓

catalyst notes

&#x20;   ↓

narrative intelligence dashboard

```



\---



\## What is a catalyst?



A catalyst is a possible reason for a market move.



Examples:



```text

match result

injury news

squad announcement

managerial decision

tactical change

media narrative

liquidity spike

major bettor activity

bracket implication

weather or venue factor

other

```



Catalysts can be manual at first.



Later, they may be semi-automated.



\---



\## Manual-first approach



The first version should use a manual CSV file.



Proposed file:



```text

data/manual/catalyst\_notes.csv

```



This keeps the system simple, transparent and easy to audit.



The project should not start with automated news scraping.



Manual notes are safer and easier to verify.



\---



\## Proposed CSV schema



Initial catalyst notes columns:



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



Column meaning:



| Column       | Meaning                                                  |

| ------------ | -------------------------------------------------------- |

| date         | Date of the catalyst or observation                      |

| provider     | Provider related to the market, for example `polymarket` |

| team         | Team affected by the event                               |

| market\_id    | Optional market identifier                               |

| market\_title | Optional market title                                    |

| event\_type   | Type of catalyst                                         |

| event\_title  | Short human-readable title                               |

| note         | Explanation of the catalyst                              |

| source\_url   | Optional source link                                     |

| confidence   | Low, medium or high confidence                           |

| created\_by   | Person or system that added the note                     |



\---



\## Event types



Initial event types:



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



The event type should remain simple.



Do not over-engineer it early.



\---



\## Confidence levels



Catalyst notes should have a confidence label.



Initial confidence values:



```text

low

medium

high

```



Suggested interpretation:



| Confidence | Meaning                                           |

| ---------- | ------------------------------------------------- |

| low        | Possible connection, but weak evidence            |

| medium     | Plausible connection with some supporting context |

| high       | Strong connection, likely related to the move     |



The confidence field should not imply certainty.



It only describes how strong the explanatory link appears.



\---



\## Linking catalysts to market movement



The first matching logic can be simple.



Catalyst notes can match trend rows by:



```text

provider

team

market\_id

date window

```



Initial approach:



```text

if team matches and date is close to the market move, show the note

```



Later, this can become more advanced.



\---



\## Date window logic



A catalyst may happen before, during or after a market move.



Initial windows:



```text

same day

previous 1 day

previous 3 days

previous 7 days

```



The first implementation can use a simple configurable lookback window.



Example:



```text

Show catalyst notes from the previous 7 days for the same team.

```



\---



\## How catalyst notes should appear



Catalyst notes should eventually appear in:



```text

historical trends dashboard

signal summary section

top movers section

future narrative intelligence page

```



A top mover without context is only a movement.



A top mover with context becomes market intelligence.



\---



\## Example note



Example manual catalyst note:



```text

date: 2026-06-20

provider: polymarket

team: Germany

market\_id:

market\_title: Will Germany win the 2026 FIFA World Cup?

event\_type: match\_result

event\_title: Germany wins group match convincingly

note: Germany's probability increased after a strong group-stage performance and rising liquidity.

source\_url:

confidence: medium

created\_by: manual

```



\---



\## Relationship with signal summary



The signal summary tells us:



```text

what moved

how much it moved

whether liquidity supports it

```



The catalyst layer adds:



```text

what may explain the move

```



Together, they create a more complete intelligence view.



\---



\## Avoiding over-interpretation



Catalyst notes should not claim certainty unless evidence is strong.



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

definitely because of

guaranteed signal

betting edge

```



The project should stay research-oriented.



\---



\## Non-goals



The first catalyst notes version should not include:



```text

automated news scraping

automated social media analysis

LLM-generated unsourced claims

betting recommendations

black-box narrative scoring

automated trading decisions

```



Manual notes first.



Automation later.



\---



\## Proposed v0.8.x implementation path



Suggested steps:



```text

v0.8.1 — Document catalyst notes architecture

v0.8.2 — Add catalyst notes CSV template

v0.8.3 — Add catalyst notes loader

v0.8.4 — Add catalyst notes validation

v0.8.5 — Add catalyst notes sample data

v0.8.6 — Add catalyst notes matching utility

v0.8.7 — Add catalyst notes section to trends dashboard

v0.8.8 — Add narrative intelligence documentation

v0.8.9 — Add release notes for v0.8.0

v0.8.10 — Final validation and tag v0.8.0

```



\---



\## Success criteria



The catalyst notes layer is useful when the project can show:



```text

which market moved

how much it moved

what signal label it received

what catalyst may explain it

how confident that explanation is

where the supporting note came from

```



\---



\## Final principle



The catalyst system should make market intelligence richer, but not less transparent.



Every catalyst note should be:



```text

auditable

human-readable

clearly sourced when possible

clearly labeled by confidence

separate from betting advice

```



The project should remain educational, research-oriented and provider-agnostic.



