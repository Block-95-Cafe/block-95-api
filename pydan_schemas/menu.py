from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MenuItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    oz: int


class GetMenuItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    oz: int


class PostMenuItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    oz: int = Field(gt=0)
    category_id: int = Field(gt=0)


class UpdateMenuItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(default=None, min_length=1)
    price: Optional[float] = Field(default=None, gt=0)
    oz: Optional[int] = Field(default=None, gt=0)
    category_id: Optional[int] = Field(default=None, gt=0)
