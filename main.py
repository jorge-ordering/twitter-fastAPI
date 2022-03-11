from datetime import date
from typing import Optional
from uuid import UUID

# Pydantic
from pydantic import BaseModel, EmailStr, Field

# FastAPI
from fastapi import FastAPI

app = FastAPI()

#models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    birth_date: Optional[date] = Field(default=None)
class Tweet(BaseModel):
    pass

@app.get(path="/")
def home():
    return {"Twitter API": "Working"}
