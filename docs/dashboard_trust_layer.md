# Dashboard Trust Layer

The dashboard trust layer explains freshness, generated output status and provider reliability in World Cup Market Intelligence.

This layer helps users understand whether dashboard data is fresh, stale, missing or experimental.

It improves interpretation.

It does not make the project predictive.

It is not betting advice.

It is not investment advice.

---

## Purpose

A public intelligence dashboard should not only show data.

It should also show whether the data can be trusted.

The trust layer helps answer:

- When was the dashboard generated?
- Are generated outputs available?
- Are outputs missing?
- Are outputs stale?
- Which dashboards exist?
- Which provider layers are stable?
- Which provider layers are experimental?
- Should the viewer treat this page cautiously?

---

## Why freshness matters

Prediction-market data can become stale quickly.

A probability shown yesterday may not represent the current market.

A dashboard should clearly communicate:

- fresh data
- stale data
- missing data
- generated output availability
- experimental provider limitations

Freshness does not mean correctness.

Freshness only means the file was generated recently.

---

## Stable vs experimental trust

Stable layer:

- manual_csv provider
- manual CSV data
- stable dashboard
- reproducible offline workflow

Experimental layers:

- Polymarket live provider
- historical trends
- catalyst notes
- narrative intelligence
- team intelligence
- data freshness metadata

The stable layer is safer to publish.

The experimental layers are useful for research, but should not be overinterpreted.

---

## Data freshness utility

Script:

- scripts/check_data_freshness.py

Purpose:

- checks file existence
- checks last modified time
- marks files as fresh or stale
- reports missing outputs
- prints a terminal-only report

Run:

- python scripts/check_data_freshness.py

Optional commands:

- python scripts/check_data_freshness.py --stale-hours 24
- python scripts/check_data_freshness.py --show-stale-only
- python scripts/check_data_freshness.py --show-missing-only

Default stale threshold:

- 72 hours

A file older than the threshold is marked stale.

---

## Dashboard metadata generator

Script:

- scripts/generate_dashboard_metadata.py

Generated output:

- data/processed/dashboard_metadata_latest.json

This file is generated and ignored by Git.

Purpose:

- summarize dashboard availability
- summarize generated output availability
- identify stale outputs
- identify missing outputs
- expose warnings
- provide a machine-readable trust layer

Run:

- python scripts/generate_dashboard_metadata.py

Optional:

- python scripts/generate_dashboard_metadata.py --stale-hours 24

---

## Metadata fields

The metadata JSON includes fields such as:

- generated_at
- stale_threshold_hours
- public_dashboard_status
- stable_dashboard_available
- polymarket_dashboard_available
- trends_dashboard_available
- trend_outputs_available
- catalyst_outputs_available
- team_intelligence_available
- dashboard_available_count
- generated_output_available_count
- stale_dashboards
- missing_dashboards
- stale_outputs
- missing_outputs
- warnings
- dashboards
- generated_outputs
- manual_inputs
- interpretation
- powered_by

---

## Public dashboard status

The metadata generator can mark public dashboard status as:

- ready
- stale
- incomplete

Meaning:

- ready: dashboard files exist and are not stale
- stale: dashboard files exist but some are older than the configured threshold
- incomplete: one or more dashboard HTML files are missing

This is a trust indicator, not a prediction score.

---

## Trends dashboard trust panel

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

Dashboard file:

- docs/trends-dashboard/index.html

Dashboard generator:

- scripts/generate_trends_dashboard.py

The panel reads:

- data/processed/dashboard_metadata_latest.json

If metadata is missing, the dashboard still loads and shows a metadata warning.

---

## Generated outputs

Generated CSV outputs include:

- data/processed/snapshot_comparison_latest.csv
- data/processed/probability_deltas_latest.csv
- data/processed/top_movers_latest.csv
- data/processed/signal_summary_latest.csv
- data/processed/catalyst_matches_latest.csv
- data/processed/team_intelligence_latest.csv

Generated JSON metadata:

- data/processed/dashboard_metadata_latest.json

These generated files should be ignored by Git.

Dashboard HTML files may be committed intentionally when refreshing public pages.

---

## Missing outputs

Missing generated outputs can be normal.

For example, historical trend outputs may be missing if the historical workflow has not been run locally.

This does not mean the project is broken.

It means the related dashboard section may have no current generated data.

---

## Stale outputs

Stale outputs mean the file exists but is older than the configured threshold.

This can happen when:

- the workflow has not been run recently
- the dashboard has not been regenerated recently
- the repo is being viewed after a long period without updates

Stale data should be treated cautiously.

---

## Provider trust

Provider reliability differs by layer.

manual_csv:

- stable
- local
- reproducible
- best baseline

Polymarket and other live providers:

- experimental
- dependent on external APIs
- may change schema
- may fail due to network or availability
- should not be overclaimed

Provider health is summarized by:

- scripts/project_health.py

Run:

- python scripts/project_health.py

---

## Validation

The project validation script checks that the core project is healthy.

Script:

- scripts/validate_project.py

Run:

- python scripts/validate_project.py

Expected result:

- Result: PASS

Validation checks:

- required files
- Python syntax
- catalyst notes validation
- sample catalyst validation
- provider validation when available
- generated output ignore rules
- dashboard content
- safe command help

---

## Recommended trust workflow

Before publishing or tagging:

1. Run project validation
2. Run project health report
3. Generate dashboard metadata
4. Generate trends dashboard
5. Inspect the dashboard locally
6. Commit dashboard HTML only if intentionally refreshed

Commands:

- python scripts/validate_project.py
- python scripts/project_health.py
- python scripts/generate_dashboard_metadata.py
- python scripts/generate_trends_dashboard.py
- start docs/trends-dashboard/index.html

---

## Interpretation rules

Good wording:

- data appears fresh
- data appears stale
- output is missing
- provider is experimental
- dashboard is safe to inspect
- manual review is needed

Avoid wording:

- data is guaranteed correct
- stale data is useless
- fresh data is predictive
- provider output is always reliable
- dashboard implies betting edge

---

## Research-only position

The trust layer improves transparency.

It does not turn the project into:

- a betting model
- an investment system
- a prediction engine
- a causal inference system
- a trading bot

The project remains:

- open-source
- educational
- transparent
- static-site friendly
- research-oriented

---

## Current status

Dashboard trust layer status:

- data freshness utility added
- dashboard metadata generator added
- trends dashboard trust panel added
- provider health summary improved
- documentation added

Powered by Mayior Capital.
