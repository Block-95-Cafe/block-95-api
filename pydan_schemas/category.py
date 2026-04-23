from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from pydan_schemas.menu import MenuItemSchema


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class GetCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    items: list[MenuItemSchema]


class PostCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=1)


class UpdateCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(default=None, min_length=1)
