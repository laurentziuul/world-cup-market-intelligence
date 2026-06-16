# Provider Status

This document tracks the current implementation status of all data providers in World Cup Market Intelligence.

The project is designed to support multiple data sources over time, while keeping one stable normalized provider contract.

---

## Status levels

| Status         | Meaning                                                     |
| -------------- | ----------------------------------------------------------- |
| `stable`       | Implemented, tested and safe to use in the default pipeline |
| `experimental` | Implemented but still under active testing                  |
| `planned`      | Added to the architecture, but not implemented yet          |
| `disabled`     | Implemented but intentionally turned off                    |
| `broken`       | Known to fail and should not be used                        |

---

## Current providers

| Provider      | Status         | Mode    | Network required | Description                                                                 |
| ------------- | -------------- | ------- | ---------------- | --------------------------------------------------------------------------- |
| `manual_csv`  | `stable`       | offline | no               | Manual CSV provider. Default reproducible provider.                         |
| `polymarket`  | `experimental` | live    | yes              | Experimental live API provider for Polymarket World Cup prediction markets. |
| `predict_fun` | `planned`      | live    | yes              | Planned live API provider for Predict.fun prediction markets.               |
| `kalshi`      | `planned`      | live    | yes              | Planned live API provider for Kalshi prediction markets.                    |
| `manifold`    | `planned`      | live    | yes              | Planned live API provider for Manifold prediction markets.                  |

---

## Current default provider

The current default provider is:

```text
manual_csv
```

It reads data from:

```text
data/manual/world_cup_markets.csv
```

It can be run with:

```bash
python scripts/update_snapshot.py --provider manual_csv
```

The manual provider remains the stable default provider.

---

## Experimental live provider

The first experimental live provider is:

```text
polymarket
```

It can be validated with:

```bash
python scripts/validate_providers.py --provider polymarket --include-live
```

It can generate a live snapshot with:

```bash
python scripts/update_snapshot.py --provider polymarket
```

Current Polymarket behavior:

```text
fetches live markets from Polymarket Gamma API
filters World Cup / FIFA markets
normalizes each market outcome into the provider contract
produces snapshot rows compatible with the existing pipeline
```

Important access note:

```text
Polymarket access may depend on network, DNS, Cloudflare behavior, geo restrictions or VPN availability.
The provider worked during testing with Proton VPN using a Moldova server.
```

Because of these risks, `polymarket` should remain:

```text
experimental
```

not stable.

---

## Planned live providers

The following providers exist as placeholders in the architecture:

```text
predict_fun
kalshi
manifold
```

They appear in the provider registry and in:

```bash
python scripts/update_snapshot.py --list-providers
```

However, they are not implemented yet.

Trying to run one of them should return a clear error explaining that the provider is planned but not implemented.

---

## Validation policy

Offline and stable providers can be validated with:

```bash
python scripts/validate_providers.py
```

One provider can be validated directly with:

```bash
python scripts/validate_providers.py --provider manual_csv
```

Live providers are skipped by default because they may require:

```text
network access
API availability
authentication
geo access
rate-limit handling
schema stability
```

Live providers can be tested explicitly with:

```bash
python scripts/validate_providers.py --include-live
```

Or individually with:

```bash
python scripts/validate_providers.py --provider polymarket --include-live
```

---

## Smoke test policy

The stable offline pipeline can be tested end-to-end with:

```bash
python scripts/smoke_test_pipeline.py --provider manual_csv
```

This verifies:

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

Before adding or modifying live providers, this smoke test should pass for `manual_csv`.

---

## Provider promotion rules

A provider should move from `planned` to `experimental` only when:

* it can fetch raw data;
* it can normalize data into the required provider contract;
* it passes provider validation;
* it fails safely when the API is unavailable;
* it does not break the manual CSV pipeline.

A provider should move from `experimental` to `stable` only when:

* it has been tested repeatedly;
* API schema changes are handled safely;
* network errors produce clear messages;
* raw response caching exists or is planned;
* dashboard, trends and briefs work with its output;
* false-positive market filtering is acceptably low.

---

## Current recommendation

Use:

```text
manual_csv
```

for the stable offline workflow.

Use:

```text
polymarket
```

only for experimental live API testing.

Treat all other live providers as planned architecture until their API integrations are implemented and tested.
