# Polymarket Live Workflow

This document explains the experimental Polymarket live workflow in World Cup Market Intelligence.

The Polymarket provider is a live API provider.
It requires network access and may depend on DNS, Cloudflare behavior, geo access or VPN availability.

The stable default workflow remains:

```text
manual_csv
```

---

## Status

Current status:

```text
experimental
```

Provider name:

```text
polymarket
```

Workflow script:

```text
scripts/run_polymarket_live_workflow.py
```

Public experimental dashboard:

```text
docs/polymarket-dashboard/index.html
```

GitHub Pages URL:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/
```

---

## What the workflow does

The live workflow runs four steps:

```text
validate experimental Polymarket provider
    ↓
update Polymarket live snapshot
    ↓
generate Polymarket YES-only World Cup ranking
    ↓
generate separate Polymarket live dashboard
```

It produces live outputs based on Polymarket Gamma API data.

---

## Command

Run the complete live workflow with:

```powershell
python scripts/run_polymarket_live_workflow.py
```

If access fails, try again later or use VPN.

During testing, Polymarket access worked with Proton VPN using a Moldova server.

---

## Generated outputs

The workflow may generate or update:

```text
data/processed/snapshot_latest.csv
data/processed/snapshots/*-polymarket.csv
data/processed/polymarket_worldcup_yes_ranking.csv
data/processed/polymarket_worldcup_yes_ranking_summary.txt
docs/polymarket-dashboard/index.html
```

The processed CSV and summary files are generated outputs.

The dashboard HTML file can be committed when the goal is to publish the latest experimental Polymarket dashboard to GitHub Pages.

---

## Stable workflow remains manual CSV

The stable offline workflow is still:

```powershell
python scripts/smoke_test_pipeline.py --provider manual_csv
```

The stable dashboard remains:

```text
docs/dashboard/index.html
```

Stable dashboard URL:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/
```

This should remain the default reproducible workflow.

---

## Polymarket provider validation

Validate the experimental provider with:

```powershell
python scripts/validate_providers.py --provider polymarket --include-live
```

Expected result:

```text
Result: PASS
```

If validation fails because of network, DNS, timeout, Cloudflare or geo access, this does not mean the stable project is broken.

It means the live provider is temporarily unavailable.

---

## Polymarket live snapshot

Generate a live Polymarket snapshot with:

```powershell
python scripts/update_snapshot.py --provider polymarket
```

This creates a live snapshot using the experimental Polymarket provider.

The provider currently:

```text
fetches live markets from Polymarket Gamma API
filters World Cup / FIFA markets
normalizes each outcome into the provider contract
outputs rows compatible with the snapshot pipeline
```

---

## YES-only ranking

Generate the Polymarket World Cup YES-only ranking with:

```powershell
python scripts/generate_polymarket_yes_ranking.py
```

This keeps only useful winner-market rows:

```text
outcome = Yes
market_title = Will X win the 2026 FIFA World Cup?
```

This is useful because winner markets also contain `No` rows, and those usually dominate raw sorted tables.

---

## Separate Polymarket live dashboard

Generate the separate experimental dashboard with:

```powershell
python scripts/generate_polymarket_live_dashboard.py
```

This writes:

```text
docs/polymarket-dashboard/index.html
```

The page is separate from the stable manual CSV dashboard.

Stable manual dashboard:

```text
docs/dashboard/index.html
```

Experimental Polymarket dashboard:

```text
docs/polymarket-dashboard/index.html
```

---
## Optional historical trends

The Polymarket live workflow can optionally run the historical trends workflow.

Default command:

```powershell
python scripts/run_polymarket_live_workflow.py
```

This runs:

```text
provider validation
live snapshot generation
YES-only ranking generation
separate Polymarket dashboard generation
```

Optional trends command:

```powershell
python scripts/run_polymarket_live_workflow.py --include-trends
```

This runs the same live workflow, plus:

```text
snapshot comparison
probability delta report
top movers report
signal summary report
```

The optional trends step requires at least two processed Polymarket snapshot CSV files.

Relevant generated trend outputs:

```text
data/processed/snapshot_comparison_latest.csv
data/processed/probability_deltas_latest.csv
data/processed/top_movers_latest.csv
data/processed/signal_summary_latest.csv
```

These files are generated outputs and are ignored by Git by default.

Use `--include-trends` only when historical Polymarket snapshots already exist.

A failure in the optional trend step usually means there are not enough snapshots yet, not that the stable project is broken.

## Recommended live workflow

For live Polymarket testing, use:

```powershell
python scripts/run_polymarket_live_workflow.py
```

For stable offline testing, use:

```powershell
python scripts/smoke_test_pipeline.py --provider manual_csv
```

---

## Current recommendation

Use `manual_csv` for stable reproducible work.

Use `polymarket` only for experimental live market intelligence.

Do not promote `polymarket` to stable until:

* it works repeatedly without manual intervention;
* false-positive market filtering remains low;
* network failure handling is tested;
* raw response caching is implemented or planned;
* generated live outputs are clearly separated from stable manual outputs;
* the separate Polymarket dashboard remains reliable across multiple runs.
