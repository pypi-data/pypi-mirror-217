"""Factory method to create a collector based on an input dict"""

from typing import Dict

from .abstract import Collector, CollectorType
from .pricing_collectors import (
    Ecopower,
    Enercoop,
    Engie,
    Octopus,
    OctopusOutgoing,
    SomEnergiaInjection,
    SomEnergiaOfftake,
)


def create_collector(collector_type: CollectorType, body: Dict, **kwargs) -> Collector:
    """Factory to create any collector based on input dict"""
    if collector_type == CollectorType.PRICE:
        supplier = body["supplier"]
        if supplier == "Octopus":
            region_code = body["regionCode"]
            return Octopus(region_code=region_code)
        if supplier == "Octopus_Outgoing":
            region_code = body["regionCode"]
            return OctopusOutgoing(region_code=region_code)
        if supplier == "Ecopower":
            region_code = body["regionCode"]
            direction = body["direction"]
            consumer_type = body["consumerType"]
            return Ecopower(
                region_code=region_code,
                direction=direction,
                consumer_type=consumer_type,
                **kwargs,
            )
        if supplier == "Engie":
            region_code = body["regionCode"]
            direction = body["direction"]
            consumer_type = body["consumerType"]
            return Engie(
                region_code=region_code,
                direction=direction,
                consumer_type=consumer_type,
                **kwargs,
            )
        if supplier == "Enercoop":
            tariff = body["tariff"]
            return Enercoop(tariff=tariff, **kwargs)
        if supplier == "SomEnergia":
            direction = body["direction"]
            if direction == "consumption":
                return SomEnergiaOfftake(**kwargs)
            if direction == "injection":
                return SomEnergiaInjection(**kwargs)
            else:
                raise LookupError(f"Direction {direction} not supported for SomEnergia")
        else:
            raise LookupError(f"Supplier {supplier} not supported, or unknown")
    else:
        raise NotImplementedError(
            f"Collector Type {collector_type} not yet " f"supported"
        )
