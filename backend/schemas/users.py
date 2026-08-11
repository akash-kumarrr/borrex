#schemas for user

from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
	email : EmailStr

class UserCreate(UserBase):
	password : str

class UserResponse(UserBase):
	id : int
	is_active : bool

	model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None