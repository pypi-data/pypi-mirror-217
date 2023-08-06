"""Dynamic Energy pricing collectors"""

from abc import ABC
from typing import Optional

import pandas as pd
from entsoe import EntsoePandasClient

from ..abstract import Collector


class PricingCollector(Collector, ABC):
    """Abstract collector for pricing data"""

    country: str = NotImplemented
    supplier: str = NotImplemented
    timezone: str = NotImplemented
    unit: str = NotImplemented

    def __init__(self, **kwargs):
        """Initialize"""
        super().__init__()


class DAPricingCollector(PricingCollector):
    """Abstract class for pricing collectors using DA-prices from ENTSOE"""

    def __init__(self, entsoe_api_key: str, **kwargs):
        """Initialize"""
        self.entsoe_client = EntsoePandasClient(api_key=entsoe_api_key)
        super().__init__(**kwargs)

    def get_da_prices(self, interval: Optional[pd.Interval] = None) -> pd.Series:
        """Request Day-ahead prices from ENTSOE"""
        if not interval:
            interval = pd.Interval(
                pd.Timestamp.now(tz=self.timezone).floor("H"),
                (pd.Timestamp.now(tz=self.timezone) + pd.Timedelta(days=2)).normalize(),
            )
        epex = self.entsoe_client.query_day_ahead_prices(
            country_code=self.country, start=interval.left, end=interval.right
        )
        return epex
