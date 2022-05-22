from datetime import datetime
from enum import Enum

import sqlalchemy as sa

from .base import Base
from .user import User


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
    updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)
    amount = sa.Column(sa.Numeric(10, 2), nullable=False)
    type = sa.Column(OperationTypeEnum, nullable=False)
    description = sa.Column(sa.String(256))
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False)
