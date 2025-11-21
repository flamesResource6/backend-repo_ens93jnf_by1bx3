from __future__ import annotations

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# Each Pydantic model corresponds to a MongoDB collection (lowercased)


class Message(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=5000)


class Project(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    tech: List[str] = []
    link: Optional[str] = None


class TestPing(BaseModel):
    status: str
