from typing import List, Optional

from pydantic import BaseModel


class MEMORY(BaseModel):
    free: int
    total: int


class CPU(BaseModel):
    cpu_count: int
    socket_count: int
    vendor: str
    speed: float
    modelname: str
    family: int
    model: int
    stepping: int
    flags: str
    features: str
    features_pv: str
    features_hvm: str


class VERSION(BaseModel):
    product_version: str
    product_version_text: str
    product_version_text_short: str
    platform_name: str
    platform_version: str
    product_brand: str
    build_number: str
    hostname: str
    date: str
    dbv: str
    xapi: str
    xen: str
    linux: str
    xencenter_min: str
    xencenter_max: str
    network_backend: str
    db_schema: str


class BIOS(BaseModel):
    bios_vendor: str
    bios_version: str
    system_manufacturer: str
    system_product_name: str
    system_version: str
    system_serial_number: int
    oem_1: Optional[str]
    oem_2: Optional[str]
    oem_3: Optional[str]
    oem_4: Optional[str]
    hp_rombios: str


class DATA(BaseModel):
    uuid: str
    name: str
    description: Optional[str]
    enabled: bool
    memory: MEMORY
    cpu: CPU
    bios: BIOS
    version: VERSION


class HLResponseModel(BaseModel):
    success: bool
    data: List[DATA]
