# Chapter 4: Backend Layer - FastAPI, SQLAlchemy, and SQLite

The backend is the server-side logic of the app. It receives requests from the frontend, processes the data, talks to the database, and returns responses.

## What tools are used?

### FastAPI

FastAPI is a modern Python framework used to build APIs quickly.

It is known for:

- Fast development
- Automatic validation
- Easy routing
- Great documentation support

### SQLAlchemy

SQLAlchemy is a Python library for working with databases using Python objects.

It helps you define database tables as Python classes, which is easier to work with than writing raw SQL manually.

### SQLite

SQLite is a lightweight file-based database.

It is great for learning and small applications because it does not require a separate database server.

## Backend folder structure

The backend folder contains:

- main.py: API routes and app configuration
- models.py: SQLAlchemy database models
- schemas.py: request/response validation models
- database.py: database setup and session management
- seed.py: sample data seeding

## Important backend files

### backend/main.py

This is the heart of the API.

It contains:

- FastAPI app setup
- Route definitions
- CRUD operations
- Relationship-based endpoints

Example:

```python
@app.get("/api/flats", response_model=list[FlatRead])
def get_flats(db: Session = Depends(get_db)):
    return db.query(Flat).all()
```

This endpoint returns all flats.

### backend/models.py

This file defines the database entities.

Example:

```python
class Flat(Base):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)
    flat_number = Column(String, unique=True, nullable=False, index=True)
    floor_number = Column(Integer, nullable=False)
    status = Column(String, default="Owner Occupied")
```

This creates a table called flats with columns such as id, flat_number, floor_number, and status.

### backend/schemas.py

Schemas define the shape of the input and output data.

Example:

```python
class FlatCreate(BaseModel):
    flat_number: str
    floor_number: int
    status: str = "Owner Occupied"
```

This tells FastAPI what a valid flat creation request should look like.

### backend/database.py

This file sets up the database engine and session.

Example:

```python
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

This connects the app to the SQLite database.

## Relationship between models

A major part of the app is modeling relationships between data.

For example:

- A Flat can have many Residents
- A Flat can have many Parking spots
- A Resident can be part of one or more HOA committees

In SQLAlchemy, these relationships are defined with code such as:

```python
class Flat(Base):
    residents = relationship("Resident", back_populates="flat")
    parking_spots = relationship("ParkingSpot", back_populates="flat")
```

## CRUD pattern

The backend uses the typical CRUD pattern:

- Create: POST
- Read: GET
- Update: PUT
- Delete: DELETE

Example:

```python
@app.post("/api/flats", response_model=FlatDetailRead, status_code=status.HTTP_201_CREATED)
def create_flat(payload: FlatCreate, db: Session = Depends(get_db)):
    flat = Flat(**payload.model_dump())
    db.add(flat)
    db.commit()
    db.refresh(flat)
    return flat
```

## Starting the backend server

From the backend folder, run:

```bash
cd backend
. venv/bin/activate
uvicorn main:app --reload
```

This starts the FastAPI development server.

## Summary

The backend layer is responsible for:

- Exposing API endpoints
- Validating requests
- Working with the database
- Returning JSON responses

In the next chapter, we will look at the database and how data is modeled.
