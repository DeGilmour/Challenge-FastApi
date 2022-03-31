# from typing import Optional
from pydantic import BaseModel


class Plant(BaseModel):
    plant_name: str
    healthy: bool
    type: str | None = None

    class Config:
        orm_mode = True
