from pydantic import BaseModel, EmailStr, Field


class RequestLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=20)


class RequestSignupSchema(BaseModel):
    email: EmailStr
    name: str
    password: str = Field(min_length=4, max_length=20)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
