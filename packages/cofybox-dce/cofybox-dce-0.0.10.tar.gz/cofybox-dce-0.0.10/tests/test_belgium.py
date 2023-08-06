"""Test EcoPower collector"""

from unittest.mock import MagicMock

import pandas as pd
import pytest

pytest_plugins = ("pytest_asyncio",)

from cofybox_dce.pricing_collectors import Ecopower


@pytest.fixture
def ecopower():
    """Fixture for EcoPower collector"""
    collector = Ecopower(
        region_code="Antwerpen",
        direction="consumption",
        consumer_type="residential",
        entsoe_api_key="test",
    )
    collector.entsoe_client = MagicMock()
    collector.entsoe_client.query_day_ahead_prices.return_value = pd.read_pickle(
        "tests/data/da_prices_sample.pkl"
    )
    return collector


def test_ecopower(ecopower):
    """Test EcoPower collector"""
    assert ecopower.country == "BE"
    assert ecopower.supplier == "Ecopower_Dynamic"
    assert ecopower.timezone == "Europe/Brussels"
    assert ecopower.unit == "c€/kWh"
    assert ecopower.region_code == "Antwerpen"
    assert ecopower.price_name == "Ecopower_Dynamic_Antwerpen_residential_consumption"


@pytest.mark.asyncio
async def test_ecopower_get_data(ecopower):
    """Test EcoPower get_data"""
    df = await ecopower.get_data()
    assert df.columns.tolist() == ["value_inc_vat", "Unit"]
    assert df.index.tz.zone == "Europe/Brussels"
    assert df["Unit"].iloc[0] == "c€/kWh"

    # Test with interval

    interval = pd.Interval(
        left=pd.Timestamp("2021-01-01", tz="Europe/Brussels"),
        right=pd.Timestamp("2021-01-04", tz="Europe/Brussels"),
        closed="left",
    )

    df = await ecopower.get_data(interval=interval)
    assert df.columns.tolist() == ["value_inc_vat", "Unit"]
    assert df.index.tz.zone == "Europe/Brussels"
    assert df["Unit"].iloc[0] == "c€/kWh"

    # Test with epex argument
    df = await ecopower.get_data(epex=pd.read_pickle("tests/data/da_prices_sample.pkl"))
    assert df.columns.tolist() == ["value_inc_vat", "Unit"]
    assert df.index.tz.zone == "Europe/Brussels"
    assert df["Unit"].iloc[0] == "c€/kWh"
