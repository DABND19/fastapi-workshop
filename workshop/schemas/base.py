import humps
from pydantic import BaseModel


class APISchema(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = humps.camelize
        orm_mode = True
