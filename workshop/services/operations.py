import csv
from http import HTTPStatus
from typing import BinaryIO, List, Optional

from fastapi import Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from workshop.db import get_session
from workshop.db.models import Operation, OperationType
from workshop.schemas import OperationCreateSchema, OperationUpdateSchema


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_operations(
        self,
        user_id: int,
        *,
        type_: Optional[OperationType] = None
    ) -> List[Operation]:
        q = self.session.query(Operation).order_by(
            Operation.created_at.desc()
        ).filter_by(
            user_id=user_id
        )

        if type_ is not None:
            q = q.filter_by(type=type_)

        return q.all()

    def create_operation(
        self,
        user_id: int,
        payload: OperationCreateSchema
    ) -> Operation:
        with self.session.begin():
            operation = Operation(
                user_id=user_id,
                **payload.dict()
            )
            self.session.add(operation)
            self.session.flush()
            return operation

    def get_operation(self, user_id: int, operation_id: int) -> Operation:
        operation = self.session.query(Operation).filter_by(
            id=operation_id,
            user_id=user_id
        ).scalar()
        if not operation:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        return operation

    def update_operation(
        self,
        user_id: int,
        operation_id: int, 
        payload: OperationUpdateSchema
    ) -> Operation:
        with self.session.begin():
            operation = self.get_operation(user_id, operation_id)
            for field, value in payload.dict(exclude_unset=True).items():
                setattr(operation, field, value)
            self.session.add(operation)
            self.session.flush()
            return operation

    def delete_operation(
        self,
        user_id: int,
        operation_id: int
    ) -> None:
        with self.session.begin():
            operation = self.get_operation(user_id, operation_id)
            self.session.delete(operation)
            self.session.flush()

    def import_operations(self, user_id: int, file: BinaryIO) -> None:
        try:
            parsed_operations = [
                OperationCreateSchema.parse_obj(record)
                for record in csv.DictReader(
                    map(lambda line: line.decode('utf-8'), file), 
                    skipinitialspace=True
                )
            ]
        except ValidationError:
            return

        with self.session.begin():
            self.session.add_all([
                Operation(user_id=user_id, **payload.dict())
                for payload in parsed_operations
            ])
            self.session.flush()
