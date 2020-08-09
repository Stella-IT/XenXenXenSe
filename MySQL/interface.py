from pydantic import BaseModel


class credentials_interface(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db: str
    charset: str
