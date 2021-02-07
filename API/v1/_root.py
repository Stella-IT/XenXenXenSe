from typing import List

from pydantic import BaseModel


class XXXS_V1_App(BaseModel):
    version: int
    name: str


class XXXS_V1_Root(BaseModel):
    hello: str
    app: XXXS_V1_App
    clusters: List[str]
