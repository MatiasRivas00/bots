from app.schemas.mongo import BaseSchema, PythonObjectId
from typing import Literal, List
from pydantic import Field, field_validator
from datetime import datetime

class Transaction(BaseSchema):
    user_id: PythonObjectId
    amount: float
    currency: str = "CLP"

    type: Literal["expense", "income"]
    description: str

    category_id: PythonObjectId

    payment_method: Literal["cash", "debit_card", "credit_card","transfer", "other"] = "debit_card"

    tag_ids: List[PythonObjectId] = Field(default_factory=list)  # Hasta 5 tags por transacción
    timestamp: datetime
    message_text: str

    @field_validator("tag_ids")
    def validate_tag_ids_length(cls, v):
        if len(v) > 5:
            raise ValueError("Cannot add more than 5 tags to one Transaction")
        return v