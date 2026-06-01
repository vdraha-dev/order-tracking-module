from decimal import Decimal

from pydantic import BaseModel, ValidationError, model_validator


class ProductBase(BaseModel):
    name: str
    price: Decimal
    stock: int


class ProductCreate(ProductBase): ...


class ProductResponse(ProductBase):
    id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    stock: int | None = None

    @model_validator(mode="after")
    def validate(self):
        if not any([self.name, self.price, self.stock]):
            raise ValidationError("At least one field must be provided")
        return self
