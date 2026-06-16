# Operator Performance Analysis

This document explains how to analyze operator decision performance for the internal validation layer.

The real performance summary should stay private.

Public repository:

- scripts/analyze_operator_performance.py
- docs/operator_performance_analysis.md
- examples/operator_decision_log_sample.csv

Private local files:

- data/private/operator_decision_log.csv
- data/private/operator_positions.csv
- data/private/operator_performance.csv
- data/private/operator_performance_summary.md

Powered by Mayior Capital.

---

## Purpose

The performance analyzer helps test whether World Cup Market Intelligence has operational value.

It answers:

- how many operator decisions were made
- which operator account produced decisions
- which signal types were used
- how many decisions were closed
- total PnL in internal units
- win rate
- result distribution
- whether one strategy profile performs better than others

---

## Command

Run:

- python scripts/analyze_operator_performance.py

Private output:

- data/private/operator_performance_summary.md

This output should not be committed.

---

## Why output is private

Operator performance may contain:

- private decision history
- real-money experiments
- PnL
- active strategy information
- notes that should not be public

The public repository should only contain:

- methodology
- scripts
- sample files
- documentation

---

## Input file

Default input:

- data/private/operator_decision_log.csv

The input file should contain decision rows created before or after operator decisions.

Every decision should include:

- operator ID
- market
- team or outcome
- signal type
- catalyst status
- probability at decision
- decision type
- paper or real mode
- position size
- risk units
- result
- PnL units
- notes

---

## Output file

Default output:

- data/private/operator_performance_summary.md

The output includes:

- high-level performance
- decisions by operator
- signal type distribution
- mode distribution
- result distribution
- status distribution
- interpretation notes

---

## Placeholder behavior

By default, placeholder rows are ignored.

This prevents example rows from polluting performance statistics.

To include placeholders for testing:

- python scripts/analyze_operator_performance.py --include-placeholders

---

## Operator comparison questions

Use the summary to ask:

- Does momentum work?
- Does liquidity confirmation help?
- Do catalyst-confirmed ideas perform better?
- Does contrarian logic work?
- Do high-priority team intelligence signals help?
- Does human discretionary review outperform mechanical filters?
- Is no-trade/control better than active decisions?

---

## Safety rules

Do not commit:

- private operator logs
- active positions
- wallet addresses
- account IDs
- API keys
- real-money PnL
- sensitive private notes

All real testing should be:

- small
- manually reviewed
- no leverage
- logged before execution
- measured honestly

---

## Final note

The performance analyzer turns the system from a dashboard into an operational research workflow.

The goal is not to prove that every signal works.

The goal is to discover which signals deserve attention and which signals are noise.

Powered by Mayior Capital.
