# Repo Presentation Checklist

This checklist helps verify that World Cup Market Intelligence is ready to be presented publicly as a portfolio-ready open-source MVP.

The project should look clear, credible, navigable and research-oriented.

It is not betting advice.

It is not investment advice.

It is not a prediction engine.

Powered by Mayior Capital.

---

## First impression

Check that a new visitor can quickly understand:

- what the project does
- why it exists
- what dashboards are available
- what is stable
- what is experimental
- how to run validation
- how to read the documentation
- why the project is research-only

---

## GitHub repository checklist

The GitHub repository should include:

- clear README
- public dashboard links
- documentation map
- release notes
- roadmap documents
- validation script
- project health script
- demo guide
- research-only disclaimer
- Mayior Capital branding

Required files:

- README.md
- docs/documentation_map.md
- docs/public_mvp.md
- docs/demo_guide.md
- scripts/validate_project.py
- scripts/project_health.py

---

## README checklist

README should clearly show:

- project summary
- public dashboard links
- current architecture
- stable vs experimental explanation
- quickstart
- core workflows
- catalyst notes
- narrative intelligence
- team intelligence
- dashboard trust layer
- generated outputs
- validation and health checks
- documentation map
- research-only disclaimer
- Powered by Mayior Capital

Command to inspect:

- Get-Content README.md -Head 120

---

## Public dashboard checklist

Public dashboard links:

- https://laurentziuul.github.io/world-cup-market-intelligence/
- https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/
- https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/
- https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Each public page should be readable and should not look broken.

The landing page should clearly show:

- Public MVP positioning
- Stable dashboard
- Polymarket live dashboard
- Historical trends dashboard
- Catalyst notes
- Team intelligence
- Research-only disclaimer
- Powered by Mayior Capital

---

## Stable dashboard checklist

Stable dashboard should communicate:

- manual CSV baseline
- reproducible data layer
- safe public layer
- World Cup market context
- Powered by Mayior Capital

File:

- docs/dashboard/index.html

---

## Polymarket dashboard checklist

Polymarket dashboard should communicate:

- experimental provider status
- live-provider caution
- probability / volume / liquidity context
- source links when available
- research-only interpretation
- Powered by Mayior Capital

File:

- docs/polymarket-dashboard/index.html

---

## Trends dashboard checklist

Trends dashboard should show:

- Data freshness and trust status
- Trend output status
- Team intelligence
- Top movers
- Signal summary
- Catalyst matches
- Powered by Mayior Capital

File:

- docs/trends-dashboard/index.html

The trust panel should show:

- public dashboard status
- metadata generated at
- stale threshold
- dashboards available
- generated outputs available
- warnings
- research-only interpretation

---

## Documentation checklist

Core documentation:

- docs/public_mvp.md
- docs/documentation_map.md
- docs/demo_guide.md
- docs/team_intelligence.md
- docs/catalyst_notes_workflow.md
- docs/narrative_intelligence.md
- docs/dashboard_trust_layer.md
- docs/historical_trends_workflow.md
- docs/stable_vs_experimental.md

Roadmaps:

- docs/v1.2.0_roadmap.md
- docs/v1.1.0_roadmap.md
- docs/v1.0.0_roadmap.md
- docs/v0.9.0_roadmap.md
- docs/v0.8.0_roadmap.md

Release notes:

- docs/releases/v1.1.0.md
- docs/releases/v1.0.0.md
- docs/releases/v0.9.0.md
- docs/releases/v0.8.0.md
- docs/releases/v0.7.0.md
- docs/releases/v0.6.0.md

---

## Validation checklist

Run:

- python scripts/validate_project.py

Expected:

- Result: PASS

Run:

- python scripts/project_health.py

Expected:

- report completes
- WARN for missing or stale generated outputs is acceptable
- Git status should be clean before final tag

Run:

- python scripts/check_data_freshness.py

Expected:

- report completes
- stale or missing outputs are informational

---

## Generated output checklist

Generated outputs should be ignored by Git:

- data/processed/snapshot_comparison_latest.csv
- data/processed/probability_deltas_latest.csv
- data/processed/top_movers_latest.csv
- data/processed/signal_summary_latest.csv
- data/processed/catalyst_matches_latest.csv
- data/processed/team_intelligence_latest.csv
- data/processed/dashboard_metadata_latest.json

Check:

- git check-ignore -v data/processed/dashboard_metadata_latest.json
- git check-ignore -v data/processed/team_intelligence_latest.csv

Generated CSV and JSON files should not be committed.

Dashboard HTML files may be committed intentionally when refreshing public pages.

---

## Demo readiness checklist

Before demo:

- run validation
- run project health report
- run data freshness check
- generate dashboard metadata
- generate trends dashboard
- open landing page
- open all three dashboards
- confirm public URLs work
- confirm README looks good on GitHub

Recommended commands:

- python scripts/validate_project.py
- python scripts/project_health.py
- python scripts/check_data_freshness.py
- python scripts/generate_dashboard_metadata.py
- python scripts/generate_trends_dashboard.py
- git status

---

## Branding checklist

The project should consistently mention:

- Powered by Mayior Capital

Pages/docs where branding should appear:

- README.md
- docs/index.html
- docs/dashboard/index.html
- docs/polymarket-dashboard/index.html
- docs/trends-dashboard/index.html
- major release notes
- demo guide
- final summary

---

## Research-only checklist

The project should clearly say it is not:

- betting advice
- investment advice
- financial advice
- prediction engine
- trading bot
- black-box model
- automated news scraper

The project should be framed as:

- open-source
- educational
- transparent
- market-intelligence research
- static dashboard MVP
- portfolio-ready proof-of-work

---

## Final Git checklist

Before release/tag:

- git status is clean
- validation passes
- release notes exist
- readiness checklist exists
- public pages are pushed
- generated outputs are ignored
- dashboard HTML refreshes are intentional

Expected final Git status:

- nothing to commit, working tree clean

---

## Status

Repo presentation checklist status:

- added for v1.2.0 final polish
- ready for portfolio review

Powered by Mayior Capital.
