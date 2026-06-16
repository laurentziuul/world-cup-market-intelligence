# Team Intelligence

Team intelligence is an experimental summary layer in World Cup Market Intelligence.

It aggregates signal rows and catalyst matches by team.

The goal is to help identify which teams deserve manual review first.

This is not betting advice.

---

## Purpose

The team intelligence layer helps answer:

- Which teams have the most signals?
- Which teams have positive or negative movement?
- Which teams have catalyst context?
- Which teams have unmatched signals?
- Which teams should be reviewed manually first?

---

## Inputs

Team intelligence uses two generated files:

- data/processed/signal_summary_latest.csv
- data/processed/catalyst_matches_latest.csv

These are created by the historical trends workflow.

---

## Output

The team intelligence generator creates:

- data/processed/team_intelligence_latest.csv

This file is generated output and is ignored by Git.

---

## Generator script

Script:

- scripts/generate_team_intelligence.py

Run manually:

- python scripts/generate_team_intelligence.py

Run for a specific provider:

- python scripts/generate_team_intelligence.py --provider polymarket

The script is also integrated into:

- scripts/run_historical_trends_workflow.py

---

## Output columns

The generated team intelligence file includes:

- team
- provider
- total_signals
- positive_signals
- negative_signals
- flat_signals
- matched_catalysts
- unmatched_signals
- high_confidence_catalysts
- medium_confidence_catalysts
- low_confidence_catalysts
- strongest_signal
- latest_signal_date
- latest_catalyst_date
- summary_label
- review_priority

---

## Summary labels

The summary_label field gives a simple interpretation.

Current labels include:

- no_signals
- strong_signal_with_catalyst
- signal_with_catalyst
- strong_signal_needs_manual_review
- net_positive_attention
- net_negative_attention
- monitor

These labels are transparent rule-based labels.

They are not machine learning predictions.

---

## Review priority

The review_priority field helps sort teams by importance.

Current values:

- high
- medium
- low

High priority can mean:

- strong signal without catalyst context
- high-confidence catalyst exists

Medium priority can mean:

- medium-confidence catalyst exists
- unmatched signals exist
- signal exists with catalyst context

Low priority usually means:

- weak signal
- flat signal
- little or no catalyst context

---

## Dashboard integration

The trends dashboard reads:

- data/processed/team_intelligence_latest.csv

Dashboard generator:

- scripts/generate_trends_dashboard.py

Public dashboard section:

- Team intelligence

Dashboard path:

- docs/trends-dashboard/index.html

Public URL:

- https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

---

## Historical workflow integration

The historical trends workflow now runs:

- compare snapshots
- generate probability deltas
- generate top movers
- generate signal summary
- match catalyst notes
- generate team intelligence
- generate trends dashboard

Run:

- python scripts/run_historical_trends_workflow.py

---

## Why this matters

Before team intelligence, the dashboard showed individual signals and catalyst matches.

Team intelligence makes it easier to scan the whole market and ask:

- Which team deserves review first?
- Which signal has context?
- Which signal has no explanation yet?
- Which team is getting positive attention?
- Which team is getting negative attention?

This moves the project closer to a usable intelligence product.

---

## Interpretation rules

A high review priority does not mean a team is a good trade or bet.

It means the team deserves manual research.

Preferred wording:

- deserves review
- may need manual context
- has signal activity
- has catalyst context
- appears worth monitoring

Avoid wording:

- guaranteed edge
- sure bet
- prediction
- trading recommendation
- causality proven

---

## Design principles

The team intelligence layer is:

- simple
- transparent
- provider-aware
- static-site friendly
- compatible with generated CSV outputs
- useful for manual research

The team intelligence layer is not:

- a betting model
- a black-box score
- a causal inference engine
- an automated news system

---

## Current status

Team intelligence status:

- experimental
- integrated into historical workflow
- visible in trends dashboard

Powered by Mayior Capital.
