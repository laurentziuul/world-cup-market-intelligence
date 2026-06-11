# Architecture

## Design principle

World Cup Market Intelligence is designed as a reusable event-intelligence engine.

The FIFA World Cup 2026 is the first event implementation, but the system should later support:

- elections
- central bank meetings
- crypto unlocks
- major court decisions
- sport tournaments
- tech product launches
- geopolitical deadlines

## Pipeline

```text
Event calendar
Prediction markets
Manual narrative notes
News catalysts
        ↓
Raw snapshots
        ↓
Normalized market rows
        ↓
Signal scoring
        ↓
Daily brief
        ↓
Public archive / X / Substack
```

## Layers

### 1. Data ingestion

Initial v0 sources:

- Polymarket Gamma API for events and markets
- Manual narrative notes
- FIFA public schedule references

Future sources:

- CLOB order book data
- odds aggregators
- news APIs
- official FIFA match events
- social trend signals

### 2. Storage

v0 uses flat files:

- raw JSON in `data/raw/`
- processed CSV in `data/processed/`
- generated Markdown briefs in `briefs/`

Future versions can add SQLite or DuckDB.

### 3. Signal scoring

The v0 heuristic model:

```text
Signal Score = Price Move + Liquidity + Catalyst - Narrative Crowding - Failure Risk
```

Interpretation:

- 7+ = structural / write
- 4–6 = tactical / research
- 2–3 = speculative / watch
- <2 = noise / ignore

This is intentionally simple. The first goal is process discipline, not predictive sophistication.

### 4. Brief generation

The brief should always separate:

- market data
- catalyst inference
- narrative classification
- red-team analysis
- uncertainty level

The brief should never be positioned as a betting tip.
