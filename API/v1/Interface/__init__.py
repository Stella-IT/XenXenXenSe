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


class CloneArgs(NameArgs):
    provision: bool = True


class NameDescriptionArgs(BaseModel):
    name: Optional[str]
    description: Optional[str]


class UUIDArgs(BaseModel):
    uuid: str
