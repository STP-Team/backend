from pydantic import BaseModel


class EmployeeDTO(BaseModel):
    id: int
    fullname: str
    role: int
    user_id: int | None
    username: str | None
    division: str | None
    position: str | None
    head: str | None
    email: str | None
    is_trainee: bool
    is_casino_allowed: bool
    is_exchange_banned: bool

    class Config:
        from_attributes = True


class EmployeesList(BaseModel):
    employees: list[EmployeeDTO]


class PatchEmployeeDTO(BaseModel):
    fullname: str | None = None
    role: int | None = None
    user_id: int | None = None
    username: str | None = None
    division: str | None = None
    position: str | None = None
    head: str | None = None
    email: str | None = None
    is_trainee: bool | None = None
    is_casino_allowed: bool | None = None
    is_exchange_banned: bool | None = None
