from typing import List, Optional

from pydantic import BaseModel


class VIFCreateModel(BaseModel):
    device: str
    network: str
    vm: str
    mac: str
    mtu: int
    other_config: Optional[dict]
    qos_algorithm_type: Optional[str]
    qos_algorithm_params: Optional[dict]

    # - Optional -
    currently_attached: Optional[bool]
    locking_mode: Optional[str]
    ipv4_allowed: Optional[List[str]]
    ipv6_allowed: Optional[List[str]]


class IPModel(BaseModel):
    address: str
    gateway: Optional[str]


class IPAddressModel(BaseModel):
    address: str


class IPAddressesModel(BaseModel):
    addresses: List[str]


class ModeModel(BaseModel):
    mode: str
