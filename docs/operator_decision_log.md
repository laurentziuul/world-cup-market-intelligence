# Operator Decision Log

This document explains how to log operator decisions for the internal validation layer.

The real decision logs should stay private.

Public repository:

- docs
- scripts
- templates
- examples
- sample rows

Private local data:

- data/private/operator_decision_log.csv
- data/private/operator_positions.csv
- data/private/operator_performance.csv

The private files should not be committed to GitHub.

Powered by Mayior Capital.

---

## Purpose

The decision log exists to test whether World Cup Market Intelligence can support disciplined decision-making.

The goal is to measure:

- which operator strategy generated the idea
- what signal triggered review
- whether catalyst context existed
- whether the decision was paper or real
- what risk was used
- what happened after entry
- whether the decision had positive or negative PnL
- which signals were useful
- which signals were noise

---

## Important rule

A signal is not a trade.

A dashboard movement is not a recommendation.

A Daily Brief item is not a betting tip.

Every decision must be logged before execution.

Real-money validation must be:

- small
- manual
- controlled
- no leverage
- no revenge trading
- logged before execution

---

## Private files

The private working files are:

- data/private/operator_decision_log.csv
- data/private/operator_positions.csv
- data/private/operator_performance.csv

These files may contain personal research notes, real-money decisions or sensitive PnL.

They must stay local or in a private repo.

---

## Public sample file

Public sample file:

- examples/operator_decision_log_sample.csv

This file contains fake example rows only.

It is safe to commit.

---

## Decision log columns

### date

Date of the decision.

### operator_id

Strategy profile that generated or owns the decision.

Examples:

- operator_01
- operator_02
- operator_03
- operator_09
- operator_10

### market

Market being reviewed.

Example:

- World Cup 2026 winner market

### team_or_outcome

Team, outcome or asset being reviewed.

### signal_type

Main reason the decision exists.

Examples:

- positive_probability_momentum
- probability_move_with_liquidity
- signal_with_catalyst
- overreaction_or_negative_move
- volume_spike
- high_review_priority
- human_discretionary_review
- no_trade_control

### catalyst_status

Whether catalyst context exists.

Examples:

- catalyst_matched
- no_catalyst
- manual_review_needed
- unknown

### probability_at_decision

Market-implied probability at decision time.

### implied_odds

Optional implied odds at decision time.

### decision_type

Examples:

- paper_entry
- real_entry
- watchlist_only
- no_trade
- exit
- reduce
- add

### mode

Examples:

- paper
- real

### position_size_units

Position size in internal units.

### risk_units

Risk amount in internal units.

### entry_reason

Short explanation of why the decision was made.

### exit_plan

What would invalidate or close the decision.

### status

Examples:

- open
- closed
- cancelled
- watchlist

### result

Examples:

- unknown
- win
- loss
- break_even
- no_trade

### pnl_units

PnL measured in internal units.

### notes

Any additional private or public-safe notes.

---

## How to use daily

Daily workflow:

1. Generate dashboard metadata.
2. Generate trends dashboard.
3. Generate Daily Brief.
4. Review top movers and team intelligence.
5. Assign candidate ideas to operator accounts.
6. Add decision rows before execution.
7. Mark paper or real mode.
8. Review open positions.
9. Update result and PnL later.
10. Analyze performance weekly.

---

## Safety rules

Do not commit:

- real-money PnL
- active positions
- real account IDs
- platform usernames
- wallet addresses
- API keys
- private notes
- sensitive personal data

Use public examples only.

---

## Final note

The operator decision log is the bridge between intelligence and performance.

It helps separate disciplined research from emotional action.

Powered by Mayior Capital.
