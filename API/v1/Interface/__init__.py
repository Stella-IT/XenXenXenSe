from typing import Optional

from pydantic import BaseModel


class VCpuArgs(BaseModel):
    vCPU_count: int


class MemoryArgs(BaseModel):
    memory: int


class NameArgs(BaseModel):
    name: str


class CopyArgs(NameArgs):
    sr_uuid: str
    provision: bool = True


class SRCopyArgs(BaseModel):
    sr_uuid: str


class QoSTypeArgs(BaseModel):
    type: str
    info: dict


class VBDCreateArgs(BaseModel):
    vm_uuid: str
    vdi_uuid: str
    userdevice: str = "0"
    bootable: bool = True
    mode: str = "RW"
    type: str = "Disk"
    empty: bool = False
    qos_algorithm_type: str = ""
    qos_algorithm_params: dict = {}
    other_config: dict = {}
    unpluggable: Optional[bool] = True
    currently_attached: Optional[bool] = False


class CloneArgs(NameArgs):
    provision: bool = True


class NameDescriptionArgs(BaseModel):
    name: Optional[str]
    description: Optional[str]


class UUIDArgs(BaseModel):
    uuid: str


class SizeArgs(BaseModel):
    size: str
