# World Cup Market Intelligence v0

Open-source market-intelligence framework for tracking prediction-market prices, liquidity, narratives, catalysts and historical probability trends around FIFA World Cup 2026.

This project is not a betting system and does not provide betting tips.
The goal is to study how crowds price uncertainty during a scheduled global attention event.

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

## What v0 does

The current version supports an offline/manual-first intelligence pipeline:

```text
provider
    ↓
normalized snapshot
    ↓
timestamped snapshot archive
    ↓
historical trend engine
    ↓
daily Markdown brief
    ↓
static dashboard
```

Current capabilities:

* ingest a manual CSV watchlist;
* normalize market data into a standard snapshot;
* archive timestamped snapshots;
* calculate snapshot-to-snapshot price, volume and liquidity changes;
* generate historical trend summaries;
* generate a daily Markdown intelligence brief;
* generate a static HTML dashboard;
* separate market data from narrative interpretation;
* classify early signals as structural, tactical, speculative or noise;
* red-team the strongest signals before publishing;
* use a provider abstraction layer so new data sources can be added later.

## Current data provider

v0 uses a manual CSV provider by default.

Input file:

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

Generated trend file:

```text
data/processed/trends_latest.csv
```

Generated brief:

```text
briefs/YYYY-MM-DD-world-cup-market-brief.md
```

Generated dashboard:

```text
docs/dashboard/index.html
```

External APIs such as Polymarket, Kalshi, Manifold or other odds providers can be added later as optional providers. They should not be hard dependencies.

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

Generate historical trends:

```powershell
python scripts/generate_trends.py
```

Generate the daily brief:

```powershell
python scripts/generate_brief.py
```

Generate the dashboard:

```powershell
python scripts/generate_dashboard.py
```

Open the dashboard locally:

```powershell
start docs/dashboard/index.html
```

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

## Provider validation

Validate all offline providers:

```powershell
python scripts/validate_providers.py
```

Validate one provider only:

```powershell
python scripts/validate_providers.py --provider manual_csv
```

Live or network-based providers are skipped by default. When live providers are added later, they can be tested explicitly with:

```powershell
python scripts/validate_providers.py --include-live
```

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

## Full pipeline smoke test

Run a full local pipeline test with:

```powershell
python scripts/smoke_test_pipeline.py --provider manual_csv
```

This validates the provider, exports a normalized provider sample, updates the latest snapshot, regenerates trends and rebuilds the dashboard.



## Example workflow

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

5. Generate the dashboard:

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

## Project philosophy

This project is designed as a learning system.

It prioritizes:

* reproducibility;
* transparent assumptions;
* provider-agnostic architecture;
* manual-first workflows;
* clear research notes;
* historical context;
* red-team analysis;
* no black-box trading claims.

The goal is not to predict the World Cup winner.
The goal is to learn how markets, narratives, liquidity and probability changes interact around a global event.
## API provider strategy

The project is designed to support multiple data providers over time, not just one API.

Current and future providers may include:

```text
manual_csv
polymarket
predict_fun
kalshi
manifold
custom_csv
other APIs
```

The API provider strategy is documented here:

```text
docs/api_provider_strategy.md
```

The core principle is that each provider can have different raw data, but every provider must return the same normalized internal format before entering the snapshot, trend, dashboard and brief pipeline.
## Dashboards

World Cup Market Intelligence currently has two public dashboards.

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

---

## Live provider documentation

The stable default provider remains:

```text
manual_csv
```

The first experimental live provider is:

```text
polymarket
```

Provider and live workflow documentation:

```text
docs/provider_status.md
docs/polymarket_live_workflow.md
docs/api_provider_strategy.md
docs/api_sources_matrix.md
```

The experimental Polymarket workflow can be run with:

```powershell
python scripts/run_polymarket_live_workflow.py
```

This workflow validates the live provider, creates a Polymarket snapshot, generates a YES-only World Cup ranking and updates the separate Polymarket live dashboard.

The stable offline workflow remains:

```powershell
python scripts/smoke_test_pipeline.py --provider manual_csv
```

Use `manual_csv` for stable reproducible work.
Use `polymarket` only for experimental live market intelligence.
