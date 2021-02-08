from pydantic import BaseModel
from typing import List, Optional


class IPModel(BaseModel):
    address: str
    gateway: Optional[str]

class IPAddressModel(BaseModel):
    address: str
    
class IPAddressesModel(BaseModel):
    addresses: List[str]

class ModeModel(BaseModel):
    mode: str
