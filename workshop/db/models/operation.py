from datetime import datetime
from enum import Enum

import sqlalchemy as sa

from .base import Base


class OperationType(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'


OperationTypeEnum = sa.Enum(
    OperationType,
    name='operation_type_enum'
)


class Operation(Base):
    __tablename__ = 'operation'

    id = sa.Column('operation_id', sa.Integer,
                   autoincrement=True, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True),
                           nullable=False, default=datetime.utcnow)
    amount = sa.Column(sa.Numeric(10, 2), nullable=False)
    type = sa.Column(OperationTypeEnum, nullable=False)
    description = sa.Column(sa.String(256))
