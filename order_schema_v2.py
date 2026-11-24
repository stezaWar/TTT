from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderItem(BaseModel):
    """Позиция заказа."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    sku: str = Field(min_length=3, max_length=32, description="Артикул товара")
    quantity: int = Field(gt=0, le=1000, description="Количество, от 1 до 1000")
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class Order(BaseModel):
    """Эталонная модель заказа (Pydantic v2)."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    order_id: str = Field(min_length=1, description="Идентификатор заказа")
    customer_email: str = Field(description="Email покупателя")
    items: list[OrderItem] = Field(min_length=1, description="Минимум одна позиция")
    comment: str | None = Field(default=None, max_length=500)

    @field_validator("order_id")
    @classmethod
    def order_id_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("order_id не может быть пустым")
        return value

    @field_validator("customer_email")
    @classmethod
    def email_must_contain_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("customer_email должен содержать символ '@'")
        return value.lower()
