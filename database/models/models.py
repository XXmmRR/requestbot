from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Float, BigInteger, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.ini import Base
from database.mixins.timestamp import TimeStampMixin

class User(Base, TimeStampMixin):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(Float)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    mention: Mapped[str] = mapped_column(String(50), index=True)

    entries: Mapped[List["Entry"]] = relationship(back_populates="created_by_user")
    tickets_submitted: Mapped[List["Ticket"]] = relationship(
        foreign_keys="[Ticket.submitted_by]", back_populates="submitted_by_user"
    )
    tickets_moderated: Mapped[List["Ticket"]] = relationship(
        foreign_keys="[Ticket.moderator_id]", back_populates="moderator"
    )
    queries: Mapped[List["Query"]] = relationship(back_populates="user")
    payments: Mapped[List["Payment"]] = relationship(back_populates="user")
    watchlist_items: Mapped[List["Watchlist"]] = relationship(back_populates="user")
    events: Mapped[List["Event"]] = relationship(back_populates="user")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user")
    referrals_invited: Mapped[List["Referral"]] = relationship(
        foreign_keys="[Referral.inviter_id]", back_populates="inviter"
    )
    referrals_as_invitee: Mapped[List["Referral"]] = relationship(
        foreign_keys="[Referral.invitee_id]", back_populates="invitee"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.mention!r}, id={self.id!r})"


class Entry(Base, TimeStampMixin):
    __tablename__ = "entries"
    entry_id: Mapped[int] = mapped_column(primary_key=True)
    name_key: Mapped[str] = mapped_column(String, index=True)
    aliases: Mapped[dict] = mapped_column(JSON)
    region: Mapped[str] = mapped_column(String, index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("user_account.id"), index=True)
    status: Mapped[str] = mapped_column(String, index=True)
    merged_into: Mapped[Optional[int]] = mapped_column(ForeignKey("entries.entry_id"), index=True)

    created_by_user: Mapped["User"] = relationship(back_populates="entries")
    evidences: Mapped[List["Evidence"]] = relationship(back_populates="entry")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="entry")
    queries: Mapped[List["Query"]] = relationship(back_populates="entry")
    watchlist_items: Mapped[List["Watchlist"]] = relationship(back_populates="entry")
    events: Mapped[List["Event"]] = relationship(back_populates="entry")


class Evidence(Base):
    __tablename__ = "evidence"
    evidence_id: Mapped[int] = mapped_column(primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entries.entry_id"), index=True)
    file_ref: Mapped[str] = mapped_column(String, index=True)
    kind: Mapped[str] = mapped_column(String, index=True)
    
    entry: Mapped["Entry"] = relationship(back_populates="evidences")


class Ticket(Base, TimeStampMixin):
    __tablename__ = "tickets"
    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entries.entry_id"), index=True)
    submitted_by: Mapped[int] = mapped_column(ForeignKey("user_account.id"), index=True)
    status: Mapped[str] = mapped_column(String, index=True)
    reason: Mapped[str] = mapped_column(String)
    moderator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user_account.id"), index=True)
    notes: Mapped[str] = mapped_column(String)
    
    entry: Mapped["Entry"] = relationship(back_populates="tickets")
    submitted_by_user: Mapped["User"] = relationship(foreign_keys=[submitted_by])
    moderator: Mapped[Optional["User"]] = relationship(foreign_keys=[moderator_id])


class Query(Base, TimeStampMixin):
    __tablename__ = "queries"
    query_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), index=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entries.entry_id"), index=True)
    result_level: Mapped[str] = mapped_column(String, index=True)
    charged: Mapped[bool] = mapped_column()
    
    user: Mapped["User"] = relationship(back_populates="queries")
    entry: Mapped["Entry"] = relationship(back_populates="queries")


class Payment(Base):
    __tablename__ = "payments"
    payment_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), index=True)
    invoice_id: Mapped[str] = mapped_column(String, index=True)
    sku: Mapped[str] = mapped_column(String, index=True)
    type: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, index=True)
    provider: Mapped[str] = mapped_column(String, index=True)
    provider_payload: Mapped[dict] = mapped_column(JSON)
    signature_ok: Mapped[bool] = mapped_column()
    status: Mapped[str] = mapped_column(String, index=True)
    order_id: Mapped[str] = mapped_column(String, index=True)
    paid_at: Mapped[str] = mapped_column(String, index=True)
    
    user: Mapped["User"] = relationship(back_populates="payments")


class Watchlist(Base):
    __tablename__ = "watchlist"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), index=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entries.entry_id"), index=True)
    created_at: Mapped[str] = mapped_column(String, index=True)
    
    user: Mapped["User"] = relationship(back_populates="watchlist_items")
    entry: Mapped["Entry"] = relationship(back_populates="watchlist_items")


class Event(Base):
    __tablename__ = "events"
    event_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), index=True)
    type: Mapped[str] = mapped_column(String, index=True)
    ts: Mapped[str] = mapped_column(String, index=True)
    session_id: Mapped[Optional[str]] = mapped_column(String, index=True)
    entry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("entries.entry_id"), index=True)
    amount: Mapped[Optional[float]] = mapped_column(Float)
    order_id: Mapped[Optional[str]] = mapped_column(String, index=True)
    latency_ms: Mapped[Optional[int]] = mapped_column(BigInteger)
    error_code: Mapped[Optional[str]] = mapped_column(String, index=True)
    version: Mapped[str] = mapped_column(String)
    event_metadata: Mapped[dict] = mapped_column(JSON) 
        
    user: Mapped["User"] = relationship(back_populates="events")
    entry: Mapped[Optional["Entry"]] = relationship(back_populates="events")


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), index=True)
    kind: Mapped[str] = mapped_column(String, index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String, index=True)
    fail_reason: Mapped[Optional[str]] = mapped_column(String)
    sent_at: Mapped[str] = mapped_column(String, index=True)
    
    user: Mapped["User"] = relationship(back_populates="notifications")


class Referral(Base, TimeStampMixin):
    __tablename__ = "referrals"
    ref_id: Mapped[int] = mapped_column(primary_key=True)
    inviter_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), index=True)
    invitee_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), index=True)
    rewarded_at: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String, index=True)
    
    inviter: Mapped["User"] = relationship(foreign_keys=[inviter_id])
    invitee: Mapped["User"] = relationship(foreign_keys=[invitee_id])