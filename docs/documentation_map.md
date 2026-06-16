# Documentation Map

This document organizes the World Cup Market Intelligence documentation.

The goal is to help new visitors, reviewers and contributors understand where to start.

World Cup Market Intelligence is a public MVP for open-source prediction-market intelligence research around FIFA World Cup 2026.

It is for research and education only.

It is not betting advice or investment advice.

---

## Start here

Recommended reading order for first-time visitors:

1. README.md
2. docs/public_mvp.md
3. docs/stable_vs_experimental.md
4. docs/team_intelligence.md
5. docs/catalyst_notes_workflow.md
6. docs/narrative_intelligence.md
7. docs/historical_trends_workflow.md

---

## Public MVP overview

These documents explain the public product positioning.

- README.md
- docs/public_mvp.md
- docs/v1.0.0_roadmap.md

Use these when you want to understand:

- what the project is
- why it exists
- what the dashboards show
- what is stable
- what is experimental
- how the project should be interpreted

---

## Public dashboards

Public pages:

- docs/index.html
- docs/dashboard/index.html
- docs/polymarket-dashboard/index.html
- docs/trends-dashboard/index.html

Public URLs:

- https://laurentziuul.github.io/world-cup-market-intelligence/
- https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/
- https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/
- https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Dashboard meaning:

- Stable dashboard: reproducible manual CSV baseline
- Polymarket dashboard: experimental live provider dashboard
- Trends dashboard: historical signals, catalyst matches and team intelligence

---

## Core workflows

Stable manual CSV workflow:

- docs/stable_vs_experimental.md
- docs/providers.md
- scripts/update_snapshot_manual.py
- scripts/generate_dashboard.py

Experimental Polymarket workflow:

- docs/polymarket_live_workflow.md
- docs/polymarket_troubleshooting.md
- scripts/run_polymarket_live_workflow.py
- scripts/generate_polymarket_live_dashboard.py

Historical trends workflow:

- docs/historical_trends_architecture.md
- docs/historical_trends_workflow.md
- scripts/run_historical_trends_workflow.py
- scripts/generate_trends_dashboard.py

---

## Provider documentation

Provider-related documents:

- docs/providers.md
- docs/provider_status.md
- docs/api_provider_strategy.md
- docs/api_sources_matrix.md
- docs/first_api_provider_selection.md
- docs/provider_failure_modes.md
- docs/polymarket_live_workflow.md
- docs/polymarket_troubleshooting.md

Use these when you want to understand:

- available providers
- stable vs experimental providers
- provider failure modes
- how live provider workflows should be handled
- why the stable manual provider exists

---

## Catalyst notes documentation

Catalyst-related documents:

- docs/catalyst_notes_architecture.md
- docs/catalyst_notes_workflow.md
- docs/narrative_intelligence.md

Catalyst-related files:

- data/manual/catalyst_notes.csv
- examples/catalyst_notes_sample.csv
- src/wcmi/catalyst_notes.py
- scripts/validate_catalyst_notes.py
- scripts/match_catalyst_notes.py

Use these when you want to understand:

- how manual catalyst notes work
- how catalyst notes are validated
- how catalyst notes are matched to signals
- why catalyst notes do not prove causality
- why the system is manual-first

---

## Historical trends documentation

Historical trend documents:

- docs/historical_trends_architecture.md
- docs/historical_trends_workflow.md

Historical trend scripts:

- scripts/compare_snapshots.py
- scripts/generate_probability_deltas.py
- scripts/generate_top_movers.py
- scripts/generate_signal_summary.py
- scripts/match_catalyst_notes.py
- scripts/generate_team_intelligence.py
- scripts/run_historical_trends_workflow.py
- scripts/generate_trends_dashboard.py

Generated trend outputs:

- data/processed/snapshot_comparison_latest.csv
- data/processed/probability_deltas_latest.csv
- data/processed/top_movers_latest.csv
- data/processed/signal_summary_latest.csv
- data/processed/catalyst_matches_latest.csv
- data/processed/team_intelligence_latest.csv

These generated CSV outputs are ignored by Git.

---

## Team intelligence documentation

Team intelligence document:

- docs/team_intelligence.md

Team intelligence script:

- scripts/generate_team_intelligence.py

Generated output:

- data/processed/team_intelligence_latest.csv

Dashboard section:

- Team intelligence

Use this when you want to understand:

- how signals are aggregated by team
- how catalyst matches affect review priority
- why high priority means manual review, not betting advice
- how the trends dashboard prioritizes teams

---

## Validation and health checks

Validation script:

- scripts/validate_project.py

Health report script:

- scripts/project_health.py

Use validation when you want to check:

- required files
- Python syntax
- catalyst notes validation
- sample catalyst validation
- provider validation when available
- generated output ignore rules
- dashboard content
- safe command help

Use the health report when you want to inspect:

- providers
- dashboards
- documentation
- manual inputs
- generated outputs
- public URLs
- Git status

Commands:

- python scripts/validate_project.py
- python scripts/project_health.py

---

## Release notes

Release notes:

- docs/releases/v0.6.0.md
- docs/releases/v0.7.0.md
- docs/releases/v0.8.0.md
- docs/releases/v0.9.0.md

Future release notes:

- docs/releases/v1.0.0.md

Use these to understand what changed in each major milestone.

---

## Readiness checklists

Readiness checklists:

- docs/v0.6.0_readiness_checklist.md
- docs/v0.8.0_readiness_checklist.md
- docs/v0.9.0_readiness_checklist.md

Future checklist:

- docs/v1.0.0_readiness_checklist.md

Use these before tagging releases.

---

## Roadmaps

Roadmap documents:

- docs/v1.0.0_roadmap.md
- docs/v0.9.0_roadmap.md
- docs/v0.8.0_roadmap.md
- docs/v0.7.0_roadmap.md

Use these to understand the development direction.

---

## Stable vs experimental guide

Stable:

- manual_csv provider
- manual market CSV
- stable dashboard
- reproducible offline workflow

Experimental:

- Polymarket provider
- live provider dashboard
- historical trends
- catalyst notes
- narrative intelligence
- team intelligence

Stable means reproducible and safe.

Experimental means useful for research, but not guaranteed and not suitable for financial or betting decisions.

---

## Research-only interpretation

This project is:

- open-source
- educational
- transparent
- static-site friendly
- market-intelligence research
- manual-first for narrative context

This project is not:

- betting advice
- investment advice
- financial advice
- a prediction engine
- a trading bot
- a black-box model
- an automated news scraper

---

## Recommended contributor path

For a new contributor or reviewer:

1. Read README.md
2. Open the landing page
3. Open all three dashboards
4. Run python scripts/validate_project.py
5. Run python scripts/project_health.py
6. Read docs/public_mvp.md
7. Read docs/team_intelligence.md
8. Read docs/catalyst_notes_workflow.md
9. Read docs/historical_trends_workflow.md

---

## Status

Documentation map status:

- public MVP documentation map added
- ready for v1.0.0 hardening

Powered by Mayior Capital.
