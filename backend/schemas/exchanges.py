from datetime import datetime

from pydantic import BaseModel


class ExchangeDTO(BaseModel):
    id: int
    owner_id: int
    counterpart_id: int
    start_time: datetime
    end_time: datetime
    price: int
    is_paid: bool
    payment_type: str
    payment_date: datetime
    owner_intent: str
    status: str
    is_private: bool
    in_owner_schedule: bool
    in_counterpart_schedule: bool
    comment: str
    created_at: datetime
    updated_at: datetime
    sold_at: datetime

    class Config:
        from_attributes = True


class ExchangesList(BaseModel):
    exchanges: list[ExchangeDTO]


class PatchExchangeDTO(BaseModel):
    owner_id: int | None = None
    counterpart_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    price: int | None = None
    is_paid: bool | None = None
    payment_type: str | None = None
    payment_date: datetime | None = None
    owner_intent: str | None = None
    status: str | None = None
    is_private: bool | None = None
    in_owner_schedule: bool | None = None
    in_counterpart_schedule: bool | None = None
    comment: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    sold_at: datetime | None = None
