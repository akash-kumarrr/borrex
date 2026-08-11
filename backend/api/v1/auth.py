from typing import Annotated
from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import (
    create_access_token, 
    verify_password,
    hash_password
)

from backend.db.sessions import get_db
from backend.models.users import User
from backend.schemas.users import UserResponse, UserCreate, UserBase

auth_router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@auth_router.get("/")
async def root():
    return {
        "message" : "route for authentication system"
    }

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in : UserCreate, 
    db:Annotated[AsyncSession, Depends(get_db)]
):
    try : 
        result = await db.execute(select(User).where(User.email == user_in.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        new_user = User(
            email = user_in.email,
            hashed_password = hash_password(user_in.password)
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except HTTPException:
        raise

@auth_router.post("/login")
async def login(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()], 
    db:Annotated[AsyncSession, Depends(get_db)]
) :
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authentification" : "Bearer"},
        )

    access_token = create_access_token(
        subject=user.id
    )

    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }

    