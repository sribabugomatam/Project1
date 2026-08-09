# Chapter 2: Application Architecture Overview

A fullstack web application is usually built from three main layers:

1. Frontend layer
2. Backend layer
3. Database layer

This project follows that structure.

## 1. Frontend layer

The frontend is the part users interact with in the browser. In this project, the frontend is built with:

- React
- Vite
- Tailwind CSS
- Axios

The frontend files are located in the frontend folder.

### Main frontend responsibilities

- Display pages and forms
- Send HTTP requests to the backend
- Show responses from the backend
- Manage local UI state

### Example from the project

The application entry file is:

- frontend/src/main.jsx
- frontend/src/App.jsx

A simple React component uses state and renders UI like this:

```jsx
const [flats, setFlats] = useState([])

useEffect(() => {
  loadData()
}, [])
```

This shows how the app keeps data in component state and loads it when the component starts.

## 2. Backend layer

The backend exposes APIs that the frontend calls. In this project, the backend uses:

- FastAPI
- SQLAlchemy
- SQLite

The backend files are in the backend folder.

### Main backend responsibilities

- Accept requests from the frontend
- Validate input
- Interact with the database
- Return structured JSON data

### Example from the project

A FastAPI route looks like this:

```python
@app.get("/api/flats", response_model=list[FlatRead])
def get_flats(db: Session = Depends(get_db)):
    return db.query(Flat).all()
```

This route returns all flats from the database when the frontend requests the /api/flats endpoint.

## 3. Database layer

The database stores the app data. In this project, SQLite is used for simplicity.

The main database file is:

- backend/apartment_hoa.db

The database is accessed through SQLAlchemy models.

## Data flow in the app

Here is the typical flow:

1. The user opens the frontend page.
2. The React app calls an API endpoint.
3. FastAPI receives the request.
4. The backend queries or updates the SQLite database.
5. The response is returned as JSON.
6. The frontend updates the UI.

## Architecture diagram

```text
Browser (React UI)
        |
        | HTTP requests
        v
FastAPI Backend
        |
        | SQLAlchemy ORM
        v
SQLite Database
```

## Summary

In this project, you will learn to connect:

- UI components in React
- API routes in FastAPI
- Database models in SQLAlchemy

That is the core pattern of a fullstack web application.

## Next chapter

In the next chapter, we will look at the frontend files and explain what each one does.
