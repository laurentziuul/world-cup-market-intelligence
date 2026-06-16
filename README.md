# World Cup Market Intelligence v0

Open-source market-intelligence framework for tracking prediction-market prices, liquidity, narratives, catalysts, historical probability trends and signal intelligence around the FIFA World Cup 2026.

This project is not a betting system and does not provide betting tips.

The goal is to study how crowds price uncertainty during a scheduled global attention event.

---

## Why this exists

FIFA World Cup 2026 is a useful case study because it has:

* a fixed start and end date;
* global attention;
* prediction markets;
* public narratives;
* liquidity shifts;
* scheduled catalysts;
* measurable probability changes.

The long-term goal is to build a reusable event-intelligence framework that can later be adapted to other global events such as elections, FOMC meetings, CPI releases, crypto unlocks, AI conferences, geopolitical events and major sports tournaments.

---

## What the project does

The project supports a market-intelligence pipeline:

```text
provider
    â†“
normalized snapshot
    â†“
timestamped snapshot archive
    â†“
historical trend engine
    â†“
signal classification
    â†“
dashboard / reports
```

Current capabilities:

* ingest a manual CSV watchlist;
* normalize market data into a standard snapshot;
* archive timestamped snapshots;
* calculate snapshot-to-snapshot price, volume and liquidity changes;
* generate historical trend summaries;
* generate probability delta reports;
* generate top movers reports;
* generate signal classification summaries;
* generate a stable manual CSV dashboard;
* generate an experimental Polymarket live dashboard;
* generate an experimental historical trends dashboard;
* separate market data from narrative interpretation;
* use a provider abstraction layer so new data sources can be added later.

---

## Current architecture

The project currently separates stable and experimental workflows.

```text
manual_csv      = stable offline provider
polymarket      = experimental live API provider
trend workflow  = experimental historical signal intelligence
```

Stable layer:

```text
manual_csv
```

Experimental live layer:

```text
polymarket
```

Experimental intelligence layer:

```text
historical trends + top movers + signal summary
```

This separation is intentional.

Live provider failures should not be treated as stable project failures.

---

## Public pages

Main GitHub Pages landing page:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/
```

Stable manual CSV dashboard:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/
```

Experimental Polymarket live dashboard:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/
```

Experimental historical trends dashboard:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/
```

---

## Dashboards

World Cup Market Intelligence currently has three public dashboards.

### Stable manual CSV dashboard

```text
Provider: manual_csv
Status: stable
Workflow: offline / reproducible
```

Public URL:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/dashboard/
```

This is the default stable dashboard. It is generated from manually curated CSV data and does not require live API access.

### Experimental Polymarket live dashboard

```text
Provider: polymarket
Status: experimental
Workflow: live API / network-dependent
```

Public URL:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/polymarket-dashboard/
```

This dashboard uses live Polymarket Gamma API data and generates a YES-only ranking for markets matching:

```text
Will X win the 2026 FIFA World Cup?
```

The Polymarket dashboard is intentionally separate from the stable manual CSV dashboard.

### Experimental historical trends dashboard

```text
Provider: polymarket by default
Status: experimental
Workflow: historical snapshots / signal intelligence
```

Public URL:

```text
https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/
```

This dashboard shows the experimental historical trends layer:

```text
probability movement
top movers
signal summary
trend output status
```

The trends dashboard is generated from historical snapshot comparison outputs and is safe to publish even when trend CSV files are missing.

---

## Current data providers

The stable default provider is:

```text
manual_csv
```

The first experimental live provider is:

```text
polymarket
```

Planned future providers:

```text
predict_fun
kalshi
manifold
custom_csv
other APIs
```

Provider documentation:

```text
docs/providers.md
docs/provider_status.md
docs/api_provider_strategy.md
docs/api_sources_matrix.md
docs/stable_vs_experimental.md
```

The core principle is that each provider can have different raw data, but every provider must return the same normalized internal format before entering the snapshot, trend, dashboard and brief pipeline.

---

## Important files

Manual input file:

```text
data/manual/world_cup_markets.csv
```

Generated latest snapshot:

```text
data/processed/snapshot_latest.csv
```

Generated timestamped snapshot archive:

```text
data/processed/snapshots/
```

Generated stable trend file:

```text
data/processed/trends_latest.csv
```

Generated brief:

```text
briefs/YYYY-MM-DD-world-cup-market-brief.md
```

Stable dashboard:

```text
docs/dashboard/index.html
```

Experimental Polymarket dashboard:

```text
docs/polymarket-dashboard/index.html
```

Experimental trends dashboard:

```text
docs/trends-dashboard/index.html
```

---

## Quickstart

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project locally:

```powershell
python -m pip install -e .
```

Create a provider-based snapshot using the default manual CSV provider:

```powershell
python scripts/update_snapshot.py --provider manual_csv
```

The old manual command still works as a compatibility wrapper:

```powershell
python scripts/update_snapshot_manual.py
```

Generate historical trends for the stable manual workflow:

```powershell
python scripts/generate_trends.py
```

Generate the daily brief:

```powershell
python scripts/generate_brief.py
```

Generate the stable dashboard:

```powershell
python scripts/generate_dashboard.py
```

Open the stable dashboard locally:

```powershell
start docs/dashboard/index.html
```

---

## Provider-based snapshot update

The default provider is `manual_csv`:

```powershell
python scripts/update_snapshot.py --provider manual_csv
```

The old manual command still works as a compatibility wrapper:

```powershell
python scripts/update_snapshot_manual.py
```

List all available providers:

```powershell
python scripts/update_snapshot.py --list-providers
```

Provider documentation:

```text
docs/providers.md
```

---

## Provider validation

Validate all offline providers:

```powershell
python scripts/validate_providers.py
```

Validate one provider only:

```powershell
python scripts/validate_providers.py --provider manual_csv
```

Validate the experimental Polymarket provider with live access:

```powershell
python scripts/validate_providers.py --provider polymarket --include-live
```

Live or network-based providers are skipped by default.

---

## Provider sample export

Export a normalized provider sample:

```powershell
python scripts/export_provider_sample.py --provider manual_csv
```

Sample outputs are stored in:

```text
examples/provider_outputs/
```

The current manual CSV sample is:

```text
examples/provider_outputs/manual_csv_normalized_sample.csv
```

---

## Stable workflow

Run the stable offline smoke test with:

```powershell
python scripts/smoke_test_pipeline.py --provider manual_csv
```

This validates the provider, exports a normalized provider sample, updates the latest snapshot, regenerates trends and rebuilds the stable dashboard.

The stable workflow is:

```text
offline
reproducible
manual-data based
safe for demos
safe for documentation
safe for smoke testing
```

Use this workflow when the goal is to prove that the core project works reliably.

---

## Experimental Polymarket live workflow

Run the experimental Polymarket live workflow with:

```powershell
python scripts/run_polymarket_live_workflow.py
```

This workflow runs:

```text
provider validation
live snapshot generation
YES-only World Cup ranking generation
separate Polymarket dashboard generation
```

To include historical trend generation when enough snapshots exist:

```powershell
python scripts/run_polymarket_live_workflow.py --include-trends
```

This adds:

```text
snapshot comparison
probability delta report
top movers report
signal summary report
historical trends dashboard generation
```

The Polymarket workflow depends on live network access and may require VPN depending on DNS, Cloudflare behavior, geo access or provider availability.

Polymarket documentation:

```text
docs/polymarket_live_workflow.md
docs/polymarket_troubleshooting.md
docs/provider_failure_modes.md
```

---

## Historical trends workflow

The historical trends workflow compares snapshots over time and generates movement intelligence.

Run it with:

```powershell
python scripts/run_historical_trends_workflow.py
```

Default behavior:

```text
provider = polymarket
outcome = Yes
status = existing
```

The workflow runs:

```text
compare latest two snapshots
generate probability delta report
generate top movers report
generate signal summary report
generate historical trends dashboard
```

Generated trend outputs:

```text
data/processed/snapshot_comparison_latest.csv
data/processed/probability_deltas_latest.csv
data/processed/top_movers_latest.csv
data/processed/signal_summary_latest.csv
docs/trends-dashboard/index.html
```

The CSV outputs are generated files and are ignored by Git by default.

The trends dashboard HTML file can be committed when the goal is to publish the latest experimental trends preview.

Historical trends documentation:

```text
docs/v0.7.0_roadmap.md
docs/historical_trends_architecture.md
docs/historical_trends_workflow.md
```

---

## Example stable workflow

1. Edit the manual CSV file:

```text
data/manual/world_cup_markets.csv
```

2. Run the provider-based snapshot update:

```powershell
python scripts/update_snapshot.py --provider manual_csv
```

3. Generate trends:

```powershell
python scripts/generate_trends.py
```

4. Generate the brief:

```powershell
python scripts/generate_brief.py
```

5. Generate the stable dashboard:

```powershell
python scripts/generate_dashboard.py
```

6. Review the generated dashboard:

```text
docs/dashboard/index.html
```

7. Review the generated Markdown brief inside:

```text
briefs/
```

---

## Example experimental Polymarket workflow

1. Run the live workflow:

```powershell
python scripts/run_polymarket_live_workflow.py
```

2. Open the Polymarket dashboard locally:

```powershell
start docs/polymarket-dashboard/index.html
```

3. After multiple Polymarket snapshots exist, run:

```powershell
python scripts/run_polymarket_live_workflow.py --include-trends
```

4. Open the trends dashboard locally:

```powershell
start docs/trends-dashboard/index.html
```

5. Commit dashboard HTML files only when the goal is to publish refreshed public pages.

---

## Methodology

Each market is interpreted through several layers:

| Layer     | Question                                          |
| --------- | ------------------------------------------------- |
| Price     | What probability is the market implying?          |
| Liquidity | Is there real market depth or only noise?         |
| Volume    | Is there actual participation?                    |
| Narrative | What public story may be driving the price?       |
| Catalyst  | What event may explain the move?                  |
| Trend     | Is the move persistent across multiple snapshots? |
| Red-team  | Why can the signal be wrong?                      |

Signal classification:

| Type        | Meaning                                                                  |
| ----------- | ------------------------------------------------------------------------ |
| Structural  | Persistent market signal backed by price, liquidity and catalyst quality |
| Tactical    | Short-term signal that may matter temporarily                            |
| Speculative | Weak or incomplete signal that needs confirmation                        |
| Noise       | Low-quality signal with no clear information value                       |

Trend classification:

| Type     | Meaning                                                         |
| -------- | --------------------------------------------------------------- |
| Strong   | Meaningful multi-snapshot movement with enough observations     |
| Emerging | Directional move that may become meaningful but needs more data |
| Weak     | Too little history or too small a move to draw conclusions      |

---

## Experimental signal intelligence

The historical trends layer currently supports transparent rule-based signal classification.

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

Important rule:

```text
large probability move + rising liquidity = stronger signal
large probability move + low liquidity = possible noise
```

This is intentionally simple and transparent.

It is not a black-box trading model.

---

## Generated output handling

Generated Polymarket outputs are ignored by default unless a version explicitly requires publishing them.

Ignored Polymarket outputs include:

```text
data/raw/polymarket/
data/processed/polymarket/
data/processed/polymarket_worldcup_yes_ranking.csv
data/processed/polymarket_worldcup_yes_ranking_summary.txt
data/processed/snapshots/*-polymarket.csv
```

Ignored historical trend CSV outputs include:

```text
data/processed/snapshot_comparison_latest.csv
data/processed/probability_deltas_latest.csv
data/processed/top_movers_latest.csv
data/processed/signal_summary_latest.csv
```

Dashboard HTML files can be committed when the goal is to publish refreshed public pages.

---

## Project philosophy

This project is designed as a learning system.

It prioritizes:

* reproducibility;
* transparent assumptions;
* provider-agnostic architecture;
* manual-first workflows;
* live provider experimentation;
* historical context;
* signal interpretation;
* red-team analysis;
* no black-box trading claims.

The goal is not to predict the World Cup winner.

The goal is to learn how markets, narratives, liquidity and probability changes interact around a global event.

---

## Not betting or investment advice

This project is for research and education only.

It is not betting advice.

It is not trading advice.

It is not investment advice.

It does not recommend bets, trades or financial decisions.


## Catalyst notes and narrative intelligence

v0.8.0 adds an experimental catalyst-notes and narrative-intelligence layer.

This layer connects market movement and signal classification with manually curated real-world context.

It helps answer questions such as:

~~~text
What may explain this probability move?
Was there a match result, injury, squad announcement or media narrative shift?
Was the move supported by liquidity?
Is the catalyst link low, medium or high confidence?
~~~

Key files:

~~~text
data/manual/catalyst_notes.csv
examples/catalyst_notes_sample.csv
src/wcmi/catalyst_notes.py
scripts/validate_catalyst_notes.py
scripts/match_catalyst_notes.py
~~~

Key documentation:

~~~text
docs/catalyst_notes_architecture.md
docs/catalyst_notes_workflow.md
docs/narrative_intelligence.md
docs/historical_trends_workflow.md
docs/releases/v0.8.0.md
~~~

The catalyst system is manual-first by design.

It does not automatically scrape news or invent explanations.

Catalyst notes do not prove causality. They provide transparent research context that may help explain probability movement.

