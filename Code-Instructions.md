# Code Instructions for Continuing Development

## Project Goal
This project is an Apartment HOA management application with:
- a FastAPI backend
- a SQLAlchemy + SQLite database layer
- a React + Vite + Tailwind frontend

The current implementation already includes CRUD APIs for flats, residents, parking spots, monthly dues, expenses, and HOA committees, plus relationship-based endpoints.

---

## Current Status
The codebase already has:
- [x] Backend API with CRUD operations
- [x] Relationship endpoints for related resources
- [x] Frontend UI for main entities
- [x] Basic backend tests for CRUD and relationships
- [x] Chapter-wise project documentation

---

## Architecture Overview

### Backend
Main backend files:
- [backend/main.py](backend/main.py) — FastAPI app, routes, request handling, CRUD logic
- [backend/models.py](backend/models.py) — SQLAlchemy ORM models
- [backend/schemas.py](backend/schemas.py) — Pydantic request/response schemas
- [backend/database.py](backend/database.py) — database engine and session setup
- [backend/seed.py](backend/seed.py) — initial seed data
- [backend/tests/test_api_crud.py](backend/tests/test_api_crud.py) — regression tests

### Frontend
Main frontend files:
- [frontend/src/App.jsx](frontend/src/App.jsx) — main React UI and API calls
- [frontend/package.json](frontend/package.json) — frontend scripts and dependencies

---

## How to Run the Project

### Backend
```bash
cd backend
. venv/bin/activate
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

### Backend tests
```bash
cd backend
. venv/bin/activate
python -m pytest -q
```

### Frontend build check
```bash
cd frontend
npm run build
```

---

## Development Rules for Any New Change
When adding or changing a feature, follow this order:

1. Update the database model in [backend/models.py](backend/models.py)
2. Update API schemas in [backend/schemas.py](backend/schemas.py)
3. Update backend routes in [backend/main.py](backend/main.py)
4. Update the frontend form/list UI in [frontend/src/App.jsx](frontend/src/App.jsx)
5. Add or adjust tests in [backend/tests/test_api_crud.py](backend/tests/test_api_crud.py)
6. Run tests and build verification before finishing

---

## Expected Pattern for Adding a New Field
For any new field such as age, phone, status, or notes:

### 1. Database layer
Add the field to the SQLAlchemy model in [backend/models.py](backend/models.py).

### 2. API layer
Add the field to the relevant Pydantic schema in [backend/schemas.py](backend/schemas.py).

### 3. Backend route logic
Make sure the route accepts the field and saves it through the ORM model.

### 4. Frontend layer
Add the field to the form state, payload, and display UI in [frontend/src/App.jsx](frontend/src/App.jsx).

### 5. Validation
Ensure the field is converted properly if it is a number or boolean.

---

## Important Implementation Notes
- The backend uses FastAPI and Pydantic, so request validation depends heavily on the schemas.
- The database is SQLite, so schema changes may require recreating the database file if the table already exists.
- Numeric form values in React should be converted before sending to the API.
- For relationship-based features, preserve existing patterns for nested create/update flows.
- Keep the API response shape consistent with the existing schemas.

---

## Current Backend Conventions
- Create endpoints return HTTP 201.
- Update endpoints return the updated resource.
- Delete endpoints return a JSON success response.
- Flat creation supports nested resident and parking data.
- Resident and parking updates validate referenced flat IDs.
- Delete operations clean up dependent records where needed.

---

## Testing Checklist
Before considering a change complete, verify:
- [ ] Backend tests pass
- [ ] Frontend build succeeds
- [ ] The changed feature works through the UI
- [ ] The changed feature works through the API
- [ ] Related endpoints still work correctly

---

## Common Gotchas
- If you add a new model field and the app still does not save it, the database schema may need to be recreated.
- If the API rejects a payload, check the Pydantic schema first.
- If the frontend does not show a value, check whether the API response actually contains it.
- If a relationship endpoint behaves unexpectedly, inspect the ORM relationship definitions in [backend/models.py](backend/models.py).

---

## Suggested Next Enhancements
Good next tasks for this project include:
- [ ] add better validation for duplicate flat numbers or parking spots
- [ ] add richer committee/member management UI
- [ ] improve resident search and filtering
- [ ] add authentication and role-based access
- [ ] improve error handling and user feedback in the frontend
- [ ] add pagination for larger lists

---

## Instructions for the Next AI Agent
- Keep the app structure intact and avoid replacing the current architecture with a different stack.
- Prefer small, incremental changes over large rewrites.
- Follow the existing patterns already established in the backend and frontend.
- Verify the result through tests and build checks before claiming completion.
- When adding new features, update documentation if the behavior changes for developers or users.
