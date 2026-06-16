# Operator Decision Helper

This document explains how to use the operator decision log helper.

The helper appends rows to the private decision log:

- data/private/operator_decision_log.csv

The script is public.

The decision log is private.

Powered by Mayior Capital.

---

## Purpose

The helper exists so operator decisions can be logged consistently.

Every paper or real-money decision should be logged before execution.

The goal is discipline.

A signal is not a trade.

A dashboard movement is not a recommendation.

A Daily Brief item is not betting advice.

---

## Script

Public script:

- scripts/log_operator_decision.py

Private output:

- data/private/operator_decision_log.csv

The private output should not be committed.

---

## Basic usage

Example paper decision:

- python scripts/log_operator_decision.py --operator-id operator_01 --market "World Cup 2026 winner market" --team-or-outcome "Example Team" --signal-type positive_probability_momentum --catalyst-status no_catalyst --probability 0.120 --implied-odds 8.33 --decision-type paper_entry --mode paper --position-size-units 1 --risk-units 0 --entry-reason "Example momentum decision" --exit-plan "Review after next snapshot"

Example no-trade decision:

- python scripts/log_operator_decision.py --operator-id operator_10 --market "World Cup 2026 winner market" --team-or-outcome "Example Team" --signal-type no_trade_control --decision-type no_trade --mode paper --position-size-units 0 --risk-units 0 --entry-reason "No clear signal" --exit-plan "n/a" --status closed --result no_trade

---

## Dry run

Use dry run before writing:

- python scripts/log_operator_decision.py --operator-id operator_10 --market "example_market" --team-or-outcome "Example Team" --signal-type no_trade_control --decision-type no_trade --mode paper --position-size-units 0 --risk-units 0 --entry-reason "Testing helper" --exit-plan "n/a" --status closed --result no_trade --dry-run

Dry run prints the row but does not write to the private CSV.

---

## Operator validation

By default, the script checks operator IDs against:

- data/manual/operator_accounts.csv

If an operator ID is not found, the script stops.

This prevents accidental typos.

To override:

- --allow-unknown-operator

Use override only for testing.

---

## Private data rule

Do not commit:

- real-money decisions
- PnL
- active positions
- private notes
- account IDs
- wallet addresses
- platform usernames
- personal financial details

The public repo should contain only:

- scripts
- docs
- templates
- examples
- methodology

---

## Recommended daily use

Daily process:

1. Generate Daily Brief.
2. Review top movers.
3. Pick operator account.
4. Decide paper or real mode.
5. Run helper with dry run.
6. If correct, run helper without dry run.
7. Review private log.
8. Later analyze performance.

---

## Performance analysis

After logging decisions, run:

- python scripts/analyze_operator_performance.py

Private output:

- data/private/operator_performance_summary.md

This helps compare operator strategies.

---

## Final note

The helper makes decision logging easier, but it does not make decisions for you.

The operator still needs manual review, risk control and discipline.

Powered by Mayior Capital.
