from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from backend.db.base import Base
from typing import Optional, List

class Asset(Base):
    __tablename__ = "assets"

    id : Mapped[int] = mapped_column(primary_key=True)
    owner : Mapped[int] = mapped_column()

    title : Mapped[str] = mapped_column()
    description : Mapped[str] = mapped_column()

    longitude : Mapped[float] = mapped_column()
    latitude : Mapped[float] = mapped_column()