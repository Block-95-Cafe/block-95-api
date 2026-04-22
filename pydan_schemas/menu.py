from typing import Optional

from pydantic import BaseModel, Field

from pydan_schemas.category import GetCategorySchema


class PostMenuItemSchema(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    oz: int = Field(gt=0)
    category_id: int = Field(gt=0)

    class Config:
        from_attributes = True  # called orm_mode = True in Pydantic v1


class GetMenuItemSchema(BaseModel):
    id: int
    name: str
    price: float
    oz: int
    category: GetCategorySchema

    class Config:
        from_attributes = True  # called orm_mode = True in Pydantic v1


class UpdateMenuItemSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    price: Optional[float] = Field(default=None, gt=0)
    oz: Optional[int] = Field(default=None, gt=0)
    category_id: Optional[int] = Field(default=None, gt=0)

    class Config:
        from_attributes = True  # called orm_mode = True in Pydantic v1
