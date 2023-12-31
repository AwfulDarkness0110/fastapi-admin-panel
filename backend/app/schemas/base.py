import ujson
from pydantic import BaseModel as PydanticModel


# Base config for all schemas.
class BaseModel(PydanticModel):
    class Config:
        json_loads = ujson.loads
        json_dumps = ujson.dumps
        min_anystr_length = 0
        orm_mode = True


class EmptyStrValidator(PydanticModel):
    class Config:
        min_anystr_length = 1
