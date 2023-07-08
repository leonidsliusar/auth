import re
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, field_validator


class UserInput(BaseModel):
    password: str = Field(examples=['Pass2000'])
    email: EmailStr = Field(examples=['foo@example.com'])

    @field_validator('password')
    def validate_password(cls, password):
        pattern = r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])[A-Za-z\d]{8,}$'
        if re.match(pattern, password):
            return password
        else:
            raise ValueError(
                'The password isn\'t strong enough:\nMinimum eight characters, at least one uppercase latin letter, '
                'one lowercase latin letter and one number'
            )


class UserOutput(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
