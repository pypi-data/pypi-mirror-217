"""Pricing Collectors for France"""

import io
from typing import Optional

import pandas as pd
import requests

from .pricing import PricingCollector


class Enercoop(PricingCollector):
    """Pricing Collector for Enercoop Dynamic Prices"""

    supplier = "Enercoop"
    country = "FR"
    timezone = "Europe/Paris"
    unit = "c€/kWh"
    base_url = (
        "https://oos.eu-west-2.outscale.com/enercoop-data-rescoopvpp/base/flex_signal_"
    )

    def __init__(self, tariff: str, **kwargs):
        """Initialize"""
        self.tariff = tariff
        self.price_name = f"{self.supplier}_{tariff}"
        self.region_code = "FR"
        self.session = requests.Session()
        super().__init__(**kwargs)

    def _download_csv(self, url: str) -> bytes:
        request = self.session.get(url, timeout=30)
        request.raise_for_status()
        return request.content

    def _download_csv_for_date(self, date: pd.Timestamp) -> bytes:
        url = self.base_url + date.strftime("%Y-%m-%d") + ".csv"
        return self._download_csv(url)

    def _download_current_csv(self) -> bytes:
        return self._download_csv_for_date(pd.Timestamp.now(tz=self.timezone))

    def _parse_csv(self, csv: bytes) -> pd.DataFrame:
        data_frame = pd.read_csv(
            io.BytesIO(csv), parse_dates=["time"], index_col="time"
        )
        data_frame = data_frame.tz_convert(self.timezone)
        return data_frame

    async def get_data(
        self,
        interval: Optional[pd.Interval] = None,  # Not used
        csv: Optional[bytes] = None,
    ) -> pd.DataFrame:
        """Get Data"""
        if csv is None:
            csv = self._download_current_csv()
        data_frame = self._parse_csv(csv)

        # Select tariff
        data_series = data_frame[self.tariff]
        data_series.rename("value_inc_vat", inplace=True)
        # From euro/MWh to eurocent/kWh
        data_series = data_series / 10

        data_frame = pd.DataFrame(data_frame, columns=["value_inc_vat"])
        data_frame["Unit"] = self.unit
        return data_frame
