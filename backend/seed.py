from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Flat, ParkingSpot


def seed_database(db: Session):
    if db.query(Flat).count() > 0:
        return

    Base.metadata.create_all(bind=engine)

    flats = []
    for floor_number in range(1, 6):
        for flat_index in range(1, 5):
            flat_number = f"{floor_number}{flat_index:02d}"
            flats.append(Flat(flat_number=flat_number, floor_number=floor_number, status="Owner Occupied"))

    db.add_all(flats)
    db.commit()

    default_spots = []
    extra_spots = []
    for flat in flats:
        default_spots.append(
            ParkingSpot(
                spot_number=flat.flat_number,
                location="Ground Floor",
                assigned_flat_id=flat.id,
                spot_type="Default",
            )
        )

    for index in range(1, 6):
        extra_spots.append(
            ParkingSpot(
                spot_number=f"GF-{index:02d}",
                location="Ground Floor",
                assigned_flat_id=None,
                spot_type="Purchased Extra",
            )
        )

    for index in range(1, 6):
        extra_spots.append(
            ParkingSpot(
                spot_number=f"C-{index:02d}",
                location="Underground Cellar",
                assigned_flat_id=None,
                spot_type="Purchased Extra",
            )
        )

    db.add_all(default_spots)
    db.add_all(extra_spots)
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
        print("Database seeded successfully.")
    finally:
        db.close()
