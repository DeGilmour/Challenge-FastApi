from pydantic import BaseModel


class Sprinkler(BaseModel):
    water_flow: int
    sprinkler_name: str
    problems: bool | None = None

    class Config:
        orm_mode = True
