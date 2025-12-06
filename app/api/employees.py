from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import ValidationError

from app.core.db import RepoDep
from app.schemas.employee import EmployeeDTO, EmployeesList, PatchEmployeeDTO

router = APIRouter(
    prefix="/api/employees",
    tags=["Сотрудники"],
)


@router.get(
    "/",
    name="Получить сотрудников",
    description="Получает список сотрудников с фильтрами",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
    },
    response_model=EmployeesList,
)
async def get_employees(
    repo: RepoDep,
    main_id: int | None = Query(None, description="Основной идентификатор"),
    user_id: int | None = Query(None, description="Идентификатор Telegram"),
    username: str | None = Query(None, description="Имя пользователя Telegram"),
    fullname: str | None = Query(None, description="ФИО"),
    email: str | None = Query(None, description="Рабочая почта"),
    head: str | None = Query(None, description="ФИО руководителя"),
    roles: list[int] | None = Query(None, description="Роли"),
):
    try:
        employees = await repo.employee.get_users(
            main_id=main_id,
            user_id=user_id,
            username=username,
            fullname=fullname,
            email=email,
            head=head,
            roles=roles,
        )

        if not employees:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        if not isinstance(employees, (list, tuple)):
            employees = [employees]

        employees = [EmployeeDTO.model_validate(emp) for emp in employees]

        return EmployeesList(employees=employees)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {e}",
        ) from e


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
        ) from e

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path),
                "message": "Внутренняя ошибка сервера при создании сотрудника",
                "errorCode": "INTERNAL_SERVER_ERROR",
            },
        ) from None


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
        ) from e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path),
                "message": "Внутренняя ошибка сервера при обновлении сотрудника",
                "errorCode": "INTERNAL_SERVER_ERROR",
            },
        ) from None


@router.delete(
    "/",
    name="Удалить сотрудника",
    status_code=status.HTTP_200_OK,
)
async def delete_employee(
    request: Request,
    repo: RepoDep,
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
        ) from e

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path),
                "message": "Внутренняя ошибка сервера при удалении сотрудника",
                "errorCode": "INTERNAL_SERVER_ERROR",
            },
        ) from None
