from typing import List, Optional

from pydantic import BaseModel


class IPModel(BaseModel):
    address: str
    gateway: Optional[str]


class IPAddressModel(BaseModel):
    address: str


class IPAddressesModel(BaseModel):
    addresses: List[str]


class ModeModel(BaseModel):
    mode: str
