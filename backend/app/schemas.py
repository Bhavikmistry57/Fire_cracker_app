import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: int
    unit: str
    image_url: str | None = None

    model_config = {"from_attributes": True}


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=99)


class OrderCreate(BaseModel):
    customer_name: str
    whatsapp: str
    address: str
    items: list[OrderItemIn] = Field(min_length=1, max_length=30)

    @field_validator("customer_name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if not 2 <= len(cleaned) <= 80:
            raise ValueError("Enter your name (2 to 80 characters)")
        return cleaned

    @field_validator("address")
    @classmethod
    def clean_address(cls, value: str) -> str:
        lines = [" ".join(line.split()) for line in value.splitlines()]
        cleaned = "\n".join(line for line in lines if line)
        if not 10 <= len(cleaned) <= 400:
            raise ValueError("Enter a delivery address (at least 10 characters)")
        return cleaned

    @field_validator("whatsapp")
    @classmethod
    def indian_mobile(cls, value: str) -> str:
        digits = re.sub(r"\D", "", value)
        if len(digits) == 12 and digits.startswith("91"):
            digits = digits[2:]
        if len(digits) == 11 and digits.startswith("0"):
            digits = digits[1:]
        if not re.fullmatch(r"[6-9]\d{9}", digits):
            raise ValueError("Enter a 10-digit Indian mobile number")
        return digits


class OrderItemOut(BaseModel):
    product_id: int
    name: str
    unit: str
    quantity: int
    unit_price: int
    line_total: int


class OrderOut(BaseModel):
    id: int
    customer_name: str
    whatsapp: str
    address: str
    items: list[OrderItemOut]
    total: int
    created_at: datetime
    message: str
    whatsapp_url: str | None
