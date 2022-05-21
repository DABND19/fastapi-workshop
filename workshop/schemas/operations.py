from datetime import datetime
from typing import Optional
from decimal import Decimal

from pydantic import Field

from workshop.db.models import OperationType

from .base import APISchema


class OperationBaseSchema(APISchema):
    amount: Decimal
    type: OperationType
    description: Optional[str] = Field(max_length=256)


class OperationCreateSchema(OperationBaseSchema):
    pass


class OperationUpdateSchema(OperationCreateSchema):
    amount: Optional[Decimal]
    type: Optional[OperationType]


class OperationSchema(OperationBaseSchema):
    id: int
    created_at: datetime
