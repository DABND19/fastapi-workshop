from http import HTTPStatus
from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from workshop.db import get_session
from workshop.db.models import Operation, OperationType
from workshop.schemas import OperationCreateSchema, OperationUpdateSchema


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_operations(
        self,
        *,
        type_: Optional[OperationType] = None
    ) -> List[Operation]:
        q = self.session.query(Operation).order_by(
            Operation.created_at.desc()
        )

        if type_ is not None:
            q = q.filter_by(type=type_)

        return q.all()

    def create_operation(
        self, 
        payload: OperationCreateSchema
    ) -> Operation:
        with self.session.begin():
            operation = Operation(
                amount=payload.amount,
                type=payload.type,
                description=payload.description
            )
            self.session.add(operation)
            self.session.flush()
            return operation

    def get_operation(self, operation_id: int) -> Operation:
        operation = self.session.query(Operation).get(operation_id)
        if not operation:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        return operation

    def update_operation(
        self, 
        operation_id: int, 
        payload: OperationUpdateSchema
    ) -> Operation:
        with self.session.begin():
            operation = self.get_operation(operation_id)
            for field, value in payload.dict(exclude_unset=True).items():
                setattr(operation, field, value)
            self.session.add(operation)
            self.session.flush()
            return operation

    def delete_operation(
        self,
        operation_id: int
    ) -> None:
        with self.session.begin():
            operation = self.get_operation(operation_id)
            self.session.delete(operation)
            self.session.flush()
