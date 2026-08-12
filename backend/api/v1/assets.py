from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps.auth import get_current_user
from backend.api.deps.assets import create_new_asset, get_my_assets
from backend.db.sessions import get_db
from backend.models.users import User
from backend.schemas.assets import AssetBase, AssetCreateResponse

router = APIRouter(
    prefix="/assets",
    tags=["assets"]
)


@router.post(
    "/new_asset", 
    response_model=AssetCreateResponse, 
    status_code=status.HTTP_201_CREATED
)
async def new_assets(
    asset: AssetBase,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await create_new_asset(asset_in=asset, db=db, current_user=current_user)


@router.get("/me", response_model=list[AssetCreateResponse])
async def read_my_assets(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_my_assets(db=db, current_user=current_user)