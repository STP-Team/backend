from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import ValidationError
from stp_database.repo.STP import MainRequestsRepo

from app.core.dependencies import get_repo
from app.schemas.employee import EmployeeRead, EmployeeAll, EmployeeCreate

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.get(
    "/",
    name="Получить всех сотрудников",
    description="Получает список всех сотрудников",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Not found"},
        400: {"description": "Server error"},
    },
    response_model=EmployeeAll,
)
async def get_employees(repo: MainRequestsRepo = Depends(get_repo)):
    try:
        employees_data = await repo.employee.get_users()

        if not employees_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        if not isinstance(employees_data, (list, tuple)):
            employees_data = [employees_data]

        employees = [EmployeeRead.model_validate(emp) for emp in employees_data]

        return EmployeeAll(employees=employees)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Server error: {e}"
        )


@router.get(
    "/{user_id}",
    name="Получить сотрудника",
    description="Получает сотрудника по идентификатору Telegram",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Not found"},
        400: {"description": "Server error"},
    },
    response_model=EmployeeRead,
)
async def get_employee(
    user_id: int,
    repo: MainRequestsRepo = Depends(get_repo),
):
    try:
        employee = await repo.employee.get_users(user_id=user_id)

        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        return employee

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Server error: {e}"
        )


@router.post(
    "/",
    name="Создать сотрудника",
    description="Создает нового сотрудника",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeRead,
)
async def create_employee(
    request: Request,
    employee_data: EmployeeCreate,
    repo: MainRequestsRepo = Depends(get_repo),
):
    """Создает сотрудника в базе данных.

    Args:
        request:
        employee_data: Модель сотрудника с валидацией
        repo: Репозиторий БД

    Returns:
        Модель EmployeeRead при успехе, иначе ошибка
    """
    try:
        employee = await repo.employee.add_user(
            division=employee_data.division,
            position=employee_data.position,
            fullname=employee_data.fullname,
            head=employee_data.head,
            role=employee_data.role,
            user_id=employee_data.user_id,
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
