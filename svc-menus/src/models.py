from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v, values):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class IngredienteExtra(BaseModel):
    nombre: str
    precio: float

class Plato(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    nombre: str
    descripcion: str
    precio: float
    extras: List[IngredienteExtra] = []

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}