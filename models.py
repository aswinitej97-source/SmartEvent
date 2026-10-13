from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
)
from sqlalchemy.sql import func
from database import Base


# =========================================================
# USER
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="USER")
    created_at = Column(DateTime, server_default=func.now())


# =========================================================
# EVENT
# =========================================================

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    location = Column(String, nullable=False)
    event_date = Column(DateTime, nullable=False)
    ticket_price = Column(Float, nullable=False)
    banner_image = Column(String, nullable=True)

    organizer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )


# =========================================================
# COUPON
# =========================================================

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)

    coupon_code = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    discount_type = Column(String, nullable=False)
    discount_value = Column(Float, nullable=False)

    minimum_booking_amount = Column(
        Float,
        nullable=False,
        default=0,
    )

    expiry_date = Column(DateTime, nullable=False)
    usage_limit = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )


# =========================================================
# BOOKING
# =========================================================

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False,
    )

    ticket_quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    coupon_id = Column(
        Integer,
        ForeignKey("coupons.id"),
        nullable=True,
    )

    discount_amount = Column(
        Float,
        nullable=False,
        default=0,
    )

    final_amount = Column(
        Float,
        nullable=False,
        default=0,
    )

    booking_status = Column(
        String,
        default="PENDING",
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )


# =========================================================
# TICKET
# =========================================================

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False,
    )

    ticket_code = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )


# =========================================================
# PAYMENT
# =========================================================

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False,
    )

    payment_method = Column(String, nullable=False)

    payment_status = Column(
        String,
        nullable=False,
        default="PENDING",
    )

    transaction_id = Column(
        String,
        unique=True,
        nullable=True,
    )

    amount = Column(Float, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )


# =========================================================
# NOTIFICATION
# =========================================================

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    title = Column(
        String,
        nullable=False,
    )

    message = Column(
        Text,
        nullable=False,
    )

    type = Column(
        String,
        nullable=False,
    )

    is_read = Column(
        Boolean,
        default=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )


# =========================================================
# MODULE 14 - REVIEW & RATING
# =========================================================

class Review(Base):
    __tablename__ = "reviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False,
    )

    rating = Column(
        Integer,
        nullable=False,
    )

    comment = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )