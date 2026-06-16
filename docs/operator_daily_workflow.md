# Operator Daily Workflow

This document defines the daily operating workflow for using World Cup Market Intelligence as a personal research and decision-support system.

This workflow is for internal operator validation.

It supports paper testing and optional small real-money research.

It is not betting advice.

It is not investment advice.

It is not financial advice.

It is not a prediction engine.

Powered by Mayior Capital.

---

## Purpose

The purpose of the daily workflow is to create discipline.

The system should help answer:

- what changed in the market
- which teams deserve review
- which signals are noisy
- which signals are supported by liquidity
- which signals have catalyst context
- which operator strategy would act
- whether a decision should be paper only or real-money micro-test
- how performance should be measured

A signal is not a decision.

A decision must be logged before execution.

---

## Daily operating rule

Do not act before running the workflow.

The daily order is:

1. Generate or refresh data.
2. Check freshness.
3. Generate dashboards.
4. Generate Daily Brief.
5. Review signals.
6. Assign candidate decisions to operator accounts.
7. Log decisions.
8. Decide paper or real mode.
9. Execute only if rules allow it.
10. Review open positions.
11. Update performance.

---

## Step 1 — Run safe validation

Run:

- python scripts/validate_project.py

Expected:

- Result: PASS

If validation fails, stop.

Do not make decisions from a broken system.

---

## Step 2 — Refresh trust metadata

Run:

- python scripts/generate_dashboard_metadata.py

Purpose:

- updates dashboard trust metadata
- checks dashboard availability
- checks generated output availability
- helps detect stale or missing data

If metadata warns about missing or stale data, continue only with caution.

---

## Step 3 — Refresh trends dashboard

Run:

- python scripts/generate_trends_dashboard.py

Purpose:

- updates public trends dashboard
- refreshes team intelligence display
- refreshes catalyst matches display
- refreshes trust panel

If the dashboard is stale, do not overinterpret signals.

---

## Step 4 — Generate Daily Brief

Run:

- python scripts/generate_daily_brief.py

Outputs:

- docs/briefs/latest.md
- docs/briefs/YYYY-MM-DD.md

Read:

- executive summary
- top probability movers
- top liquidity movers
- top volume movers
- teams requiring manual review
- catalyst watchlist
- freshness status
- warnings and limitations

---

## Step 5 — Review market movement

Review the Daily Brief and dashboard.

Look for:

- large probability moves
- liquidity confirmation
- volume spikes
- catalyst matches
- repeated movement across snapshots
- team review priority
- stale data warnings
- missing output warnings

Do not act on one number alone.

---

## Step 6 — Map signal to operator account

Assign each candidate idea to an operator strategy.

Examples:

- strong probability move = operator_01_momentum
- probability move with liquidity = operator_02_liquidity_confirmed
- signal with catalyst = operator_03_catalyst_confirmed
- overreaction idea = operator_04_contrarian
- major team only = operator_05_top_teams_only
- volume spike = operator_06_volume_spike
- high review priority = operator_07_high_review_priority
- wait for confirmation = operator_08_low_risk_watchlist
- full human review = operator_09_human_discretionary
- no action = operator_10_no_trade_control

If no operator account fits, do not act.

---

## Step 7 — Decide paper or real mode

Default:

- paper

Real mode is allowed only if:

- decision is manually reviewed
- data is fresh enough
- position is small
- no leverage is used
- decision is logged before execution
- operator allows real-money testing
- you can accept full loss
- you are calm and not chasing

Real mode should be rare at the beginning.

Recommended starting rule:

- 90 percent paper
- 10 percent real-money micro-test

---

## Step 8 — Log decision before execution

Private file:

- data/private/operator_decision_log.csv

Every decision should be logged before action.

Required fields:

- date
- operator_id
- market
- team_or_outcome
- signal_type
- catalyst_status
- probability_at_decision
- implied_odds
- decision_type
- mode
- position_size_units
- risk_units
- entry_reason
- exit_plan
- status
- result
- pnl_units
- notes

If it is not logged, it does not count.

---

## Step 9 — Update open positions

Private file:

- data/private/operator_positions.csv

Update:

- open positions
- current probability
- position status
- unrealized PnL
- realized PnL
- notes

Do not keep positions only in your head.

---

## Step 10 — Analyze performance

Run:

- python scripts/analyze_operator_performance.py

Private output:

- data/private/operator_performance_summary.md

Review:

- total decisions
- decisions by operator
- win rate
- total PnL units
- signal type distribution
- mode distribution
- result distribution

Do not judge strategy quality from one trade.

Minimum review period:

- 7 days

Better review period:

- 30 days

---

## Daily checklist

Before any decision:

- validation passed
- data freshness checked
- dashboard refreshed
- Daily Brief generated
- signal reviewed
- catalyst status checked
- liquidity or volume checked
- operator account selected
- paper or real mode decided
- decision logged before execution
- exit plan written
- position size controlled

If any item is missing, do not act.

---

## Real-money micro-test rules

If using real money:

- no leverage
- no emotional entries
- no revenge trading
- no doubling down blindly
- no stale-data decisions
- no oversized positions
- no acting without a written exit plan
- no acting outside operator rules

Suggested unit system:

- total test bankroll = 100 units
- normal paper decision = 1 unit
- real-money micro-test = 0.5 to 1 unit
- max risk per real decision = 1 to 2 units
- no compounding during first 30 days

The purpose is learning, not profit maximization.

---

## No-trade is a valid decision

Operator:

- operator_10_no_trade_control

Use no-trade when:

- signal is unclear
- data is stale
- liquidity is weak
- catalyst is missing
- market looks noisy
- you are tired
- you are emotional
- setup does not fit any strategy

No-trade decisions should also be logged when useful.

They create a control group.

---

## Weekly review

Once per week, review:

- which operators made decisions
- which operators performed best
- which signals were noisy
- which signals were useful
- whether catalyst confirmation helped
- whether liquidity confirmation helped
- whether human discretion helped
- whether no-trade would have been better
- whether real-money testing should continue or pause

Run:

- python scripts/analyze_operator_performance.py

Then read:

- data/private/operator_performance_summary.md

---

## Stop conditions

Stop real-money testing immediately if:

- validation fails
- data is stale
- you feel emotional
- you are chasing losses
- you increase size without a plan
- you ignore the decision log
- you act without an exit plan
- you cannot explain the decision in one paragraph
- performance review shows repeated errors

Paper testing can continue.

---

## What success looks like

Success does not mean instant profit.

Success means:

- cleaner decisions
- fewer random actions
- better review discipline
- clear performance tracking
- understanding which signals matter
- avoiding stale-data mistakes
- identifying one or two useful operator strategies
- building confidence in the system before scaling

---

## What failure looks like

Failure signs:

- signals are too noisy
- decisions are emotional
- no strategy profile is useful
- paper and real decisions diverge too much
- catalyst notes do not help
- liquidity confirmation does not help
- performance cannot be measured
- the log is not updated honestly

If this happens, pause real-money testing and improve the system.

---

## Daily command sequence

Recommended daily commands:

- python scripts/validate_project.py
- python scripts/generate_dashboard_metadata.py
- python scripts/generate_trends_dashboard.py
- python scripts/generate_daily_brief.py
- python scripts/analyze_operator_performance.py
- git status

Public generated files may change.

Private files should remain ignored by Git.

---

## Privacy and GitHub rule

Do not commit:

- real-money PnL
- active positions
- private decision notes
- wallet addresses
- platform account IDs
- screenshots with balances
- private usernames
- personal financial details

Keep private research in:

- data/private/

Public repo should contain:

- methodology
- docs
- scripts
- examples
- sample rows only

---

## Final note

The daily workflow turns the project into an operating system for decision quality.

The goal is not to always be right.

The goal is to make every decision measurable, reviewable and improvable.

Powered by Mayior Capital.
