"""Pricing Collectors for Belgium (Flanders) Dynamic Prices"""

from enum import Enum
from typing import Optional, Union

import pandas as pd

from .pricing import DAPricingCollector


# Enum containing directions
class Direction(str, Enum):
    """Enum containing directions"""

    CONSUMPTION = "consumption"
    INJECTION = "injection"


class ConsumerType(str, Enum):
    """Enum containing consumer types"""

    RESIDENTIAL = "residential"
    BUSINESS = "business"


class BEPricingCollector(DAPricingCollector):
    """Abstract Collector for Belgium (Flanders) Dynamic prices"""

    country = "BE"
    timezone = "Europe/Brussels"
    unit = "c€/kWh"

    grid_costs = {
        "consumption": {
            "Antwerpen": 73.30,
            "Limburg": 75.21,
            "West": 74.02,
            "Gaselwest": 85.00,
            "Imewo": 75.83,
            "Intergem": 72.49,
            "Iveka": 77.75,
            "Iverlek": 74.66,
            "PBE": 72.39,
            "Sibelgas": 81.16,
        },
        "injection": {
            "Antwerpen": 0.0,
            "Limburg": 0.0,
            "West": 0.0,
            "Gaselwest": 0.0,
            "Imewo": 0.0,
            "Intergem": 0.0,
            "Iveka": 0.0,
            "Iverlek": 0.0,
            "PBE": 0.0,
            "Sibelgas": 0.0,
        },
    }

    balancing_costs = {"consumption": 0.0, "injection": 0.0}

    vat = {
        "consumption": {"residential": 0.06, "business": 0.21},
        "injection": {"residential": 0.0, "business": 0.21},
    }

    def __init__(
        self,
        region_code: str,
        direction: Union[str, Direction],
        consumer_type: Union[str, ConsumerType],
        entsoe_api_key: str,
        **kwargs,
    ):
        """Initialize"""
        self.region_code = region_code
        self.direction = (
            Direction(direction) if isinstance(direction, str) else direction
        )
        self.consumer_type = (
            ConsumerType(consumer_type)
            if isinstance(consumer_type, str)
            else consumer_type
        )
        self.price_name = f"{self.supplier}_{region_code}_{consumer_type}_{direction}"
        super().__init__(entsoe_api_key=entsoe_api_key, **kwargs)

    async def get_data(
        self,
        interval: Optional[pd.Interval] = None,
        epex: Optional[pd.Series] = None,
    ) -> pd.DataFrame:
        """Get Data"""
        if epex is None:
            price = self.get_da_prices(interval)
        else:
            price = epex

        # Add / Subtract balancing cost
        price = price + self.balancing_costs[self.direction]

        # Add Grid costs
        price = price + self.grid_costs[self.direction][self.region_code]

        # Add VAT
        price = price * (1 + self.vat[self.direction][self.consumer_type])

        # From euro/MWh to eurocent/kWh

        price = price / 10

        price = pd.DataFrame(price, columns=["value_inc_vat"])
        price["Unit"] = self.unit
        return price


class Ecopower(BEPricingCollector):
    """Pricing Collector for Ecopower Dynamic Prices"""

    supplier = "Ecopower_Dynamic"

    balancing_costs = {"consumption": 2.3, "injection": 2.3}


class Engie(BEPricingCollector):
    """Pricing Collector for Engie Dynamic Prices"""

    supplier = "Engie_Dynamic"

    balancing_costs = {"consumption": 2.04, "injection": 0}
