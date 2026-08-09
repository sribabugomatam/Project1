from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ResidentBase(BaseModel):
    full_name: str
    role: str
    phone: Optional[str] = None
    email: Optional[str] = None
    is_primary_contact: bool = True


class ResidentCreate(ResidentBase):
    flat_id: Optional[int] = None


class ResidentUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_primary_contact: Optional[bool] = None
    flat_id: Optional[int] = None


class ResidentRead(ResidentBase):
    id: int
    flat_id: int

    model_config = ConfigDict(from_attributes=True)


class ParkingSpotBase(BaseModel):
    spot_number: str
    location: str
    assigned_flat_id: Optional[int] = None
    spot_type: str = "Default"


class ParkingSpotCreate(ParkingSpotBase):
    pass


class ParkingSpotUpdate(BaseModel):
    spot_number: Optional[str] = None
    location: Optional[str] = None
    assigned_flat_id: Optional[int] = None
    spot_type: Optional[str] = None


class ParkingSpotRead(ParkingSpotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FlatBase(BaseModel):
    flat_number: str
    floor_number: int
    status: str = "Owner Occupied"


class FlatCreate(FlatBase):
    residents: Optional[List[ResidentCreate]] = None
    parking_spots: Optional[List[ParkingSpotCreate]] = None


class FlatUpdate(BaseModel):
    flat_number: Optional[str] = None
    floor_number: Optional[int] = None
    status: Optional[str] = None
    residents: Optional[List[ResidentCreate]] = None
    parking_spots: Optional[List[ParkingSpotCreate]] = None


class FlatRead(FlatBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FlatDetailRead(FlatRead):
    residents: List[ResidentRead] = []
    parking_spots: List[ParkingSpotRead] = []

    model_config = ConfigDict(from_attributes=True)


class HOACommitteeBase(BaseModel):
    term_name: str
    start_date: date
    end_date: date
    is_active: bool = True


class HOACommitteeCreate(HOACommitteeBase):
    members: Optional[List[dict]] = None


class HOACommitteeRead(HOACommitteeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HOAMemberBase(BaseModel):
    committee_id: int
    resident_id: int
    role: str


class HOAMemberRead(HOAMemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MonthlyDuesBase(BaseModel):
    flat_id: int
    month_year: str
    amount_due: float
    amount_paid: float = 0.0
    status: str = "Pending"
    paid_date: Optional[date] = None
    payment_mode: Optional[str] = None


class MonthlyDuesCreate(MonthlyDuesBase):
    pass


class MonthlyDuesUpdate(BaseModel):
    flat_id: Optional[int] = None
    month_year: Optional[str] = None
    amount_due: Optional[float] = None
    amount_paid: Optional[float] = None
    status: Optional[str] = None
    paid_date: Optional[date] = None
    payment_mode: Optional[str] = None


class MonthlyDuesRead(MonthlyDuesBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ExpenseBase(BaseModel):
    title: str
    category: str
    amount: float
    expense_date: date
    month_year: str
    receipt_notes: Optional[str] = None
    created_by: Optional[int] = None
    flat_id: Optional[int] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    month_year: Optional[str] = None
    receipt_notes: Optional[str] = None
    created_by: Optional[int] = None
    flat_id: Optional[int] = None


class ExpenseRead(ExpenseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
