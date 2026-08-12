from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps.auth import get_current_user
from backend.core.security import hash_password
from backend.db.sessions import get_db
from backend.models.users import User
from backend.schemas.users import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])



@router.get("/me", response_model=UserResponse)
async def get_current_user_from_token(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update profile details for the currently logged-in user."""
    if user_in.email is not None and user_in.email != current_user.email:
        # Check if new email is already taken
        result = await db.execute(
            select(User).where(User.email == user_in.email)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        current_user.email = user_in.email

    if user_in.password is not None:
        current_user.hashed_password = hash_password(user_in.password)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user