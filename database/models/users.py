from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Float, BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from database.ini import Base
from database.mixins import TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(Float)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    mention: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.mention!r}, id={self.id!r})"
