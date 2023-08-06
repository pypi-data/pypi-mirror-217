"""Tests for pricing collectors"""

import json
from unittest.mock import MagicMock

import pandas as pd
import pytest

pytest_plugins = ("pytest_asyncio",)

from cofybox_dce.pricing_collectors import Octopus, OctopusOutgoing


@pytest.fixture
def octopus():
    """Fixture for Octopus collector"""
    return Octopus(region_code="A")


@pytest.fixture
def octopus_outgoing():
    """Fixture for Octopus Outgoing collector"""
    return OctopusOutgoing(region_code="A")


def test_octopus(octopus):
    """Test Octopus collector"""
    assert octopus.country == "UK"
    assert octopus.supplier == "Octopus"
    assert octopus.timezone == "Europe/London"
    assert octopus.unit == "p£/kWh"
    assert octopus.region_code == "A"
    assert octopus.price_name == "Octopus_A"


def test_octopus_outgoing(octopus_outgoing):
    """Test Octopus Outgoing collector"""
    assert octopus_outgoing.country == "UK"
    assert octopus_outgoing.supplier == "Octopus_Outgoing"
    assert octopus_outgoing.timezone == "Europe/London"
    assert octopus_outgoing.unit == "p£/kWh"
    assert octopus_outgoing.region_code == "A"
    assert octopus_outgoing.price_name == "Octopus_Outgoing_A"


@pytest.mark.asyncio
async def test_octopus_get_data(octopus):
    """Test Octopus get_data"""
    octopus.agile = MagicMock()

    # Load test data from JSON file
    octopus.agile.get_new_rates.return_value = json.load(
        open("tests/data/octopus_agile_sample.json")
    )

    df = await octopus.get_data()
    assert df.columns.tolist() == ["value_inc_vat", "Unit"]
    assert df.index.tz.zone == "Europe/London"
    assert df["Unit"].iloc[0] == "p£/kWh"

    # Test with interval

    octopus.agile.get_rates.return_value = json.load(
        open("tests/data/octopus_agile_sample.json")
    )

    interval = pd.Interval(
        left=pd.Timestamp("2021-01-01", tz="Europe/London"),
        right=pd.Timestamp("2021-01-04", tz="Europe/London"),
        closed="left",
    )

    df = await octopus.get_data(interval=interval)
    assert df.columns.tolist() == ["value_inc_vat", "Unit"]
    assert df.index.tz.zone == "Europe/London"
    assert df["Unit"].iloc[0] == "p£/kWh"
