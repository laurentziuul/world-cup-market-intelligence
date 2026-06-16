from __future__ import annotations

from dataclasses import dataclass

from wcmi.providers.base import MarketProvider
from wcmi.providers.manual_csv import ManualCsvProvider


@dataclass(frozen=True)
class ProviderInfo:
    name: str
    provider_class: type[MarketProvider]
    description: str
    is_live: bool
    requires_network: bool
    status: str


PROVIDER_REGISTRY: dict[str, ProviderInfo] = {
    "manual_csv": ProviderInfo(
        name="manual_csv",
        provider_class=ManualCsvProvider,
        description="Offline manual CSV provider. Default reproducible provider.",
        is_live=False,
        requires_network=False,
        status="stable",
    ),
}


def available_provider_names() -> list[str]:
    return sorted(PROVIDER_REGISTRY.keys())


def get_provider_info(provider_name: str) -> ProviderInfo:
    if provider_name not in PROVIDER_REGISTRY:
        available = ", ".join(available_provider_names())
        raise ValueError(
            f"Unknown provider: {provider_name}\n"
            f"Available providers: {available}"
        )

    return PROVIDER_REGISTRY[provider_name]


def create_provider(provider_name: str) -> MarketProvider:
    provider_info = get_provider_info(provider_name)
    return provider_info.provider_class()


def list_provider_info() -> list[ProviderInfo]:
    return [
        PROVIDER_REGISTRY[name]
        for name in available_provider_names()
    ]