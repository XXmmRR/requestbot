import datetime
from sqlalchemy import func
from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column

@declarative_mixin
class TimeStampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        insert_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )