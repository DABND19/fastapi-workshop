from http import HTTPStatus
from typing import List, Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Query,
    Path,
    Response,
    UploadFile
)

from workshop.db.models import OperationType
from workshop.services import OperationsService, strict_authorizer
from workshop.schemas import (
    OperationSchema,
    OperationCreateSchema,
    OperationUpdateSchema
)


router = APIRouter(prefix='/operations', tags=['Operations'])


@router.get('/', response_model=List[OperationSchema])
def get_operations(
    service: OperationsService = Depends(),
    user_id: int = Depends(strict_authorizer),
    type_: Optional[OperationType] = Query(None, alias='type')
):
    return service.get_operations(user_id, type_=type_)


@router.post('/', response_model=OperationSchema)
def create_operation(
    payload: OperationCreateSchema,
    user_id: int = Depends(strict_authorizer),
    service: OperationsService = Depends()
):
    return service.create_operation(user_id, payload)


@router.get('/{operationId}', response_model=OperationSchema)
def get_operation(
    operation_id: int = Path(alias='operationId'),
    user_id: int = Depends(strict_authorizer),
    service: OperationsService = Depends()
):
    return service.get_operation(user_id, operation_id)


@router.patch('/{operationId}', response_model=OperationSchema)
def update_operation(
    payload: OperationUpdateSchema,
    user_id: int = Depends(strict_authorizer),
    operation_id: int = Path(alias='operationId'),
    service: OperationsService = Depends()
):
    return service.update_operation(user_id, operation_id, payload)


@router.delete('/{operationId}', status_code=HTTPStatus.NO_CONTENT)
def delete_operation(
    operation_id: int = Path(alias='operationId'),
    user_id: int = Depends(strict_authorizer),
    service: OperationsService = Depends()
):
    service.delete_operation(user_id, operation_id)
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.post('/import')
def import_operations(
    background_tasks: BackgroundTasks,
    service: OperationsService = Depends(),
    user_id: int = Depends(strict_authorizer),
    body: UploadFile = File(...)
):
    background_tasks.add_task(
        service.import_operations,
        user_id,
        body.file
    )
    return Response()
