# Chapter 3: Frontend Layer - React, Vite, and Tailwind

The frontend is the part of the application that the user sees and interacts with. In this project, the frontend is built using React and Vite.

## What tools are used?

### React

React is a JavaScript library for building user interfaces.

It helps you create reusable UI components such as forms, buttons, cards, and lists.

### Vite

Vite is a fast development tool for React projects.

It provides:

- Fast startup
- Fast hot reload during development
- Easy build for production

### Tailwind CSS

Tailwind CSS is a utility-first CSS framework.

Instead of writing large CSS files, you write small utility classes directly in JSX.

Example:

```jsx
<div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
  Hello
</div>
```

## Frontend folder structure

The frontend folder contains:

- src/: application source code
- index.html: main HTML entry
- package.json: frontend dependencies and scripts
- vite.config.js: Vite configuration
- tailwind.config.js: Tailwind setup

## Important frontend files

### frontend/src/main.jsx

This file mounts the React app to the browser.

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(<App />)
```

### frontend/src/App.jsx

This is the main UI file. It contains:

- Page navigation
- Forms for flats, residents, parking, and committees
- API calls to the backend
- State management

### Example: loading data from the backend

```jsx
const loadData = async () => {
  try {
    const [flatsRes, residentsRes, parkingRes] = await Promise.all([
      axios.get(`${API_BASE}/flats`),
      axios.get(`${API_BASE}/residents`),
      axios.get(`${API_BASE}/parking`),
    ])
    setFlats(flatsRes.data)
    setResidents(residentsRes.data)
    setParking(parkingRes.data)
  } catch (error) {
    setHealth('backend unavailable')
  }
}
```

This code calls the backend APIs and stores the returned data in React state.

## How the frontend communicates with the backend

The frontend uses Axios to make HTTP requests.

Example:

```jsx
await axios.post(`${API_BASE}/flats`, payload)
```

This sends data to the backend API to create a new flat.

## Why state matters

React uses state to track data such as:

- Current form values
- List of flats
- List of residents
- Message shown to the user

Example:

```jsx
const [flats, setFlats] = useState([])
```

## How forms work

A form in React usually has:

1. Input fields bound to state
2. Submit handler that collects the form data
3. A request sent to the backend
4. UI updated after success

Example:

```jsx
<form onSubmit={handleFlatSubmit}>
  <input value={flatForm.flat_number} />
</form>
```

## Running the frontend locally

From the frontend folder, run:

```bash
npm install
npm run dev
```

Then open the local address shown by Vite in your browser.

## Summary

The frontend layer is responsible for:

- Showing pages
- Collecting user input
- Calling backend APIs
- Updating the UI

In the next chapter, we will explore the backend layer in detail.
