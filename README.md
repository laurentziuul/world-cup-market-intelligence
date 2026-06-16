# World Cup Market Intelligence

Open-source market intelligence for FIFA World Cup 2026 prediction-market data.

World Cup Market Intelligence is a research project that combines:

- stable manual CSV data
- experimental live provider data
- historical probability movement
- signal classification
- catalyst notes
- narrative intelligence
- team intelligence
- static public dashboards

The project is designed to be transparent, reproducible and easy to inspect.

It is for research and education only.

It is not betting advice, investment advice, a prediction engine or a trading system.

Powered by Mayior Capital.

---

## Public dashboards

### Main landing page

https://laurentziuul.github.io/world-cup-market-intelligence/

### Stable dashboard

https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/

Purpose:

- stable manual CSV dashboard
- reproducible offline baseline
- safe public layer
- no live API dependency

### Polymarket live dashboard

https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/

Purpose:

- experimental live provider dashboard
- market probability view
- volume and liquidity context
- source links when available

### Historical trends dashboard

https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Purpose:

- historical probability movement
- top movers
- signal summary
- catalyst matches
- team intelligence

---

## What this project does

The project helps answer questions such as:

- Which World Cup teams are priced highest by prediction markets?
- Which teams are gaining or losing probability?
- Which moves are supported by liquidity?
- Which signals may deserve manual review?
- Which signals have possible catalyst context?
- Which teams deserve closer attention?

The project does not claim to predict match results.

The project does not recommend bets or trades.

---

## Current architecture

~~~text
manual_csv provider
    ↓
stable snapshot
    ↓
stable dashboard

polymarket provider
    ↓
experimental live snapshot
    ↓
polymarket dashboard

historical snapshots
    ↓
probability deltas
    ↓
top movers
    ↓
signal summary
    ↓
catalyst matches
    ↓
team intelligence
    ↓
historical trends dashboard
~~~

---

## Stable vs experimental

Stable layer:

- manual_csv provider
- manual CSV data
- stable dashboard
- reproducible offline workflow

Experimental layers:

- Polymarket live provider
- historical trends
- signal classification
- catalyst notes
- narrative intelligence
- team intelligence

The experimental layers are useful for research and product exploration, but they should not be treated as reliable predictions or trading signals.

---

## Quickstart

Create and activate a Python virtual environment, then install dependencies.

Typical local workflow:

~~~powershell
python scripts/validate_project.py
python scripts/project_health.py
~~~

Stable dashboard workflow:

~~~powershell
python scripts/update_snapshot_manual.py
python scripts/generate_dashboard.py
start docs\dashboard\index.html
~~~

Polymarket experimental workflow:

~~~powershell
python scripts/run_polymarket_live_workflow.py
start docs\polymarket-dashboard\index.html
~~~

Historical trends workflow:

~~~powershell
python scripts/run_historical_trends_workflow.py
start docs\trends-dashboard\index.html
~~~

The historical workflow requires at least two processed snapshots for the selected provider.

---

## Core workflows

### 1. Stable manual CSV workflow

Main files:

- data/manual/world_cup_markets.csv
- scripts/update_snapshot_manual.py
- scripts/generate_dashboard.py
- docs/dashboard/index.html

This is the reproducible baseline workflow.

### 2. Experimental Polymarket workflow

Main files:

- scripts/run_polymarket_live_workflow.py
- scripts/generate_polymarket_live_dashboard.py
- docs/polymarket-dashboard/index.html

This workflow depends on external provider data and may fail if the provider is unavailable.

### 3. Historical trends workflow

Main files:

- scripts/run_historical_trends_workflow.py
- scripts/compare_snapshots.py
- scripts/generate_probability_deltas.py
- scripts/generate_top_movers.py
- scripts/generate_signal_summary.py
- scripts/match_catalyst_notes.py
- scripts/generate_team_intelligence.py
- scripts/generate_trends_dashboard.py
- docs/trends-dashboard/index.html

This workflow powers the main intelligence dashboard.

---

## Catalyst notes

Catalyst notes are manual observations that may help explain market movement.

Main file:

- data/manual/catalyst_notes.csv

Sample file:

- examples/catalyst_notes_sample.csv

Validation:

~~~powershell
python scripts/validate_catalyst_notes.py
python scripts/validate_catalyst_notes.py --path examples\catalyst_notes_sample.csv
~~~

Catalyst notes may include:

- match results
- injuries
- squad announcements
- manager changes
- tactical changes
- media narrative shifts
- liquidity spikes
- bracket implications
- market structure observations

Catalyst notes do not prove causality.

They provide transparent research context.

---

## Narrative intelligence

Narrative intelligence connects market movement with possible real-world context.

It combines:

- probability movement
- liquidity context
- signal classification
- catalyst notes
- manual interpretation

Preferred language:

- may explain
- possibly linked to
- appears consistent with
- may have contributed to

Avoid language such as:

- caused by
- guaranteed
- certain
- betting edge
- sure prediction

---

## Team intelligence

Team intelligence aggregates signal rows and catalyst matches by team.

Main script:

- scripts/generate_team_intelligence.py

Generated output:

- data/processed/team_intelligence_latest.csv

Documentation:

- docs/team_intelligence.md

The Team intelligence section helps identify:

- teams with signal activity
- teams with positive movement
- teams with negative movement
- teams with catalyst context
- teams with unmatched signals
- teams that deserve manual review

High review priority means manual research is recommended.

It does not mean a betting recommendation.

---

## Generated outputs

Generated CSV outputs include:

- data/processed/snapshot_comparison_latest.csv
- data/processed/probability_deltas_latest.csv
- data/processed/top_movers_latest.csv
- data/processed/signal_summary_latest.csv
- data/processed/catalyst_matches_latest.csv
- data/processed/team_intelligence_latest.csv

These files are ignored by Git.

Dashboard HTML files may be committed intentionally when the goal is to publish refreshed public pages.

---

## Validation and health checks

Run safe local validation:

~~~powershell
python scripts/validate_project.py
~~~

This checks:

- required files
- Python syntax
- catalyst notes validation
- catalyst sample validation
- provider validation when available
- generated output ignore rules
- dashboard content
- safe command help

Run project health report:

~~~powershell
python scripts/project_health.py
~~~

This prints:

- providers
- dashboards
- documentation
- manual inputs
- generated outputs
- public URLs
- Git status

---

## Documentation map

Public MVP:

- docs/public_mvp.md

Roadmaps:

- docs/v1.0.0_roadmap.md
- docs/v0.9.0_roadmap.md
- docs/v0.8.0_roadmap.md

Catalyst and narrative docs:

- docs/catalyst_notes_architecture.md
- docs/catalyst_notes_workflow.md
- docs/narrative_intelligence.md

Team intelligence:

- docs/team_intelligence.md

Historical trends:

- docs/historical_trends_architecture.md
- docs/historical_trends_workflow.md

Provider docs:

- docs/providers.md
- docs/provider_status.md
- docs/api_provider_strategy.md
- docs/api_sources_matrix.md
- docs/first_api_provider_selection.md
- docs/polymarket_live_workflow.md
- docs/polymarket_troubleshooting.md
- docs/provider_failure_modes.md
- docs/stable_vs_experimental.md

Release notes:

- docs/releases/v0.6.0.md
- docs/releases/v0.7.0.md
- docs/releases/v0.8.0.md
- docs/releases/v0.9.0.md

Readiness checklists:

- docs/v0.6.0_readiness_checklist.md
- docs/v0.8.0_readiness_checklist.md
- docs/v0.9.0_readiness_checklist.md

---

## Research-only disclaimer

This project is:

- open-source
- educational
- research-oriented
- transparent
- static-site friendly
- manual-first for narrative context

This project is not:

- betting advice
- investment advice
- financial advice
- a trading bot
- a prediction engine
- a black-box model
- an automated news scraper

---

## Project status

Current phase:

- v1.0.0 public MVP hardening

Already included:

- stable dashboard
- experimental Polymarket dashboard
- historical trends dashboard
- catalyst notes
- narrative intelligence
- team intelligence
- project validation script
- project health report

Powered by Mayior Capital.


## Dashboard trust layer

v1.1.0 adds a data freshness and trust layer.

This layer helps visitors understand whether dashboard data is fresh, stale, missing or experimental.

Key trust-layer files:

- scripts/check_data_freshness.py
- scripts/generate_dashboard_metadata.py
- scripts/project_health.py
- docs/dashboard_trust_layer.md

Generated metadata output:

- data/processed/dashboard_metadata_latest.json

This metadata file is generated and ignored by Git.

The trends dashboard now includes:

- Data freshness and trust status

This panel shows:

- public dashboard status
- metadata generated time
- stale threshold
- dashboards available
- generated outputs available
- warnings
- research-only interpretation

Trust-layer commands:

- python scripts/check_data_freshness.py
- python scripts/generate_dashboard_metadata.py
- python scripts/project_health.py
- python scripts/validate_project.py

The trust layer improves transparency.

It does not make the project predictive.

It does not provide betting advice or investment advice.



## Monetization and Daily Brief layer

World Cup Market Intelligence is now also being developed as the first monetizable vertical of a broader event-intelligence engine.

Working umbrella concept:

- Mayior Event Intelligence

First use case:

- World Cup Market Intelligence

The first monetizable product is:

- World Cup Market Intelligence Daily Brief

This product is designed to summarize:

- top probability movers
- top liquidity movers
- top volume movers
- team review priority
- catalyst watchlist
- data freshness status
- dashboard links
- research-only interpretation

Key monetization docs and assets:

- docs/v1.3.0_monetization_roadmap.md
- docs/briefs/sample_world_cup_market_brief.md
- docs/briefs/latest.md
- docs/alert_formats.md
- docs/pro/index.html

Public Pro landing page:

- https://laurentziuul.github.io/world-cup-market-intelligence/pro/

Sample public brief:

- https://laurentziuul.github.io/world-cup-market-intelligence/briefs/sample_world_cup_market_brief.md

Latest generated brief:

- https://laurentziuul.github.io/world-cup-market-intelligence/briefs/latest.md

The monetization layer sells structure, context, prioritization and research workflow.

It does not sell betting tips, guaranteed signals, investment advice or prediction certainty.

## Final project status

Current public MVP release target:

- v1.2.0 — Final Polish and Portfolio-Ready MVP

Current status:

- stable dashboard available
- experimental Polymarket dashboard available
- historical trends dashboard available
- catalyst notes layer available
- narrative intelligence documentation available
- team intelligence layer available
- dashboard trust layer available
- project validation script available
- project health report available
- public demo guide available
- final project summary available

Public dashboards:

- https://laurentziuul.github.io/world-cup-market-intelligence/
- https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/
- https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/
- https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Recommended validation command:

- python scripts/validate_project.py

Recommended health check:

- python scripts/project_health.py

Recommended freshness check:

- python scripts/check_data_freshness.py

Best project description:

World Cup Market Intelligence is an open-source, static-dashboard MVP for FIFA World Cup 2026 prediction-market intelligence.

It combines market data, historical movement, signal classification, catalyst notes, team intelligence and dashboard trust indicators into a transparent public research product.

Final positioning:

- open-source market-intelligence MVP
- World Cup 2026 prediction-market research project
- transparent static dashboard system
- catalyst and narrative intelligence experiment
- team-level intelligence layer
- dashboard freshness and trust layer
- Mayior Capital proof-of-work project

This project is not:

- betting advice
- investment advice
- financial advice
- a prediction engine
- a trading bot
- a guaranteed signal system
- a black-box AI model

Powered by Mayior Capital.


