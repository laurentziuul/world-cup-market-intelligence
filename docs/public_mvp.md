# Public MVP

World Cup Market Intelligence is an open-source market intelligence project for FIFA World Cup 2026 prediction-market data.

The project combines:

- stable manual CSV data
- experimental live provider data
- historical probability movement
- signal classification
- catalyst notes
- narrative intelligence
- team intelligence
- static public dashboards

This document explains the public MVP version of the project.

It is for research and education only.

It is not betting advice.

It is not investment advice.

---

## What this project does

The project helps answer questions such as:

- Which teams are priced highest by the market?
- Which teams are gaining or losing probability?
- Which probability moves are supported by liquidity?
- Which signals may deserve manual review?
- Which signals have catalyst context?
- Which teams deserve closer attention?

The project does not claim to predict match results.

It does not tell users what to bet on.

It does not provide financial or investment recommendations.

---

## Public dashboards

The project currently exposes three main dashboard layers.

### Stable dashboard

Path:

- docs/dashboard/index.html

Public URL:

- https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/

Purpose:

- stable offline dashboard
- uses manual CSV data
- reproducible
- safe baseline
- does not require live API access

This is the most stable layer of the project.

### Polymarket live dashboard

Path:

- docs/polymarket-dashboard/index.html

Public URL:

- https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/

Purpose:

- experimental live provider dashboard
- uses Polymarket data when available
- shows market probabilities, volume, liquidity and source links

This layer is experimental because it depends on external provider data.

### Historical trends dashboard

Path:

- docs/trends-dashboard/index.html

Public URL:

- https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Purpose:

- compares snapshots over time
- shows probability movement
- shows top movers
- shows signal classification
- shows catalyst matches
- shows team intelligence

This is the main intelligence surface of the project.

---

## Stable vs experimental

Stable layer:

- manual_csv provider
- stable dashboard
- manual data file
- reproducible local workflow

Experimental layers:

- Polymarket live provider
- historical trends
- catalyst notes
- narrative intelligence
- team intelligence

The experimental layers are useful for research, but they should not be interpreted as reliable predictions or trading signals.

---

## Core workflows

### Stable workflow

The stable workflow uses local CSV data.

Typical files:

- data/manual/world_cup_markets.csv
- scripts/update_snapshot_manual.py
- scripts/generate_dashboard.py
- docs/dashboard/index.html

Purpose:

- reproducible baseline
- public stable dashboard

### Polymarket workflow

The Polymarket workflow uses live provider data when available.

Typical files:

- scripts/run_polymarket_live_workflow.py
- scripts/generate_polymarket_live_dashboard.py
- docs/polymarket-dashboard/index.html

Purpose:

- experimental live market dashboard
- provider-based research

### Historical trends workflow

The historical trends workflow compares snapshots over time.

Typical command:

- python scripts/run_historical_trends_workflow.py

Generated outputs:

- data/processed/snapshot_comparison_latest.csv
- data/processed/probability_deltas_latest.csv
- data/processed/top_movers_latest.csv
- data/processed/signal_summary_latest.csv
- data/processed/catalyst_matches_latest.csv
- data/processed/team_intelligence_latest.csv
- docs/trends-dashboard/index.html

Purpose:

- probability movement
- signal classification
- catalyst matching
- team-level review priorities

---

## Catalyst notes

Catalyst notes are manual observations that may help explain a market move.

Main file:

- data/manual/catalyst_notes.csv

Sample file:

- examples/catalyst_notes_sample.csv

Validation:

- python scripts/validate_catalyst_notes.py

Catalyst notes can include:

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

Narrative intelligence connects market movement with possible real-world explanations.

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

Team intelligence aggregates signals and catalyst matches by team.

Generated file:

- data/processed/team_intelligence_latest.csv

Script:

- scripts/generate_team_intelligence.py

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

Many files are generated and should not be manually edited.

Generated CSV outputs include:

- data/processed/snapshot_comparison_latest.csv
- data/processed/probability_deltas_latest.csv
- data/processed/top_movers_latest.csv
- data/processed/signal_summary_latest.csv
- data/processed/catalyst_matches_latest.csv
- data/processed/team_intelligence_latest.csv

These are ignored by Git.

Dashboard HTML files may be committed intentionally when the goal is to publish updated public pages.

---

## Local validation

Run the project validation script:

- python scripts/validate_project.py

This performs safe checks:

- no live API calls
- no scraping
- no full historical workflow
- Python syntax checks
- catalyst notes validation
- sample catalyst validation
- generated output ignore checks
- dashboard content checks
- safe help-command checks

Run the project health report:

- python scripts/project_health.py

This prints:

- provider status
- dashboard status
- documentation status
- manual input status
- generated output status
- public URLs
- Git status

---

## What this MVP can claim

The project can claim:

- open-source World Cup market intelligence
- static public dashboards
- stable manual CSV baseline
- experimental provider support
- transparent historical trend analysis
- catalyst-note matching
- team-level manual review prioritization
- reproducible local validation

The project should not claim:

- predictive accuracy
- betting edge
- investment advice
- guaranteed signals
- automated causal inference
- black-box AI prediction

---

## Who this is for

This project is useful for:

- builders
- researchers
- data analysts
- prediction-market observers
- open-source reviewers
- sports data enthusiasts
- people studying market narratives

It is not designed for:

- automated betting
- financial advice
- high-frequency trading
- guaranteed prediction systems

---

## Public MVP status

Current status:

- public MVP in progress
- stable dashboard available
- experimental Polymarket dashboard available
- experimental trends dashboard available
- catalyst notes integrated
- team intelligence integrated
- project validation script available
- project health report available

Powered by Mayior Capital.
