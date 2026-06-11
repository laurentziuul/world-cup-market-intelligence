# World Cup Market Intelligence v0

Open-source market-intelligence framework for tracking prediction-market prices, liquidity, narratives and catalysts around FIFA World Cup 2026.

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

The current version supports a simple offline/manual pipeline:

```text
manual CSV data
        ↓
normalized snapshot
        ↓
daily Markdown brief
```

Current capabilities:

* ingest a manual CSV watchlist;
* normalize market data into a standard snapshot;
* generate a daily Markdown intelligence brief;
* separate market data from narrative interpretation;
* classify early signals as structural, tactical or speculative;
* red-team the strongest signal before publishing.

## Current data provider

v0 uses a manual CSV provider by default.

Input file:

```text
data/manual/world_cup_markets.csv
```

Generated snapshot:

```text
data/processed/snapshot_latest.csv
```

Generated brief:

```text
briefs/YYYY-MM-DD-world-cup-market-brief.md
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

Create a manual snapshot:

```powershell
python scripts/update_snapshot_manual.py
```

Generate the daily brief:

```powershell
python scripts/generate_brief.py
```

## Example workflow

1. Edit the manual CSV file:

```text
data/manual/world_cup_markets.csv
```

2. Run:

```powershell
python scripts/update_snapshot_manual.py
```

3. Generate the brief:

```powershell
python scripts/generate_brief.py
```

4. Review the generated Markdown file inside:

```text
briefs/
```

## Methodology

Each market is interpreted through several layers:

| Layer     | Question                                    |
| --------- | ------------------------------------------- |
| Price     | What probability is the market implying?    |
| Liquidity | Is there real market depth or only noise?   |
| Volume    | Is there actual participation?              |
| Narrative | What public story may be driving the price? |
| Catalyst  | What event may explain the move?            |
| Red-team  | Why can the signal be wrong?                |

Signal classification:

| Type        | Meaning                                                                  |
| ----------- | ------------------------------------------------------------------------ |
| Structural  | Persistent market signal backed by price, liquidity and catalyst quality |
| Tactical    | Short-term signal that may matter temporarily                            |
| Speculative | Weak or incomplete signal that needs confirmation                        |
| Noise       | Low-quality signal with no clear information value                       |

## Project philosophy

This project is designed as a learning system.

It prioritizes:

* reproducibility;
* transparent assumptions;
* provider-agnostic architecture;
* manual-first workflows;
* clear research notes;
* red-team analysis;
* no black-box trading claims.

The goal is not to predict the World Cup winner.
The goal is to learn how markets, narratives and liquidity interact around a global event.

## Disclaimer

This repository is for educational and research purposes only.

It is not financial advice, betting advice or investment advice.
Do not use this project as the sole basis for placing trades or bets.
