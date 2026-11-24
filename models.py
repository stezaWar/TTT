from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RefundRequest(BaseModel):
    """Запрос на возврат товара."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    order_id: str = Field(min_length=1, description="Идентификатор заказа")
    reason: str = Field(min_length=10, description="Причина возврата, минимум 10 символов")
    refund_amount: Decimal = Field(gt=0, description="Сумма возврата, строго больше 0")

    @field_validator("order_id")
    @classmethod
    def order_id_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("order_id не может быть пустым")
        return value

    @field_validator("reason")
    @classmethod
    def reason_must_be_meaningful(cls, value: str) -> str:
        if len(value) < 10:
            raise ValueError("reason должна содержать минимум 10 символов")
        return value
