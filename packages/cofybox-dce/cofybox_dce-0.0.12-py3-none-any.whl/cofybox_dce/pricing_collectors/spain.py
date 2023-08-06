"""Pricing Collectors for Spain"""
import datetime as dt
from typing import Optional

import aiohttp
import aiopvpc
import pandas as pd

from .pricing import DAPricingCollector, PricingCollector


class SomEnergiaOfftake(PricingCollector):
    """Pricing Collector for Som Energia Dynamic Prices"""

    supplier = "SomEnergia"
    country = "ES"
    timezone = "Europe/Madrid"
    unit = "c€/kWh"

    def __init__(self, **kwargs):
        """Initialize"""
        self.region_code = "ES"
        self.price_name = f"{self.supplier}_consumption"
        super().__init__(**kwargs)

    async def get_data(
        self,
        interval: Optional[pd.Interval] = None,  # Not used
    ) -> pd.DataFrame:
        """Get Data"""
        async with aiohttp.ClientSession() as session:
            pvpc_handler = aiopvpc.PVPCData(session=session, tariff="2.0TD")
            esios_data = await pvpc_handler.async_update_all(
                current_data=None, now=dt.datetime.utcnow()
            )
        pvpc_data = esios_data.sensors["PVPC"]
        data_frame = pd.DataFrame.from_dict(pvpc_data, orient="index")
        data_frame = data_frame.tz_convert("Europe/Madrid")
        data_frame.sort_index(inplace=True)

        # Add Margin
        data_frame = data_frame + 0.01

        # Rename columns
        data_frame.rename(columns={0: "value_inc_vat"}, inplace=True)

        # From euro/kWh to eurocent/kWh
        data_frame = data_frame * 100
        data_frame["Unit"] = self.unit
        return data_frame


class SomEnergiaInjection(DAPricingCollector):
    """Pricing Collector for Som Energia Injection Prices"""

    supplier = "SomEnergia"
    country = "ES"
    timezone = "Europe/Madrid"
    unit = "c€/kWh"

    def __init__(self, entsoe_api_key: str, **kwargs):
        """Initialize"""
        self.region_code = "ES"
        self.price_name = f"{self.supplier}_injection"
        super().__init__(entsoe_api_key=entsoe_api_key, **kwargs)

    async def get_data(
        self, interval: Optional[pd.Interval] = None
    ):
        """Get Data"""
        price = self.get_da_prices(interval)

        # From euro/MWh to eurocent/kWh

        price = price / 10

        price = pd.DataFrame(price, columns=["value_inc_vat"])
        price["Unit"] = self.unit
        return price
