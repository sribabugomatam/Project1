# Chapter 8: How to Start, Stop, and Run the Application

This chapter explains how to run the project locally and how to stop it cleanly.

## 1. Start the backend

Open a terminal and navigate to the backend folder:

```bash
cd /Users/sribabu/Projects/Project1/backend
. venv/bin/activate
uvicorn main:app --reload
```

This starts the FastAPI server.

You should see a local URL such as:

```text
http://127.0.0.1:8000
```

The API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 2. Start the frontend

Open a second terminal and navigate to the frontend folder:

```bash
cd /Users/sribabu/Projects/Project1/frontend
npm install
npm run dev
```

Vite will provide a local URL such as:

```text
http://localhost:5173
```

## 3. Stop the servers

To stop the running servers:

- Press Ctrl+C in the terminal where the server is running.

## 4. Run tests

Backend tests:

```bash
cd /Users/sribabu/Projects/Project1/backend
. venv/bin/activate
python -m pytest -q
```

Frontend build check:

```bash
cd /Users/sribabu/Projects/Project1/frontend
npm run build
```

## 5. Useful tips

- Keep the backend and frontend running in separate terminals.
- If the backend is not running, the frontend may show a connection error.
- If the frontend cannot reach the backend, check that the API URL is correct.

## Summary

To run the fullstack app locally, you need:

1. The backend server running
2. The frontend dev server running
3. The browser open to the frontend URL

## Next chapter

Next, we will create a developer-friendly lesson plan and explain how to use this documentation for teaching others.
