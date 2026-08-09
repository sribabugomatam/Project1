from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Flat(Base):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)
    flat_number = Column(String, unique=True, nullable=False, index=True)
    floor_number = Column(Integer, nullable=False)
    status = Column(String, default="Owner Occupied")

    residents = relationship("Resident", back_populates="flat", cascade="all, delete-orphan")
    parking_spots = relationship("ParkingSpot", back_populates="flat")
    monthly_dues = relationship("MonthlyDues", back_populates="flat", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="flat")


class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True, index=True)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_primary_contact = Column(Boolean, default=True)

    flat = relationship("Flat", back_populates="residents")
    created_expenses = relationship("Expense", back_populates="creator")
    hoa_members = relationship("HOAMember", back_populates="resident")


class ParkingSpot(Base):
    __tablename__ = "parking_spots"

    id = Column(Integer, primary_key=True, index=True)
    spot_number = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    assigned_flat_id = Column(Integer, ForeignKey("flats.id"), nullable=True)
    spot_type = Column(String, nullable=False, default="Default")

    flat = relationship("Flat", back_populates="parking_spots")


class HOACommittee(Base):
    __tablename__ = "hoa_committees"

    id = Column(Integer, primary_key=True, index=True)
    term_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    members = relationship("HOAMember", back_populates="committee", cascade="all, delete-orphan")


class HOAMember(Base):
    __tablename__ = "hoa_members"

    id = Column(Integer, primary_key=True, index=True)
    committee_id = Column(Integer, ForeignKey("hoa_committees.id"), nullable=False)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    role = Column(String, nullable=False)

    committee = relationship("HOACommittee", back_populates="members")
    resident = relationship("Resident", back_populates="hoa_members")


class MonthlyDues(Base):
    __tablename__ = "monthly_dues"

    id = Column(Integer, primary_key=True, index=True)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=False)
    month_year = Column(String, nullable=False)
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    status = Column(String, default="Pending")
    paid_date = Column(Date, nullable=True)
    payment_mode = Column(String, nullable=True)

    flat = relationship("Flat", back_populates="monthly_dues")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    expense_date = Column(Date, nullable=False)
    month_year = Column(String, nullable=False)
    receipt_notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("residents.id"), nullable=True)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=True)

    creator = relationship("Resident", back_populates="created_expenses")
    flat = relationship("Flat", back_populates="expenses")
