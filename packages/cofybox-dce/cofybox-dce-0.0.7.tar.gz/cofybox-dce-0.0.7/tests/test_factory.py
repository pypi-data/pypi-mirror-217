import pytest

from src.cofybox_dce.abstract import CollectorType
from src.cofybox_dce.factory import create_collector
from src.cofybox_dce.pricing_collectors import *


@pytest.mark.parametrize(
    "collector_type, body, expected",
    [
        (CollectorType.PRICE, {"supplier": "Octopus", "regionCode": "A"}, Octopus),
        (
            CollectorType.PRICE,
            {"supplier": "Octopus_Outgoing", "regionCode": "A"},
            OctopusOutgoing,
        ),
        (
            CollectorType.PRICE,
            {
                "supplier": "Ecopower",
                "regionCode": "Antwerpen",
                "direction": "consumption",
                "consumerType": "residential",
            },
            Ecopower,
        ),
        (
            CollectorType.PRICE,
            {
                "supplier": "Engie",
                "regionCode": "Antwerpen",
                "direction": "consumption",
                "consumerType": "residential",
            },
            Engie,
        ),
        (CollectorType.PRICE, {"supplier": "Enercoop", "tariff": "test"}, Enercoop),
        (
            CollectorType.PRICE,
            {"supplier": "SomEnergia", "direction": "consumption"},
            SomEnergiaOfftake,
        ),
        (
            CollectorType.PRICE,
            {"supplier": "SomEnergia", "direction": "injection"},
            SomEnergiaInjection,
        ),
    ],
)
def test_create_collector(collector_type, body, expected):
    """Test that the factory creates the correct collectors"""
    collector = create_collector(
        collector_type=collector_type, body=body, entsoe_api_key="test"
    )
    assert isinstance(collector, expected)


# Test some exceptions
@pytest.mark.parametrize(
    "collector_type, body, expected",
    [
        (
            "Not a collector type",
            {"supplier": "Octopus", "regionCode": "A"},
            NotImplementedError,
        ),
        (
            CollectorType.PRICE,
            {"supplier": "Not a supplier", "regionCode": "A"},
            LookupError,
        ),
        (
            CollectorType.PRICE,
            {"supplier": "SomEnergia", "direction": "Not a direction"},
            LookupError,
        ),
    ],
)
def test_create_collector_exceptions(collector_type, body, expected):
    """Test that the factory raises the correct exceptions"""
    with pytest.raises(expected):
        create_collector(
            collector_type=collector_type, body=body, entsoe_api_key="test"
        )
