# app/models.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class OrgCreate(BaseModel):
    organization_name: str = Field(..., min_length=3)
    admin_email: EmailStr
    admin_password: str = Field(..., min_length=6)

class OrgOut(BaseModel):
    org_name: str
    collection_name: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
