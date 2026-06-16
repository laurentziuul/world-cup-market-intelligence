# Operator Accounts

This document defines the internal operator accounts used for validating World Cup Market Intelligence as an operational research system.

These are strategy profiles.

They are not necessarily real platform accounts.

The purpose is to test whether market intelligence can support better research, cleaner decisions and measurable performance.

This layer is for personal research and controlled validation.

It is not betting advice.

It is not investment advice.

It is not financial advice.

It is not a prediction engine.

Powered by Mayior Capital.

---

## Data file

Operator account configuration:

- data/manual/operator_accounts.csv

This file defines:

- operator ID
- operator name
- mode
- risk profile
- primary signal
- confirmation requirement
- whether real-money testing is allowed
- max risk units
- description
- status

---

## Important rule

An operator account is not automatically a real-money account.

Default mode:

- paper

Real-money testing is allowed only when:

- explicitly marked
- manually reviewed
- risk is small
- decision is logged before execution
- no leverage is used
- data is fresh enough
- the operator is not the control account

---

## Operator list

### operator_01_momentum

Purpose:

- follows strong positive probability movement

Hypothesis:

- strong market momentum may continue when supported by volume or liquidity.

Default mode:

- paper

---

### operator_02_liquidity_confirmed

Purpose:

- acts only when probability movement is confirmed by liquidity expansion

Hypothesis:

- probability movement with liquidity support may be more meaningful than thin movement.

Default mode:

- paper

---

### operator_03_catalyst_confirmed

Purpose:

- acts only when a market signal has a matching catalyst note

Hypothesis:

- movement with catalyst context is more interpretable.

Default mode:

- paper

---

### operator_04_contrarian

Purpose:

- looks for negative overreaction or excessive positive movement

Hypothesis:

- markets may overreact to narratives, injuries or short-term sentiment.

Default mode:

- paper

Risk:

- high

---

### operator_05_top_teams_only

Purpose:

- only monitors high-profile teams

Hypothesis:

- major teams may have better liquidity, more information flow and more reliable pricing.

Default mode:

- paper

---

### operator_06_volume_spike

Purpose:

- follows unusual volume movement

Hypothesis:

- volume spikes can reveal attention shifts before broader repricing.

Default mode:

- paper

---

### operator_07_high_review_priority

Purpose:

- acts only on high review priority from team intelligence

Hypothesis:

- aggregated signals may be more useful than isolated movement.

Default mode:

- paper

---

### operator_08_low_risk_watchlist

Purpose:

- tracks candidates first and waits for confirmation

Hypothesis:

- waiting for confirmation reduces false positives.

Default mode:

- paper

Risk:

- low

---

### operator_09_human_discretionary

Purpose:

- allows a human decision after reviewing all available context

Inputs:

- daily brief
- trends dashboard
- catalyst notes
- team intelligence
- freshness status
- personal judgment

Default mode:

- paper

Real-money allowed:

- yes, but only micro-size and after manual review

Max real-money risk:

- 1 unit

---

### operator_10_no_trade_control

Purpose:

- control account

Behavior:

- never enters positions

Why it exists:

- compares active strategies against doing nothing
- prevents us from fooling ourselves
- shows whether activity is actually adding value

Default mode:

- paper

Real-money allowed:

- no

---

## How to use operator accounts

Daily workflow:

1. Generate the Daily Brief.
2. Review top movers.
3. Review liquidity and volume changes.
4. Review catalyst watchlist.
5. Review team intelligence.
6. Assign candidate ideas to one or more operator accounts.
7. Log a decision before any simulated or real action.
8. Track outcome and PnL later.

---

## Paper-first rule

All operators start in paper mode.

Real-money testing should be rare at the beginning.

Recommended split:

- 90 percent paper
- 10 percent real-money micro-test

Real-money testing should start only after the decision log exists.

---

## What we are testing

We are testing whether each strategy profile can help answer:

- Which signals are useful?
- Which filters reduce noise?
- Does liquidity confirmation matter?
- Do catalyst notes help?
- Does team intelligence improve decision quality?
- Does human discretion outperform mechanical filters?
- Is doing nothing better than acting?

---

## What we are not testing

We are not testing:

- guaranteed profit
- betting tips
- automated execution
- leverage
- revenge trading
- prediction certainty
- official tournament knowledge

---

## Final note

Operator accounts create discipline.

They force every decision to belong to a strategy profile.

This makes performance measurable instead of emotional.

Powered by Mayior Capital.
