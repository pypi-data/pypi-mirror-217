"""Test France collector"""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

pytest_plugins = ("pytest_asyncio",)

from cofybox_dce.pricing_collectors import Enercoop


@pytest.fixture
def enercoop():
    """Fixture for Enercoop collector"""
    collector = Enercoop(tariff="dynamic_tariff")

    collector.session = MagicMock()
    collector.session.get.return_value.content = open(
        "tests/data/enercoop_sample.csv", "rb"
    ).read()

    return collector


def test_enercoop(enercoop):
    """Test Enercoop collector"""
    assert enercoop.country == "FR"
    assert enercoop.supplier == "Enercoop"
    assert enercoop.timezone == "Europe/Paris"
    assert enercoop.unit == "c€/kWh"
    assert enercoop.tariff == "dynamic_tariff"
    assert enercoop.price_name == "Enercoop_dynamic_tariff"
    assert enercoop.region_code == "FR"


@pytest.mark.asyncio
async def test_enercoop_get_data(enercoop):
    """Test Enercoop get_data"""
    df = await enercoop.get_data()
    assert df.columns.tolist() == ["value_inc_vat", "Unit"]
    assert df.index.tz.zone == "Europe/Paris"
    assert df["Unit"].iloc[0] == "c€/kWh"
