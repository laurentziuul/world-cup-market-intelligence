# Provider System

World Cup Market Intelligence uses a provider abstraction layer so market data can come from multiple sources while keeping the rest of the pipeline stable.

## Current provider

### `manual_csv`

The default provider reads market data from:

```text
data/manual/world_cup_markets.csv
```

Run:

```bash
python scripts/update_snapshot.py --provider manual_csv
```

Backward-compatible wrapper:

```bash
python scripts/update_snapshot_manual.py
```

## Provider contract

Every provider must return a normalized dataframe with these columns:

| Column         | Meaning                             |
| -------------- | ----------------------------------- |
| `market_id`    | Stable market identifier            |
| `market_title` | Human-readable market title         |
| `outcome`      | Outcome/team/player being tracked   |
| `price`        | Market-implied probability or price |
| `volume`       | Market volume, if available         |
| `liquidity`    | Market liquidity, if available      |
| `narrative`    | Analyst narrative label             |
| `catalyst`     | Main catalyst or reason to watch    |
| `source_url`   | Source URL or provider reference    |
| `notes`        | Analyst notes                       |

The snapshot pipeline then adds:

| Column                 | Meaning                                   |
| ---------------------- | ----------------------------------------- |
| `provider`             | Provider name                             |
| `snapshot_time_utc`    | Snapshot timestamp                        |
| `snapshot_date_utc`    | Snapshot date                             |
| `price_change_24h`     | Change versus previous snapshot           |
| `volume_change_24h`    | Volume change versus previous snapshot    |
| `liquidity_change_24h` | Liquidity change versus previous snapshot |

## Current pipeline

```text
provider
    ↓
normalized dataframe
    ↓
snapshot_latest.csv
    ↓
timestamped snapshot archive
    ↓
trends_latest.csv
    ↓
dashboard / brief
```

## Future providers

Planned providers:

```text
polymarket
kalshi
manual_google_sheet
custom_csv
```

Live providers should be optional and fail safely. The manual CSV provider should remain the default because it works offline and makes the project reproducible.
