# Provider System

World Cup Market Intelligence uses a provider abstraction layer so market data can come from multiple sources while keeping the rest of the pipeline stable.

The goal is simple: every provider can have different raw data, but every provider must return the same normalized internal format.

---

## Current provider

### `manual_csv`

The default provider reads market data from:

```text
data/manual/world_cup_markets.csv
```

Run the provider-based snapshot update:

```bash
python scripts/update_snapshot.py --provider manual_csv
```

Backward-compatible wrapper:

```bash
python scripts/update_snapshot_manual.py
```

The manual CSV provider is the default because it works offline, is reproducible, and does not depend on any external API.

---

## Provider registry

Available providers can be listed with:

```bash
python scripts/update_snapshot.py --list-providers
```

Current provider registry:

```text
manual_csv
```

Future providers can be added to:

```text
src/wcmi/providers/registry.py
```

---

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

---

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

---

## Provider validation

Providers can be validated against the normalized provider contract with:

```bash
python scripts/validate_providers.py
```

Validate one provider only:

```bash
python scripts/validate_providers.py --provider manual_csv
```

Live or network-based providers are skipped by default. When live providers are added later, they can be tested explicitly with:

```bash
python scripts/validate_providers.py --include-live
```

The validator checks that each provider returns:

* a pandas dataframe;
* all required normalized columns;
* numeric `price`, `volume` and `liquidity` fields;
* non-empty key fields such as `market_id`, `market_title` and `outcome`;
* consistent provider names.

---

## Future providers

Planned providers may include:

```text
polymarket
predict_fun
kalshi
manifold
manual_google_sheet
custom_csv
other APIs
```

Live providers should be optional and fail safely.

The manual CSV provider should remain the default because it works offline and makes the project reproducible.

The long-term goal is multi-source market intelligence, not dependence on a single API.

---

## Provider sample outputs

Normalized provider samples can be exported with:

```bash
python scripts/export_provider_sample.py --provider manual_csv
```

The default sample output path is:

```text
examples/provider_outputs/manual_csv_normalized_sample.csv
```

These files are used as human-readable fixtures. They show what a valid normalized provider output should look like before the data enters the snapshot pipeline.

When new providers are added later, each provider should be able to export a similar normalized sample.

Example future files:

```text
examples/provider_outputs/polymarket_normalized_sample.csv
examples/provider_outputs/predict_fun_normalized_sample.csv
examples/provider_outputs/kalshi_normalized_sample.csv
examples/provider_outputs/manifold_normalized_sample.csv
```
---

## Full pipeline smoke test

The full local pipeline can be tested with:

```bash
python scripts/smoke_test_pipeline.py --provider manual_csv
```

This command runs:

```text
provider validation
    ↓
provider sample export
    ↓
snapshot update
    ↓
trend generation
    ↓
dashboard generation
```

This is useful before adding new live API providers, because it confirms that the current provider still works end-to-end.

