import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import app
from database import Base, engine, SessionLocal
from models import Expense, Flat, HOACommittee, HOAMember, MonthlyDues, ParkingSpot, Resident


@pytest.fixture(scope="function")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


def test_nested_flat_creation_with_related_resources(client):
    response = client.post(
        "/api/flats",
        json={
            "flat_number": "777",
            "floor_number": 7,
            "status": "Owner Occupied",
            "residents": [{"full_name": "Bob Carter", "role": "Owner", "phone": "555", "email": "bob@example.com"}],
            "parking_spots": [{"spot_number": "P77", "location": "Garage", "spot_type": "Default"}],
        },
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["flat_number"] == "777"
    assert len(payload["residents"]) == 1
    assert payload["residents"][0]["full_name"] == "Bob Carter"
    assert len(payload["parking_spots"]) == 1
    assert payload["parking_spots"][0]["spot_number"] == "P77"


def test_full_crud_and_relationships(client):
    # Flats
    flat_response = client.post(
        "/api/flats",
        json={"flat_number": "999", "floor_number": 9, "status": "Owner Occupied"},
    )
    assert flat_response.status_code == 201
    flat_id = flat_response.json()["id"]

    # Residents
    resident_response = client.post(
        "/api/residents",
        json={"flat_id": flat_id, "full_name": "Alice Johnson", "role": "Owner", "phone": "123", "email": "alice@example.com"},
    )
    assert resident_response.status_code == 201
    resident_id = resident_response.json()["id"]

    # Parking spots
    parking_response = client.post(
        "/api/parking",
        json={"spot_number": "P1", "location": "Garage", "assigned_flat_id": flat_id, "spot_type": "Default"},
    )
    assert parking_response.status_code == 201
    spot_id = parking_response.json()["id"]

    # Dues
    dues_response = client.post(
        "/api/dues",
        json={"flat_id": flat_id, "month_year": "2026-08", "amount_due": 150.0, "amount_paid": 0.0, "status": "Pending"},
    )
    assert dues_response.status_code == 201
    dues_id = dues_response.json()["id"]

    # Expense
    expense_response = client.post(
        "/api/expenses",
        json={"title": "Maintenance", "category": "Repair", "amount": 50.0, "expense_date": "2026-08-01", "month_year": "2026-08", "created_by": resident_id, "flat_id": flat_id},
    )
    assert expense_response.status_code == 201
    expense_id = expense_response.json()["id"]

    # Committee and HOAMember
    committee_response = client.post(
        "/api/committee",
        json={"term_name": "2026", "start_date": "2026-01-01", "end_date": "2026-12-31", "is_active": True, "members": [{"resident_id": resident_id, "role": "Chair"}]},
    )
    assert committee_response.status_code == 201
    committee_id = committee_response.json()["id"]

    # Relationship endpoints
    flat_detail = client.get(f"/api/flats/{flat_id}")
    assert flat_detail.status_code == 200
    assert len(flat_detail.json()["residents"]) == 1
    assert len(flat_detail.json()["parking_spots"]) == 1

    residents_for_flat = client.get(f"/api/flats/{flat_id}/residents")
    assert residents_for_flat.status_code == 200
    assert residents_for_flat.json()[0]["id"] == resident_id

    parking_for_flat = client.get(f"/api/flats/{flat_id}/parking")
    assert parking_for_flat.status_code == 200
    assert parking_for_flat.json()[0]["id"] == spot_id

    resident_detail = client.get(f"/api/residents/{resident_id}/flat")
    assert resident_detail.status_code == 200
    assert resident_detail.json()["id"] == flat_id

    resident_hoa = client.get(f"/api/residents/{resident_id}/hoa-members")
    assert resident_hoa.status_code == 200
    assert resident_hoa.json()[0]["committee_id"] == committee_id

    committee_members = client.get(f"/api/committee/{committee_id}/members")
    assert committee_members.status_code == 200
    assert committee_members.json()[0]["resident_id"] == resident_id

    # CRUD retrieve all
    assert client.get("/api/flats").status_code == 200
    assert client.get("/api/residents").status_code == 200
    assert client.get("/api/parking").status_code == 200
    assert client.get("/api/dues").status_code == 200
    assert client.get("/api/expenses").status_code == 200
    assert client.get("/api/committee/current").status_code == 200

    # Update and delete checks
    updated_flat = client.put(f"/api/flats/{flat_id}", json={"status": "Rented"})
    assert updated_flat.status_code == 200
    assert updated_flat.json()["status"] == "Rented"

    updated_resident = client.put(f"/api/residents/{resident_id}", json={"role": "Tenant"})
    assert updated_resident.status_code == 200
    assert updated_resident.json()["role"] == "Tenant"

    updated_dues = client.put(f"/api/dues/{dues_id}", json={"status": "Paid"})
    assert updated_dues.status_code == 200
    assert updated_dues.json()["status"] == "Paid"

    updated_expense = client.put(f"/api/expenses/{expense_id}", json={"amount": 75.0})
    assert updated_expense.status_code == 200
    assert updated_expense.json()["amount"] == 75.0

    delete_dues = client.delete(f"/api/dues/{dues_id}")
    assert delete_dues.status_code == 200

    delete_expense = client.delete(f"/api/expenses/{expense_id}")
    assert delete_expense.status_code == 200

    delete_resident = client.delete(f"/api/residents/{resident_id}")
    assert delete_resident.status_code == 200

    delete_flat = client.delete(f"/api/flats/{flat_id}")
    assert delete_flat.status_code == 200

    delete_parking = client.delete(f"/api/parking/{spot_id}")
    assert delete_parking.status_code == 200
