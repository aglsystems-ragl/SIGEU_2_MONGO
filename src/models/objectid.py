from typing import Any, Optional
from bson import ObjectId

from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic.json_schema import GetJsonSchemaHandler, JsonSchemaValue
from pydantic_core import core_schema


# ============================================================
#  PYOBJECTID COMPATIBLE CON PYDANTIC v2
# ============================================================

class PyObjectId(ObjectId):
    """Tipo personalizado para ObjectId que funciona con Pydantic v2."""

    @classmethod
    def validate(cls, v: Any) -> "PyObjectId":
        if isinstance(v, ObjectId):
            return cls(str(v))
        if isinstance(v, str) and ObjectId.is_valid(v):
            return cls(v)
        raise TypeError(f"Valor inválido para ObjectId: {v!r}")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(pattern="^[a-fA-F0-9]{24}$"),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(cls),
                core_schema.no_info_after_validator_function(cls.validate, core_schema.str_schema()),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: str(v),
                when_used="json"
            )
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema_: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema_)
        json_schema.update(
            type="string",
            pattern="^[a-fA-F0-9]{24}$",
            examples=["60c5ba2d8f1b2c3d4e5f6789"],
        )
        return json_schema


# ============================================================
#  MONGOMODEL — BASE PARA MODELOS DE MONGO (COMPATIBLE CON PYDANTIC v2)
# ============================================================

class MongoModel(BaseModel):
    """
    Clase base para todos los modelos que se guardan en MongoDB.
    - Convierte `_id` de Mongo a `id` visible en API.
    - Permite serialización correcta.
    """

    id: Optional[PyObjectId] = Field(
        default=None,
        alias="_id",
        description="ID del documento en MongoDB"
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
