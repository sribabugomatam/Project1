from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
from models import Expense, Flat, HOACommittee, HOAMember, MonthlyDues, ParkingSpot, Resident
from schemas import (
    ExpenseCreate,
    ExpenseRead,
    ExpenseUpdate,
    FlatCreate,
    FlatDetailRead,
    FlatRead,
    FlatUpdate,
    HOACommitteeCreate,
    HOACommitteeRead,
    HOAMemberRead,
    MonthlyDuesCreate,
    MonthlyDuesRead,
    MonthlyDuesUpdate,
    ParkingSpotCreate,
    ParkingSpotRead,
    ParkingSpotUpdate,
    ResidentCreate,
    ResidentRead,
    ResidentUpdate,
)
from seed import seed_database

app = FastAPI(title="Apartment HOA Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        if db.query(Flat).count() == 0:
            seed_database(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/flats", response_model=list[FlatRead])
def get_flats(db: Session = Depends(get_db)):
    return db.query(Flat).all()


@app.get("/api/flats/{flat_id}/residents", response_model=list[ResidentRead])
def get_flat_residents(flat_id: int, db: Session = Depends(get_db)):
    flat = db.query(Flat).filter(Flat.id == flat_id).first()
    if not flat:
        raise HTTPException(status_code=404, detail="Flat not found")
    return flat.residents


@app.get("/api/flats/{flat_id}/parking", response_model=list[ParkingSpotRead])
def get_flat_parking(flat_id: int, db: Session = Depends(get_db)):
    flat = db.query(Flat).filter(Flat.id == flat_id).first()
    if not flat:
        raise HTTPException(status_code=404, detail="Flat not found")
    return flat.parking_spots


@app.post("/api/flats", response_model=FlatDetailRead, status_code=status.HTTP_201_CREATED)
def create_flat(payload: FlatCreate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude={"residents", "parking_spots"})
    flat = Flat(**data)
    db.add(flat)
    db.flush()

    for resident_payload in payload.residents or []:
        resident_data = resident_payload.model_dump(exclude_unset=True)
        resident_data["flat_id"] = flat.id
        resident = Resident(**resident_data)
        db.add(resident)

    for parking_payload in payload.parking_spots or []:
        parking_data = parking_payload.model_dump(exclude_unset=True)
        parking_data["assigned_flat_id"] = flat.id
        spot = ParkingSpot(**parking_data)
        db.add(spot)

    db.commit()
    db.refresh(flat)
    return flat


@app.get("/api/flats/{flat_id}", response_model=FlatDetailRead)
def get_flat_detail(flat_id: int, db: Session = Depends(get_db)):
    flat = db.query(Flat).filter(Flat.id == flat_id).first()
    if not flat:
        raise HTTPException(status_code=404, detail="Flat not found")
    return flat


@app.put("/api/flats/{flat_id}", response_model=FlatDetailRead)
def update_flat(flat_id: int, payload: FlatUpdate, db: Session = Depends(get_db)):
    flat = db.query(Flat).filter(Flat.id == flat_id).first()
    if not flat:
        raise HTTPException(status_code=404, detail="Flat not found")

    update_data = payload.model_dump(exclude={"residents", "parking_spots"}, exclude_unset=True)
    for key, value in update_data.items():
        setattr(flat, key, value)

    if payload.residents is not None:
        db.query(Resident).filter(Resident.flat_id == flat.id).delete(synchronize_session=False)
        for resident_payload in payload.residents:
            resident_data = resident_payload.model_dump(exclude_unset=True)
            resident_data["flat_id"] = flat.id
            db.add(Resident(**resident_data))

    if payload.parking_spots is not None:
        db.query(ParkingSpot).filter(ParkingSpot.assigned_flat_id == flat.id).delete(synchronize_session=False)
        for parking_payload in payload.parking_spots:
            parking_data = parking_payload.model_dump(exclude_unset=True)
            parking_data["assigned_flat_id"] = flat.id
            db.add(ParkingSpot(**parking_data))

    db.commit()
    db.refresh(flat)
    return flat


@app.delete("/api/flats/{flat_id}")
def delete_flat(flat_id: int, db: Session = Depends(get_db)):
    flat = db.query(Flat).filter(Flat.id == flat_id).first()
    if not flat:
        raise HTTPException(status_code=404, detail="Flat not found")

    for resident in list(flat.residents):
        db.query(HOAMember).filter(HOAMember.resident_id == resident.id).delete(synchronize_session=False)
        db.query(Expense).filter(Expense.created_by == resident.id).update({Expense.created_by: None}, synchronize_session=False)
        db.delete(resident)

    db.query(ParkingSpot).filter(ParkingSpot.assigned_flat_id == flat.id).update({ParkingSpot.assigned_flat_id: None}, synchronize_session=False)
    db.query(MonthlyDues).filter(MonthlyDues.flat_id == flat.id).delete(synchronize_session=False)
    db.query(Expense).filter(Expense.flat_id == flat.id).delete(synchronize_session=False)

    db.delete(flat)
    db.commit()
    return {"deleted": True}


@app.get("/api/residents", response_model=list[ResidentRead])
def get_residents(db: Session = Depends(get_db)):
    return db.query(Resident).all()


@app.get("/api/residents/{resident_id}/flat", response_model=FlatRead)
def get_resident_flat(resident_id: int, db: Session = Depends(get_db)):
    resident = db.query(Resident).filter(Resident.id == resident_id).first()
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    return resident.flat


@app.get("/api/residents/{resident_id}/hoa-members", response_model=list[HOAMemberRead])
def get_resident_hoa_members(resident_id: int, db: Session = Depends(get_db)):
    resident = db.query(Resident).filter(Resident.id == resident_id).first()
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    return resident.hoa_members


@app.post("/api/residents", response_model=ResidentRead, status_code=status.HTTP_201_CREATED)
def create_resident(payload: ResidentCreate, db: Session = Depends(get_db)):
    flat = db.query(Flat).filter(Flat.id == payload.flat_id).first()
    if not flat:
        raise HTTPException(status_code=404, detail="Flat not found")

    resident = Resident(**payload.model_dump())
    db.add(resident)
    db.commit()
    db.refresh(resident)
    return resident


@app.put("/api/residents/{resident_id}", response_model=ResidentRead)
def update_resident(resident_id: int, payload: ResidentUpdate, db: Session = Depends(get_db)):
    resident = db.query(Resident).filter(Resident.id == resident_id).first()
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")

    if payload.flat_id is not None:
        flat = db.query(Flat).filter(Flat.id == payload.flat_id).first()
        if not flat:
            raise HTTPException(status_code=404, detail="Flat not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(resident, key, value)

    db.commit()
    db.refresh(resident)
    return resident


@app.delete("/api/residents/{resident_id}")
def delete_resident(resident_id: int, db: Session = Depends(get_db)):
    resident = db.query(Resident).filter(Resident.id == resident_id).first()
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")

    db.query(HOAMember).filter(HOAMember.resident_id == resident.id).delete(synchronize_session=False)
    db.query(Expense).filter(Expense.created_by == resident.id).update({Expense.created_by: None}, synchronize_session=False)

    db.delete(resident)
    db.commit()
    return {"deleted": True}


@app.get("/api/parking", response_model=list[ParkingSpotRead])
def get_parking(db: Session = Depends(get_db)):
    return db.query(ParkingSpot).all()


@app.post("/api/parking", response_model=ParkingSpotRead, status_code=status.HTTP_201_CREATED)
def create_parking_spot(payload: ParkingSpotCreate, db: Session = Depends(get_db)):
    spot = ParkingSpot(**payload.model_dump())
    db.add(spot)
    db.commit()
    db.refresh(spot)
    return spot


@app.put("/api/parking/{spot_id}", response_model=ParkingSpotRead)
def update_parking_spot(spot_id: int, payload: ParkingSpotUpdate, db: Session = Depends(get_db)):
    spot = db.query(ParkingSpot).filter(ParkingSpot.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Parking spot not found")

    if payload.assigned_flat_id is not None:
        flat = db.query(Flat).filter(Flat.id == payload.assigned_flat_id).first()
        if not flat:
            raise HTTPException(status_code=404, detail="Flat not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(spot, key, value)

    db.commit()
    db.refresh(spot)
    return spot


@app.delete("/api/parking/{spot_id}")
def delete_parking_spot(spot_id: int, db: Session = Depends(get_db)):
    spot = db.query(ParkingSpot).filter(ParkingSpot.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Parking spot not found")
    db.delete(spot)
    db.commit()
    return {"deleted": True}


@app.get("/api/committee/current", response_model=list[HOACommitteeRead])
def get_active_committee(db: Session = Depends(get_db)):
    return db.query(HOACommittee).filter(HOACommittee.is_active.is_(True)).all()


@app.get("/api/committee/{committee_id}/members", response_model=list[HOAMemberRead])
def get_committee_members(committee_id: int, db: Session = Depends(get_db)):
    committee = db.query(HOACommittee).filter(HOACommittee.id == committee_id).first()
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    return committee.members


@app.post("/api/committee", response_model=HOACommitteeRead, status_code=status.HTTP_201_CREATED)
def create_committee(payload: HOACommitteeCreate, db: Session = Depends(get_db)):
    committee = HOACommittee(
        term_name=payload.term_name,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_active=payload.is_active,
    )
    db.add(committee)
    db.commit()
    db.refresh(committee)

    if payload.members:
        for member in payload.members:
            resident_id = member.get("resident_id")
            role = member.get("role")
            if resident_id is None or role is None:
                continue
            resident = db.query(Resident).filter(Resident.id == resident_id).first()
            if resident:
                db.add(HOAMember(committee_id=committee.id, resident_id=resident.id, role=role))

    db.commit()
    return committee


@app.get("/api/committee/menu", response_model=list[dict])
def get_committee_menu(db: Session = Depends(get_db)):
    residents = db.query(Resident).all()
    return [
        {
            "resident_id": resident.id,
            "full_name": resident.full_name,
            "flat_number": resident.flat.flat_number if resident.flat else None,
            "role": resident.role,
        }
        for resident in residents
    ]


@app.get("/api/dues", response_model=list[MonthlyDuesRead])
def get_dues(db: Session = Depends(get_db)):
    return db.query(MonthlyDues).all()


@app.post("/api/dues", response_model=MonthlyDuesRead, status_code=status.HTTP_201_CREATED)
def create_dues(payload: MonthlyDuesCreate, db: Session = Depends(get_db)):
    dues = MonthlyDues(**payload.model_dump())
    db.add(dues)
    db.commit()
    db.refresh(dues)
    return dues


@app.put("/api/dues/{dues_id}", response_model=MonthlyDuesRead)
def update_dues(dues_id: int, payload: MonthlyDuesUpdate, db: Session = Depends(get_db)):
    dues = db.query(MonthlyDues).filter(MonthlyDues.id == dues_id).first()
    if not dues:
        raise HTTPException(status_code=404, detail="Dues record not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(dues, key, value)

    db.commit()
    db.refresh(dues)
    return dues


@app.delete("/api/dues/{dues_id}")
def delete_dues(dues_id: int, db: Session = Depends(get_db)):
    dues = db.query(MonthlyDues).filter(MonthlyDues.id == dues_id).first()
    if not dues:
        raise HTTPException(status_code=404, detail="Dues record not found")
    db.delete(dues)
    db.commit()
    return {"deleted": True}


@app.get("/api/expenses", response_model=list[ExpenseRead])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()


@app.post("/api/expenses", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):
    expense = Expense(**payload.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@app.put("/api/expenses/{expense_id}", response_model=ExpenseRead)
def update_expense(expense_id: int, payload: ExpenseUpdate, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense


@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"deleted": True}
