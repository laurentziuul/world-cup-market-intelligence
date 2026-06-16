from __future__ import annotations

import argparse

import pandas as pd

from wcmi.providers.base import NORMALIZED_COLUMNS, NUMERIC_COLUMNS
from wcmi.providers.registry import (
    available_provider_names,
    create_provider,
    get_provider_info,
    list_provider_info,
)


def validate_provider_output(provider_name: str) -> tuple[bool, list[str]]:
    errors: list[str] = []

    provider_info = get_provider_info(provider_name)
    provider = create_provider(provider_name)

    try:
        df = provider.load()
    except Exception as exc:
        return False, [f"Provider failed to load: {exc}"]

    if not isinstance(df, pd.DataFrame):
        return False, [f"Provider returned {type(df).__name__}, expected pandas.DataFrame"]

    if df.empty:
        errors.append("Provider returned an empty dataframe")

    missing_columns = [
        column
        for column in NORMALIZED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")

    for column in NUMERIC_COLUMNS:
        if column not in df.columns:
            continue

        converted = pd.to_numeric(df[column], errors="coerce")

        if converted.isna().any():
            errors.append(f"Column '{column}' contains non-numeric values")

    key_columns = [
        "market_id",
        "market_title",
        "outcome",
    ]

    for column in key_columns:
        if column not in df.columns:
            continue

        empty_count = int(df[column].fillna("").astype(str).str.strip().eq("").sum())

        if empty_count > 0:
            errors.append(f"Column '{column}' contains {empty_count} empty values")

    if "provider" in df.columns:
        unexpected_provider_values = sorted(
            set(df["provider"].dropna().astype(str)) - {provider_info.name}
        )

        if unexpected_provider_values:
            errors.append(
                f"Unexpected provider values in dataframe: {unexpected_provider_values}"
            )

    return len(errors) == 0, errors


def print_provider_validation(provider_name: str) -> bool:
    provider_info = get_provider_info(provider_name)

    print(f"Validating provider: {provider_info.name}")
    print(f"Status: {provider_info.status}")
    print(f"Description: {provider_info.description}")

    is_valid, errors = validate_provider_output(provider_name)

    if is_valid:
        print("Result: PASS")
        print("")
        return True

    print("Result: FAIL")

    for error in errors:
        print(f"- {error}")

    print("")
    return False


def select_providers(provider_name: str | None, include_live: bool) -> list[str]:
    if provider_name:
        return [provider_name]

    providers = []

    for provider_info in list_provider_info():
        if provider_info.is_live and not include_live:
            continue

        providers.append(provider_info.name)

    return providers


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate provider outputs against the normalized provider contract."
    )

    parser.add_argument(
        "--provider",
        choices=available_provider_names(),
        help="Validate one provider only.",
    )

    parser.add_argument(
        "--include-live",
        action="store_true",
        help="Also validate live/network providers.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    providers = select_providers(
        provider_name=args.provider,
        include_live=args.include_live,
    )

    if not providers:
        print("No providers selected.")
        return

    all_valid = True

    for provider_name in providers:
        provider_valid = print_provider_validation(provider_name)
        all_valid = all_valid and provider_valid

    if not all_valid:
        raise SystemExit(1)

    print("All selected providers passed validation.")


if __name__ == "__main__":
    main()