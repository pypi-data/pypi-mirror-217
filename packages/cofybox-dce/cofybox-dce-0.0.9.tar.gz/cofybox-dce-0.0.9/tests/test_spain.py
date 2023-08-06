"""Tests for Spain Dynamic Prices"""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from cofybox_dce.pricing_collectors import SomEnergiaInjection, SomEnergiaOfftake


@pytest.fixture
def somenergia_injection():
    """Fixture for SomEnergia collector"""
    collector = SomEnergiaInjection(entsoe_api_key="test")
    collector.entsoe_client = MagicMock()
    collector.entsoe_client.query_day_ahead_prices.return_value = pd.read_pickle(
        "tests/data/da_prices_sample.pkl"
    ).tz_convert("Europe/Madrid")
    return collector


@pytest.fixture
def somenergia_offtake():
    """Fixture for SomEnergia collector"""
    collector = SomEnergiaOfftake()
    return collector


def test_somenergia_injection(somenergia_injection):
    """Test SomEnergia collector"""
    assert somenergia_injection.country == "ES"
    assert somenergia_injection.supplier == "SomEnergia"
    assert somenergia_injection.timezone == "Europe/Madrid"
    assert somenergia_injection.unit == "c€/kWh"
    assert somenergia_injection.price_name == "SomEnergia_injection"
    assert somenergia_injection.region_code == "ES"


def test_somenergia_offtake(somenergia_offtake):
    """Test SomEnergia collector"""
    assert somenergia_offtake.country == "ES"
    assert somenergia_offtake.supplier == "SomEnergia"
    assert somenergia_offtake.timezone == "Europe/Madrid"
    assert somenergia_offtake.unit == "c€/kWh"
    assert somenergia_offtake.price_name == "SomEnergia_consumption"
    assert somenergia_offtake.region_code == "ES"


@pytest.mark.asyncio
async def test_somenergia_injection_get_data(somenergia_injection):
    """Test SomEnergia get_data"""
    df = await somenergia_injection.get_data()
    assert df.columns.tolist() == ["value_inc_vat", "Unit"]
    assert df.index.tz.zone == "Europe/Madrid"
    assert df["Unit"].iloc[0] == "c€/kWh"


@pytest.mark.asyncio
async def test_somenergia_offtake_get_data(somenergia_offtake):
    """Test SomEnergia get_data"""
    df = await somenergia_offtake.get_data()
    assert df.columns.tolist() == ["value_inc_vat", "Unit"]
    assert df.index.tz.zone == "Europe/Madrid"
    assert df["Unit"].iloc[0] == "c€/kWh"
