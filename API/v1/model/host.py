from typing import List, Optional

from pydantic import BaseModel


class Memory(BaseModel):
    free: str
    total: str


class CPU(BaseModel):
    cpu_count: str
    socket_count: str
    vendor: str
    speed: str
    modelname: str
    family: str
    model: str
    stepping: str
    flags: str
    features: str
    features_pv: str
    features_hvm: str


class Version(BaseModel):
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
    system_serial_number: str
    oem_1: str
    oem_2: str
    oem_3: str
    oem_4: str
    hp_rombios: str


class DataModel(BaseModel):
    uuid: str
    name: str
    description: Optional[str]
    enabled: bool
    memory: Memory
    cpu: CPU
    bios: BIOS
    version: Version


class HostListResponseModel(BaseModel):
    success: bool
    data: List[DataModel]
