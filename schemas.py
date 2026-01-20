from pydantic import BaseModel
from datetime import date


class StudentSchema(BaseModel):
    id: int = None
    name: str
    birth_date: date = None