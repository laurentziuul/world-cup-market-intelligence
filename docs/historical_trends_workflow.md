# Historical Trends Workflow

This document explains how to run the historical trends workflow in World Cup Market Intelligence.

The historical trends layer compares prediction-market snapshots over time and generates:

```text
snapshot comparison
probability deltas
top movers
signal summary
catalyst matches
historical trends dashboard
```

The goal is market intelligence, not betting advice.

---

## Purpose

The historical trends workflow is designed to answer questions such as:

```text
Which teams gained probability?
Which teams lost probability?
Which markets moved the most?
Which moves are supported by liquidity?
Which moves may be low-liquidity noise?
Which catalyst notes may explain the move?
```

---

## Required input

The workflow requires at least two processed snapshot CSV files.

Snapshot directory:

```text
data/processed/snapshots/
```

For Polymarket, this means running the live workflow at least twice over time:

```powershell
python scripts/run_polymarket_live_workflow.py
```

Each run may create a new Polymarket snapshot.

Catalyst notes are optional.

Catalyst notes file:

```text
data/manual/catalyst_notes.csv
```

If the catalyst notes file is empty, the workflow still works and can generate unmatched signal rows.

---

## Main workflow command

Run the historical trends workflow with:

```powershell
python scripts/run_historical_trends_workflow.py
```

Default behavior:

```text
provider = polymarket
outcome = Yes
status = existing
catalyst lookback = 7 days
```

This is optimized for Polymarket YES-only World Cup winner markets.

---

## Full command example

```powershell
python scripts/run_historical_trends_workflow.py --provider polymarket --outcome Yes --status existing
```

Optional parameters:

```powershell
python scripts/run_historical_trends_workflow.py --provider polymarket --outcome Yes --status existing --limit 10 --min-abs-change-pp 0.25 --catalyst-lookback-days 7
```

---

## What the workflow runs

The workflow runs six steps:

```text
1. compare latest two snapshots
2. generate probability delta report
3. generate top movers report
4. generate signal summary report
5. match catalyst notes to signals
6. generate historical trends dashboard
```

Equivalent manual commands:

```powershell
python scripts/compare_snapshots.py --provider polymarket
python scripts/generate_probability_deltas.py --provider polymarket --outcome Yes --status existing
python scripts/generate_top_movers.py --provider polymarket --outcome Yes
python scripts/generate_signal_summary.py --provider polymarket --outcome Yes
python scripts/match_catalyst_notes.py --provider polymarket --lookback-days 7 --include-unmatched
python scripts/generate_trends_dashboard.py
```

---

## Generated outputs

The workflow generates:

```text
data/processed/snapshot_comparison_latest.csv
data/processed/probability_deltas_latest.csv
data/processed/top_movers_latest.csv
data/processed/signal_summary_latest.csv
data/processed/catalyst_matches_latest.csv
docs/trends-dashboard/index.html
```

The CSV files are generated outputs and are ignored by Git by default.

The trends dashboard HTML file can be committed when the goal is to publish the latest experimental historical trends dashboard to GitHub Pages.

Public trends dashboard URL:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/
```

---

## Snapshot comparison

Script:

```text
scripts/compare_snapshots.py
```

Output:

```text
data/processed/snapshot_comparison_latest.csv
```

This compares the latest two snapshots for a provider.

It calculates:

```text
previous_probability
current_probability
probability_change
probability_change_pp
previous_volume
current_volume
volume_change
previous_liquidity
current_liquidity
liquidity_change
```

The most important column is:

```text
probability_change_pp
```

This means percentage-point change.

Example:

```text
0.15 → 0.17 = +2.00 pp
```

---

## Probability deltas

Script:

```text
scripts/generate_probability_deltas.py
```

Output:

```text
data/processed/probability_deltas_latest.csv
```

This converts raw snapshot comparison into a cleaner probability movement report.

It adds:

```text
previous_probability_display
current_probability_display
probability_change_display
direction
```

Direction can be:

```text
up
down
flat
```

---

## Top movers

Script:

```text
scripts/generate_top_movers.py
```

Output:

```text
data/processed/top_movers_latest.csv
```

This extracts:

```text
top positive probability movers
top negative probability movers
top volume movers
top liquidity movers
```

Example categories:

```text
top_positive_probability_movers
top_negative_probability_movers
top_volume_movers
top_liquidity_movers
```

---

## Signal summary

Script:

```text
scripts/generate_signal_summary.py
```

Output:

```text
data/processed/signal_summary_latest.csv
```

This classifies movements into transparent signal labels.

Default signal rules:

```text
>= +2.00 pp         = strong_positive_move
+0.75 to +1.99 pp   = moderate_positive_move
-0.74 to +0.74 pp   = flat_no_signal
-0.75 to -1.99 pp   = moderate_negative_move
<= -2.00 pp         = strong_negative_move
```

Liquidity labels include:

```text
low_liquidity_noise
rising_liquidity_support
falling_liquidity
normal_liquidity
liquidity_unknown
```

---

## Catalyst matches

Script:

```text
scripts/match_catalyst_notes.py
```

Input:

```text
data/processed/signal_summary_latest.csv
data/manual/catalyst_notes.csv
```

Output:

```text
data/processed/catalyst_matches_latest.csv
```

This matches manual catalyst notes to generated signal rows.

The matching logic uses:

```text
provider
team
market_id when available
date lookback window
```

Default lookback:

```text
7 days
```

The workflow runs catalyst matching with:

```powershell
python scripts/match_catalyst_notes.py --provider polymarket --lookback-days 7 --include-unmatched
```

The `--include-unmatched` flag keeps signal rows even when no catalyst note matches.

This is useful because the dashboard can still show that a signal exists, even if no explanatory catalyst has been added yet.

---

## Catalyst notes file

Manual catalyst notes live here:

```text
data/manual/catalyst_notes.csv
```

The sample file is here:

```text
examples/catalyst_notes_sample.csv
```

Validate catalyst notes with:

```powershell
python scripts/validate_catalyst_notes.py
```

Validate the sample file with:

```powershell
python scripts/validate_catalyst_notes.py --path examples/catalyst_notes_sample.csv
```

Catalyst notes are manual-first by design.

The project does not automatically scrape news or generate unsourced catalyst explanations.

---

## Important interpretation rule

A probability move is more meaningful when it is supported by liquidity.

Example:

```text
large probability move + rising liquidity = stronger signal
large probability move + low liquidity = possible noise
```

A catalyst note may help explain why a signal appeared.

Example:

```text
large probability move + rising liquidity + relevant match result = stronger narrative context
```

The signal system and catalyst system are intentionally simple and transparent.

They are not black-box trading models.

---

## Trends dashboard

Script:

```text
scripts/generate_trends_dashboard.py
```

Output:

```text
docs/trends-dashboard/index.html
```

Public URL:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/
```

The trends dashboard shows:

```text
trend output status
top movers
signal summary
catalyst matches
```

If trend CSV outputs are missing, the page still loads and shows the missing status.

If catalyst matches are missing, the page still loads and shows that no catalyst matches were found.

This makes the trends dashboard safe to publish even before enough historical snapshots or catalyst notes exist.

---

## If the workflow fails

Most common reason:

```text
not enough snapshots
```

The workflow requires at least two snapshot CSV files for the selected provider.

For Polymarket, run the live workflow more than once over time:

```powershell
python scripts/run_polymarket_live_workflow.py
```

Then rerun:

```powershell
python scripts/run_historical_trends_workflow.py
```

If catalyst notes validation fails, run:

```powershell
python scripts/validate_catalyst_notes.py
```

---

## Stable vs experimental

Stable provider:

```text
manual_csv
```

Experimental provider:

```text
polymarket
```

The historical trends workflow can support both, but the default configuration is currently optimized for:

```text
polymarket + Yes outcome + existing markets
```

---

## Clean generated outputs

The following trend CSV outputs are ignored by Git:

```text
data/processed/snapshot_comparison_latest.csv
data/processed/probability_deltas_latest.csv
data/processed/top_movers_latest.csv
data/processed/signal_summary_latest.csv
data/processed/catalyst_matches_latest.csv
```

To clean them manually:

```powershell
Remove-Item data\processed\snapshot_comparison_latest.csv -ErrorAction SilentlyContinue
Remove-Item data\processed\probability_deltas_latest.csv -ErrorAction SilentlyContinue
Remove-Item data\processed\top_movers_latest.csv -ErrorAction SilentlyContinue
Remove-Item data\processed\signal_summary_latest.csv -ErrorAction SilentlyContinue
Remove-Item data\processed\catalyst_matches_latest.csv -ErrorAction SilentlyContinue
```

If you do not want to publish a refreshed trends dashboard, restore it:

```powershell
git restore docs\trends-dashboard\index.html
```

---

## Current status

Historical trends workflow status:

```text
experimental
```

It is ready for local testing and now has a separate public preview dashboard with catalyst matching support.

Future work:

```text
add richer catalyst context to the trends dashboard
add signal labels directly to the Polymarket dashboard
add narrative intelligence documentation
add v0.8.0 release notes
```
