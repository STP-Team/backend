from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    user_id: int | None = None
    division: str
    position: str
    fullname: str
    head: str
    role: int = 0


class EmployeeRead(BaseModel):
    id: int
    user_id: int | None
    username: str | None
    division: str | None
    position: str | None
    fullname: str
    head: str | None
    email: str | None
    role: int
    is_trainee: bool
    is_casino_allowed: bool
    is_exchange_banned: bool

    class Config:
        from_attributes = True


class EmployeeSearch(BaseModel):
    main_id: int | None
    user_id: int | None


class EmployeeAll(BaseModel):
    employees: list[EmployeeRead]
