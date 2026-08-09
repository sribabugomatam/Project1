# Comprehensive Development Plan: Apartment HOA & Building Maintenance Web App

This master plan provides a complete, step-by-step roadmap for building a web-based Apartment Maintenance & HOA Management System. Designed specifically for AI-assisted development ("vibecoding") in VS Code (using tools like Cursor, GitHub Copilot, or Windsurf), this document covers system architecture, database schema, API specifications, UI layout, and phased execution prompts.

---

## 1. Project Overview & Requirements

### 1.1 Property Layout & Domain Logic
* **Building Structure:** 5 floors, 4 flats per floor (20 flats total, e.g., 101–104, 201–204, ..., 501–504).
* **Occupancy & Residents:**
  * Primary Household: Head of Household, Spouse, Children.
  * Secondary / Extended: Relatives, temporary residents, tenants.
* **Parking Management:**
  * Default: 1 dedicated parking spot per flat in Ground Floor or Underground Cellar.
  * Extra Parking: Flat owners can purchase or rent additional available spots.
* **HOA Committee:**
  * 5 Key Roles: President, General Secretary, Treasurer, Executive Committee Member 1, Executive Committee Member 2.
  * Term: 2 years per committee setup.
* **Financial Management:**
  * **Income:** Fixed monthly maintenance fee collected per flat + extra parking fees + penalties/late fees.
  * **Recurring Monthly Expenses:** Watchman salary, Common Area Electricity, Water Bill (combined building bill), Garbage collection.
  * **Ad-hoc / Repair Expenses:** Shared area repairs, elevator servicing, plumbing, painting, emergency funds.

---

## 2. Tech Stack & Architecture

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | React (Vite) + Tailwind CSS + Lucide Icons | Fast, modern UI with easy utility styling and minimal boilerplate. |
| **Backend API** | Python (FastAPI) + Uvicorn | Blazing fast, auto-generates Swagger/OpenAPI docs, clean Python syntax. |
| **Database** | SQLite + SQLAlchemy ORM | Zero-config, single-file database ideal for local hosting and easy backups. |
| **Data Validation**| Pydantic v2 | Ensures strictly typed JSON requests and responses between React and FastAPI. |

### System Data Flow
```
[ React Single Page App ]  <--->  [ FastAPI REST API ]  <--->  [ SQLAlchemy ORM ]  <--->  [ SQLite Database ]
  (Port 5173 / Vite)                (Port 8000)                                       (apartment_hoa.db)
```

---

## 3. Database Schema Design (SQLite)

### ER Diagram & Tables Summary

#### 1. `flats`
* `id` (INTEGER, PK)
* `flat_number` (TEXT, Unique, e.g., "101")
* `floor_number` (INTEGER, 1 to 5)
* `status` (TEXT, Enum: 'Owner Occupied', 'Rented', 'Vacant')

#### 2. `residents`
* `id` (INTEGER, PK)
* `flat_id` (INTEGER, FK -> flats.id)
* `full_name` (TEXT)
* `role` (TEXT, Enum: 'Head of Household', 'Spouse', 'Child', 'Extended Family', 'Tenant')
* `phone` (TEXT)
* `email` (TEXT)
* `is_primary_contact` (BOOLEAN)

#### 3. `parking_spots`
* `id` (INTEGER, PK)
* `spot_number` (TEXT, Unique, e.g., "G-01", "C-05")
* `location` (TEXT, Enum: 'Ground Floor', 'Underground Cellar')
* `assigned_flat_id` (INTEGER, FK -> flats.id, Nullable)
* `spot_type` (TEXT, Enum: 'Default', 'Purchased Extra')

#### 4. `hoa_committees`
* `id` (INTEGER, PK)
* `term_name` (TEXT, e.g., "2026-2028 Term")
* `start_date` (DATE)
* `end_date` (DATE)
* `is_active` (BOOLEAN)

#### 5. `hoa_members`
* `id` (INTEGER, PK)
* `committee_id` (INTEGER, FK -> hoa_committees.id)
* `resident_id` (INTEGER, FK -> residents.id)
* `role` (TEXT, Enum: 'President', 'General Secretary', 'Treasurer', 'Exec Member 1', 'Exec Member 2')

#### 6. `monthly_dues`
* `id` (INTEGER, PK)
* `flat_id` (INTEGER, FK -> flats.id)
* `month_year` (TEXT, Format: 'YYYY-MM', e.g., '2026-04')
* `amount_due` (REAL)
* `amount_paid` (REAL, Default: 0)
* `status` (TEXT, Enum: 'Paid', 'Pending', 'Overdue', 'Partial')
* `paid_date` (DATE, Nullable)
* `payment_mode` (TEXT, Enum: 'UPI', 'Bank Transfer', 'Cash', 'Cheque')

#### 7. `expenses`
* `id` (INTEGER, PK)
* `title` (TEXT)
* `category` (TEXT, Enum: 'Watchman Salary', 'Common Electricity', 'Water Bill', 'Garbage Collection', 'Repairs & Maintenance', 'Other')
* `amount` (REAL)
* `expense_date` (DATE)
* `month_year` (TEXT, Format: 'YYYY-MM')
* `receipt_notes` (TEXT, Nullable)
* `created_by` (INTEGER, FK -> residents.id)

---

## 4. REST API Endpoint Specifications

### Flats & Residents
* `GET /api/flats` - List all 20 flats with floor details and primary resident info.
* `GET /api/flats/{id}` - Detailed flat details (residents, parking spots, due payment history).
* `POST /api/residents` - Add resident to a flat.
* `PUT /api/residents/{id}` - Update resident details.
* `DELETE /api/residents/{id}` - Remove resident.

### Parking Spots
* `GET /api/parking` - View map of ground & cellar parking spots and flat allocations.
* `POST /api/parking/assign` - Assign or reallocate extra parking spots to a flat.

### HOA Committee
* `GET /api/committee/current` - Get active 5-member committee.
* `POST /api/committee` - Create a new 2-year term committee with members.

### Financials & Maintenance Dues
* `GET /api/dues?month_year=2026-04` - Collection status for all 20 flats for a given month.
* `POST /api/dues/collect` - Record maintenance payment for a flat.
* `GET /api/expenses?month_year=2026-04` - List expenses for a given month.
* `POST /api/expenses` - Log new recurring or ad-hoc expense.
* `GET /api/reports/dashboard-summary` - Total dues collected vs total expenses, net balance, top pending flats.

---

## 5. UI Layout & Component Design

### Pages Breakdown
1. **Dashboard:** High-level metrics (Total Balance, Current Month Collection %, Total Expenses, Quick Dues Payment Widget, Recent Expense Log).
2. **Building & Flats Directory:** Interactive grid of 5 floors × 4 flats. Clicking a flat opens a modal showing household members and assigned parking.
3. **Parking Management:** Visual layout of Ground Floor and Underground Cellar spots, highlighting default vs purchased extra spots.
4. **HOA Committee Page:** Current term committee profiles, past committee archives, term dates countdown.
5. **Dues & Collection Tracker:** Table view for 20 flats with filterable status (Paid / Pending / Overdue) and quick "Mark as Paid" action.
6. **Expense Register:** Categorized expense logger with charts (Water, Electricity, Salary, Shared Repairs).

---

## 6. Vibecoding Phased Execution Plan

Use the following step-by-step prompts sequentially with your AI coding assistant in VS Code.

---

### Phase 1: Project Setup & Database Models
**Prompt to run:**
> "I want to set up a full-stack web application for apartment HOA management using Python FastAPI for backend and SQLite with SQLAlchemy ORM.
> Please generate the project directory structure with a backend/ folder containing:
> 1. `database.py` (SQLite connection setup)
> 2. `models.py` (SQLAlchemy models for Flats, Residents, ParkingSpots, HOACommittees, HOAMembers, MonthlyDues, Expenses based on the schema design)
> 3. `schemas.py` (Pydantic models for data validation)
> 4. `seed.py` (Script to automatically seed 5 floors with 4 flats each [101-104 to 501-504], default parking spots, and sample resident data)
> Make sure all code follows clean practices and handles SQLite foreign keys properly."

---

### Phase 2: Core FastAPI REST Endpoints
**Prompt to run:**
> "Now let me build the REST API endpoints in `main.py` using FastAPI.
> Create endpoints for:
> 1. Getting flat directory with resident list and assigned parking.
> 2. Adding/editing/deleting residents for a flat.
> 3. Assigning primary and additional parking spots.
> 4. Setting up a 5-member HOA committee term.
> 5. Monthly dues creation, tracking, and payment logging for each flat.
> 6. Logging monthly recurring (watchman, electricity, water, garbage) and repair expenses.
> Include CORS middleware enabled for localhost frontend access and auto-generate OpenAPI documentation."

---

### Phase 3: React Frontend Scaffold & Layout
**Prompt to run:**
> "Set up a Vite + React + Tailwind CSS project in a `frontend/` directory.
> Create a clean dashboard shell with:
> 1. Sidebar navigation (Dashboard, Building Directory, Parking Grid, HOA Committee, Dues Collection, Expense Log).
> 2. Top header bar displaying active HOA Committee President and Treasurer name.
> 3. Axios or Fetch helper set up to talk to `http://localhost:8000/api`.
> Use modern design principles, clean cards, muted slate/navy colors, and responsive layouts."

---

### Phase 4: Building Directory & Resident Management UI
**Prompt to run:**
> "Build the Building Directory component:
> 1. Visual representation of 5 floors with 4 flat cards per floor.
> 2. Color code flat cards by occupancy status (Owner, Rented, Vacant).
> 3. Clicking a flat card opens a detailed modal showing: Head of household, spouse, children, extended family, and assigned parking spots.
> 4. Add forms to add new family members or transfer ownership."

---

### Phase 5: Dues & Expense Financial Tracker UI
**Prompt to run:**
> "Build the Financial Management tab:
> 1. **Dues Tracker:** A table listing all 20 flats for the selected month/year. Show payment status (Paid / Pending / Overdue), amount paid, payment mode, and a button to open a 'Collect Payment' modal.
> 2. **Expense Register:** A list of expenses categorized by Watchman Salary, Common Area Electricity, Water Bill, Garbage, and Repairs. Include a modal to add new expense entry with date and notes.
> 3. **Summary KPI Cards:** Total Collections, Total Expenses, Net Cash Flow, and Deficit/Surplus badge."

---

### Phase 6: Parking & HOA Committee Pages
**Prompt to run:**
> "Build the Parking and HOA Committee views:
> 1. **Parking:** Tabbed view for Ground Floor and Underground Cellar displaying grid of parking spots. Indicate flat owner and highlight extra spots bought.
> 2. **HOA Committee:** Profile cards for the 5 roles (President, General Secretary, Treasurer, Exec Member 1, Exec Member 2) with term start/end dates and contact details."

---

## 7. Quickstart Guide (Local Development Setup)

### 1. Backend Setup (FastAPI + SQLite)
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scriptsctivate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic

# Seed database
python seed.py

# Run backend server
uvicorn main:app --reload --port 8000
```
*API Documentation available at:* `http://localhost:8000/docs`

### 2. Frontend Setup (React + Vite + Tailwind)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
npm install lucide-react axios

# Start development server
npm run dev
```
*Frontend Application available at:* `http://localhost:5173`

---
*Created for AI-Assisted Vibecoding in VS Code.*