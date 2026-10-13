from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ================= USER =================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "USER"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# ================= EVENT =================

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    location: str
    event_date: datetime
    ticket_price: float = Field(ge=0)
    banner_image: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    event_date: Optional[datetime] = None
    ticket_price: Optional[float] = Field(default=None, ge=0)
    banner_image: Optional[str] = None


class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: str
    location: str
    event_date: datetime
    ticket_price: float
    banner_image: Optional[str] = None
    organizer_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ================= BOOKING =================

class BookingCreate(BaseModel):
    event_id: int
    ticket_quantity: int = Field(gt=0)


class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    ticket_quantity: int
    total_price: float

    coupon_id: Optional[int] = None
    discount_amount: float = 0
    final_amount: float = 0

    booking_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ================= PAYMENT =================

class PaymentCreate(BaseModel):
    booking_id: int
    payment_method: str


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    payment_method: str
    payment_status: str
    transaction_id: Optional[str] = None
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True


# ================= COUPON =================

class CouponCreate(BaseModel):
    coupon_code: str
    discount_type: str
    discount_value: float = Field(gt=0)
    minimum_booking_amount: float = Field(default=0, ge=0)
    expiry_date: datetime
    usage_limit: int = Field(gt=0)
    is_active: bool = True


class CouponResponse(BaseModel):
    id: int
    coupon_code: str
    discount_type: str
    discount_value: float
    minimum_booking_amount: float
    expiry_date: datetime
    usage_limit: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CouponApply(BaseModel):
    coupon_code: str


# ================= ROLE UPDATE =================

class UserRoleUpdate(BaseModel):
    role: str

    # =========================================================
# MODULE 14 - REVIEW & RATING
# =========================================================

class ReviewCreate(BaseModel):
    event_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
        # =========================================================
# MODULE 15 - ADVANCED NOTIFICATIONS
# =========================================================

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    type: str


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True