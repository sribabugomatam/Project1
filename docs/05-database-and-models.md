# Chapter 5: Database Design and Models

The database is where the application stores its data. In this project, we use SQLite with SQLAlchemy models.

## Why a database is needed

A web application needs a place to store information such as:

- Flats
- Residents
- Parking spots
- HOA committee members
- Expenses and dues

Without a database, the app would lose all data when the server restarts.

## What is SQLite?

SQLite is a lightweight database engine that stores data in a file.

It is ideal for learning because:

- No separate database server is required
- Easy to start and stop
- Works well for small and medium applications

## Main entities in this project

The app contains these main entities:

- Flat
- Resident
- ParkingSpot
- HOACommittee
- HOAMember
- MonthlyDues
- Expense

## Example model: Flat

```python
class Flat(Base):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)
    flat_number = Column(String, unique=True, nullable=False, index=True)
    floor_number = Column(Integer, nullable=False)
    status = Column(String, default="Owner Occupied")
```

This means:

- Each flat has a unique flat number
- Every flat has a floor number
- Each flat has a status

## Example model: Resident

```python
class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True, index=True)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
```

This shows that a resident belongs to a flat through the flat_id foreign key.

## Relationship modeling

A key concept in database design is relationships.

### One-to-many relationship

A flat can have many residents.

Example:

```python
class Flat(Base):
    residents = relationship("Resident", back_populates="flat")
```

### Many-to-many relationship

A committee can have many members, and a resident can be a member of many committees.

In this project, this is modeled using a separate HOAMember table.

## Why foreign keys matter

A foreign key links a row in one table to a row in another table.

Example:

```python
flat_id = Column(Integer, ForeignKey("flats.id"), nullable=False)
```

This ensures that each resident points to an existing flat.

## Seed data

The app includes a seed script that populates the database with example data.

You can inspect it in:

- backend/seed.py

## Database file

The SQLite database file is stored here:

- backend/apartment_hoa.db

## Summary

The database layer stores the app data and enforces relationships between records. Understanding models and relationships is essential for building scalable applications.

## Next chapter

Next, we will learn how to test the API and verify that CRUD operations work correctly.
