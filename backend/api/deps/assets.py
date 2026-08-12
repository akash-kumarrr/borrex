from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.assets import Asset
from backend.models.users import User
from backend.schemas.assets import AssetBase


async def create_new_asset(
    asset_in: AssetBase,
    db: AsyncSession,
    current_user: User,
) -> Asset:
    try:
        new_asset = Asset(
            owner=current_user.id,  # Set foreign key column 'owner' to current_user.id
            title=asset_in.title,
            description=asset_in.description,
            longitude=asset_in.longitude,
            latitude=asset_in.latitude,
        )
        db.add(new_asset)
        await db.commit()
        await db.refresh(new_asset)
        return new_asset

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def get_my_assets(
    db: AsyncSession,
    current_user: User,
) -> list[Asset]:
    try:
        # Match Asset.owner column with current_user.id
        stmt = select(Asset).where(Asset.owner == current_user.id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )