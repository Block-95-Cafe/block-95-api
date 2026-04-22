from typing import Optional

from pydantic import BaseModel, Field


class GetCategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # called orm_mode = True in Pydantic v1


class PostCategorySchema(BaseModel):
    name: str = Field(min_length=1)

    class Config:
        from_attributes = True  # called orm_mode = True in Pydantic v1


class UpdateCategorySchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)

    class Config:
        from_attributes = True  # called orm_mode = True in Pydantic v1
