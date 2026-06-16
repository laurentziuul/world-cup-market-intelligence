# Operator Validation Plan

This document defines the internal operator-validation layer for World Cup Market Intelligence and the broader Mayior Event Intelligence system.

The goal is to test whether the intelligence system can support real decision-making, portfolio monitoring and performance measurement.

This layer is for personal research and controlled validation.

It is not betting advice.

It is not investment advice.

It is not financial advice.

It is not a prediction engine.

Powered by Mayior Capital.

---

## Goal

The goal is to move from:

- dashboard
- daily brief
- product concept

to:

- operational research system
- strategy accounts
- decision logs
- simulated performance
- optional small real-money validation
- measurable results

The key question is:

Does the system help identify useful market opportunities before, during or after probability movement?

---

## Core pipeline

The operational pipeline is:

1. Collect market data.
2. Generate dashboard metadata.
3. Generate trends dashboard.
4. Generate daily brief.
5. Review top movers.
6. Assign signals to strategy accounts.
7. Log decisions.
8. Track simulated positions.
9. Optionally execute small real-money tests.
10. Measure performance.

---

## Important distinction

The system should separate:

- signal generation
- human interpretation
- simulated decision
- real-money decision
- position tracking
- performance analysis

A signal is not a trade.

A dashboard movement is not a recommendation.

A strategy account is not a real account.

A real-money test must be small, controlled and manually reviewed.

---

## Operator accounts

Use 10 internal operator accounts.

These are not necessarily real platform accounts.

They are strategy profiles used to test different decision rules.

### operator_01_momentum

Follows strong positive probability movement.

Hypothesis:

- strong market momentum may continue when supported by volume.

### operator_02_liquidity_confirmed

Only acts when probability movement is confirmed by liquidity expansion.

Hypothesis:

- probability movement with liquidity support is more meaningful than thin movement.

### operator_03_catalyst_confirmed

Only acts when a market signal has a matching catalyst note.

Hypothesis:

- movement with catalyst context is more interpretable.

### operator_04_contrarian

Looks for negative overreaction or excessive positive movement.

Hypothesis:

- markets may overreact to narratives, injuries or short-term sentiment.

### operator_05_top_teams_only

Only monitors high-profile teams.

Hypothesis:

- major teams may have better liquidity and more reliable pricing.

### operator_06_volume_spike

Follows unusual volume movement.

Hypothesis:

- volume spikes can reveal attention shifts before broader repricing.

### operator_07_high_review_priority

Acts only on high review priority from team intelligence.

Hypothesis:

- aggregated signals may be more useful than isolated movement.

### operator_08_low_risk_watchlist

Does not enter immediately. Tracks watchlist first.

Hypothesis:

- waiting for confirmation reduces false positives.

### operator_09_human_discretionary

Human decision after reviewing all dashboard and brief context.

Hypothesis:

- structured intelligence improves human discretionary decisions.

### operator_10_no_trade_control

Control account.

Does not act.

Purpose:

- compare active strategies against doing nothing.

---

## Paper vs real-money testing

Default mode:

- paper testing

Optional mode:

- small real-money validation

Recommended starting split:

- 90 percent simulated
- 10 percent real-money micro-test

Real-money rules:

- use only money you can afford to lose
- do not use leverage
- do not chase losses
- do not act on stale data
- do not act on a signal without manual review
- log every real decision before execution
- log every exit
- measure PnL honestly

---

## Position log

Each decision should include:

- date
- operator account
- market
- team or outcome
- signal type
- catalyst status
- probability at entry
- implied odds at entry
- position size
- paper or real
- entry reason
- exit plan
- result
- PnL
- notes

---

## Performance metrics

Track:

- number of decisions
- win rate
- average gain
- average loss
- total PnL
- max drawdown
- best operator account
- worst operator account
- false positive signals
- useful signal types
- useless signal types

---

## Minimum validation period

Do not judge after one day.

Minimum test:

- 7 days

Better test:

- 30 days

Best test:

- full tournament cycle

---

## Success criteria

The system is useful if:

- it improves research speed
- it identifies markets worth reviewing
- it reduces random decisions
- it creates a clean decision log
- it helps avoid stale-data mistakes
- at least one strategy account shows repeatable usefulness
- human discretionary decisions improve with the brief

The system is not useful if:

- signals are too noisy
- decisions are random
- catalyst notes add no value
- liquidity filters do not help
- manual review does not improve outcomes
- real-money tests create emotional decisions

---

## Initial bankroll rule

If real-money validation is used, start with a very small bankroll.

Example:

- total test bankroll: 100 units
- max risk per real decision: 1 to 2 units
- no leverage
- no compounding until 30-day review
- no revenge trading

This is for research discipline, not profit maximization.

---

## Daily operator workflow

Daily workflow:

1. Run data pipeline.
2. Generate Daily Brief.
3. Read top movers.
4. Check data freshness.
5. Check catalyst watchlist.
6. Assign candidate decisions to operator accounts.
7. Log paper decisions.
8. Decide if any real-money micro-test is justified.
9. Record decision before execution.
10. Review previous positions.

Commands:

- python scripts/generate_dashboard_metadata.py
- python scripts/generate_trends_dashboard.py
- python scripts/generate_daily_brief.py

---

## Final note

The purpose of this layer is to learn whether the intelligence system has operational value.

Even if it does not become a paid product, it can still become a personal research and investing workflow.

Powered by Mayior Capital.
