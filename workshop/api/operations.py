from http import HTTPStatus
from typing import List, Optional

from fastapi import (
    APIRouter, 
    Depends, 
    Query, 
    Path
)

from workshop.db.models import OperationType
from workshop.services import OperationsService
from workshop.schemas import (
    OperationSchema, 
    OperationCreateSchema, 
    OperationUpdateSchema
)


router = APIRouter(prefix='/operations', tags=['Operations'])


@router.get('/', response_model=List[OperationSchema])
def get_operations(
    service: OperationsService = Depends(),
    type_: Optional[OperationType] = Query(None, alias='type')
):
    return service.get_operations(type_=type_)


@router.post('/', response_model=OperationSchema)
def create_operation(
    payload: OperationCreateSchema, 
    service: OperationsService = Depends()
):
    return service.create_operation(payload)


@router.get('/{operationId}', response_model=OperationSchema)
def get_operation(
    operation_id: int = Path(alias='operationId'),
    service: OperationsService = Depends()
):
    return service.get_operation(operation_id)


@router.patch('/{operationId}', response_model=OperationSchema)
def update_operation(
    payload: OperationUpdateSchema,
    operation_id: int = Path(alias='operationId'),
    service: OperationsService = Depends()
):
    return service.update_operation(operation_id, payload)


@router.delete('/{operationId}', status_code=HTTPStatus.NO_CONTENT)
def delete_operation(
    operation_id: int = Path(alias='operationId'),
    service: OperationsService = Depends()
):
    service.delete_operation(operation_id)
