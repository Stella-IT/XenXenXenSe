from typing import Optional

from pydantic import BaseModel


class VCpuArgs(BaseModel):
    vCPU_count: int


class MemoryArgs(BaseModel):
    memory: int


class NameArgs(BaseModel):
    name: str


class NameDescriptionArgs(BaseModel):
    name: Optional[str]
    description: Optional[str]


class UUIDArgs(BaseModel):
    uuid: str
