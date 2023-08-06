"""Collectors for Octopus Energy"""

import warnings
from typing import Optional

import pandas as pd
from OctopusAgile import Agile

from ..misc import iso8601z
from .octopus_outgoing_workaround import Outgoing
from .pricing import PricingCollector


class Octopus(PricingCollector):
    """Collector for Octopus Agile"""

    country = "UK"
    supplier = "Octopus"
    timezone = "Europe/London"
    unit = "p£/kWh"

    def __init__(self, region_code: str, **kwargs):
        """Initialize"""
        self.region_code = region_code
        self.agile = Agile(region_code)
        self.price_name = f"{self.supplier}_{region_code}"
        super().__init__(**kwargs)

    async def get_data(
        self,
        interval: Optional[pd.Interval] = None,
    ) -> pd.DataFrame:
        """Request data"""
        if not interval:
            rates = self.agile.get_new_rates()
        else:
            date_from = iso8601z(interval.left)
            date_to = iso8601z(interval.right)
            if interval.length.days > 2:
                warnings.warn(
                    "You requested an interval larger than 2 days, "
                    "be advised that the response may not be complete"
                )
            rates = self.agile.get_rates(date_from, date_to)

        rates = pd.DataFrame.from_dict(rates["date_rates"], orient="index")
        # noinspection PyTypeChecker
        rates.index = pd.to_datetime(rates.index)
        rates.rename(columns={0: "value_inc_vat"}, inplace=True)
        rates = rates.tz_convert(self.timezone)
        rates.sort_index(inplace=True)
        rates["Unit"] = self.unit
        return rates


class OctopusOutgoing(Octopus):
    """Collector for Octopus Outgoing Prices"""

    supplier = "Octopus_Outgoing"

    def __init__(self, region_code: str, **kwargs):
        """Initialize"""
        super().__init__(region_code=region_code, **kwargs)
        self.agile = Outgoing(region_code)
