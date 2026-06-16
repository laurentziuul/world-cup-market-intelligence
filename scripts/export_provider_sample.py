from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from wcmi.providers.base import NORMALIZED_COLUMNS
from wcmi.providers.registry import available_provider_names, create_provider, get_provider_info


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "examples" / "provider_outputs"


def export_provider_sample(provider_name: str, output_path: Path | None = None) -> Path:
    provider_info = get_provider_info(provider_name)
    provider = create_provider(provider_name)

    df = provider.load()

    expected_columns = NORMALIZED_COLUMNS + ["provider"]

    missing_columns = [
        column
        for column in expected_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Provider '{provider_name}' is missing required columns: {missing_columns}"
        )

    df = df[expected_columns].copy()

    if output_path is None:
        output_path = DEFAULT_OUTPUT_DIR / f"{provider_name}_normalized_sample.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Provider: {provider_info.name}")
    print(f"Status: {provider_info.status}")
    print(f"Rows exported: {len(df)}")
    print(f"Sample saved: {output_path}")

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a normalized sample CSV from a provider."
    )

    parser.add_argument(
        "--provider",
        default="manual_csv",
        choices=available_provider_names(),
        help="Provider to export.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output CSV path.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    export_provider_sample(
        provider_name=args.provider,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()