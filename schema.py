import pydantic
from errors import HttpError

class AnnouncementCreate(pydantic.BaseModel):
    title: str
    descr: str
    owner: str

class AnnouncementUpdate(pydantic.BaseModel):
    title: str | None = None
    descr: str | None = None
    owner: str | None = None

def validate_json(json_data: dict, schema_cls: type[AnnouncementCreate] | type[AnnouncementUpdate]):
    try:
        schema_obj = schema_cls(**json_data)
        return schema_obj.model_dump(exclude_unset=True)
    except pydantic.ValidationError as e:
        errors = e.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)