from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import ValidationError

from backend.api.deps import CurrentUserDep, RepoDep
from backend.schemas.employee import EmployeeDTO, EmployeesList, PatchEmployeeDTO
from backend.schemas.exchanges import ExchangesList

router = APIRouter(
    prefix="/exchanges",
    tags=["Сделки"],
)


@router.get(
    "/",
    name="Получить сделки",
    description="Получает список сделок с фильтрами",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
    },
    response_model=ExchangesList,
)
async def get_exchanges(
    repo: RepoDep,
    _current_user: CurrentUserDep,
):
    try:
        exchanges = await repo.exchange.get_exchanges(
            main_id=main_id,
            user_id=user_id,
            username=username,
            fullname=fullname,
            email=email,
            head=head,
            roles=roles,
        )

        if not exchanges:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        if not isinstance(exchanges, (list, tuple)):
            exchanges = [exchanges]

        exchanges = [EmployeeDTO.model_validate(emp) for emp in exchanges]

        return EmployeesList(employees=exchanges)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {e}",
        )


@router.post(
    "/",
    name="Создать сотрудника",
    description="Создает нового сотрудника",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeDTO,
)
async def create_employee(
    request: Request,
    repo: RepoDep,
    _current_user: CurrentUserDep,
    division: str = Query(str, description="Направление сотрудника"),
    position: str = Query(str, description="Должность сотрудника"),
    fullname: str = Query(str, description="ФИО сотрудника"),
    head: str = Query(str, description="Руководитель сотрудника"),
    role: int = Query(0, description="Роль сотрудника"),
    user_id: int | None = Query(None, description="Идентификатор Telegram сотрудника"),
):
    try:
        employee = await repo.employee.add_user(
            division=division,
            position=position,
            fullname=fullname,
            head=head,
            role=role,
            user_id=user_id,
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось создать сотрудника",
            )

        return employee

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка валидации входных данных: {e}",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path),
                "message": "Внутренняя ошибка сервера при создании сотрудника",
                "errorCode": "INTERNAL_SERVER_ERROR",
            },
        )


@router.patch(
    "/",
    name="Изменить сотрудника",
    description="Изменяет существующего сотрудника",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeDTO,
)
async def patch_employee(
    request: Request,
    repo: RepoDep,
    _current_user: CurrentUserDep,
    payload: PatchEmployeeDTO,
    user_id: int = Query(int, description="Идентификатор Telegram сотрудника"),
):
    try:
        employee = await repo.employee.get_users(user_id=user_id)

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        update_data = payload.model_dump(exclude_unset=True)
        updated = await repo.employee.update_user(user_id, **update_data)

        return updated
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка валидации входных данных: {e}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path),
                "message": "Внутренняя ошибка сервера при обновлении сотрудника",
                "errorCode": "INTERNAL_SERVER_ERROR",
            },
        )


@router.delete(
    "/",
    name="Удалить сотрудника",
    status_code=status.HTTP_200_OK,
)
async def delete_employee(
    request: Request,
    repo: RepoDep,
    _current_user: CurrentUserDep,
    fullname: str | None = Query(None, description="ФИО сотрудника"),
    user_id: int | None = Query(None, description="Идентификатор Telegram сотрудника"),
):
    try:
        deleted_count = await repo.employee.delete_user(
            fullname=fullname, user_id=user_id
        )

        if deleted_count <= 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No one deleted"
            )

        return deleted_count

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка валидации входных данных: {e}",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path),
                "message": "Внутренняя ошибка сервера при удалении сотрудника",
                "errorCode": "INTERNAL_SERVER_ERROR",
            },
        )
