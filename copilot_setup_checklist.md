# Beginner Setup Checklist for the Apartment HOA App

This checklist helps you install the tools, create the project structure, and build and test the app locally on macOS using VS Code and GitHub Copilot Agent.

## 1. Install the required software

### 1.1 Install Xcode Command Line Tools
Open Terminal and run:

```bash
xcode-select --install
```

If prompted, confirm the install.

### 1.2 Install Homebrew
If Homebrew is not already installed, run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

If Homebrew asks you to add it to your PATH, follow the instructions shown in the terminal.

### 1.3 Install Python, Node.js, and Git
Run:

```bash
brew install python git node
```

### 1.4 Install VS Code
Run:

```bash
brew install --cask visual-studio-code
```

## 2. Verify the installation
Run these commands in Terminal:

```bash
python3 --version
node --version
npm --version
git --version
```

You should see version numbers for each tool.

## 3. Open the project in VS Code
Open your project folder in VS Code.

Inside that folder, create two folders:

```bash
mkdir -p backend frontend
```

## 4. Install the required VS Code extensions
In VS Code, install:

- GitHub Copilot
- GitHub Copilot Chat
- Python
- Pylance

Optional but helpful:
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense

## 5. Open Copilot Chat in Agent mode
In VS Code:

1. Open the Copilot Chat panel.
2. Switch to Agent mode.
3. Use the prompts below one by one.

## 6. Create the backend
Open a terminal in VS Code and run:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic
```

### Copilot Agent prompt for the backend
Use this prompt in Agent mode:

```text
Create a full-stack apartment HOA management app backend in the backend folder using Python FastAPI and SQLAlchemy with SQLite. Create files named database.py, models.py, schemas.py, seed.py, and main.py. Include SQLAlchemy models for flats, residents, parking spots, HOA committees, HOA members, monthly dues, and expenses. Create a seed script that creates 20 flats from 101 to 504, default parking spots, and sample residents. Make sure foreign keys work correctly and include basic CRUD-style API routes.
```

## 7. Create the frontend
Open a new terminal tab and run:

```bash
cd frontend
npm create vite@latest . -- --template react
npm install
npm install axios lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

If Vite asks whether to overwrite files, choose yes only if you are sure the folder is empty.

### Copilot Agent prompt for the frontend
Use this prompt in Agent mode:

```text
Create a React + Vite + Tailwind CSS frontend in the frontend folder. Build a modern dashboard shell with a sidebar, top bar, and pages for Dashboard, Building Directory, Parking, HOA Committee, Dues, and Expenses. Connect it to the backend at http://localhost:8000/api. Use axios or fetch and make the UI responsive.
```

## 8. Run the backend locally
In the backend terminal, run:

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

Then open:

```text
http://localhost:8000/docs
```

You should see the FastAPI Swagger documentation.

## 9. Run the frontend locally
In a second terminal tab, run:

```bash
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

## 10. Test the app locally
Check the following:

- The frontend opens in the browser.
- The backend docs open at http://localhost:8000/docs.
- The dashboard loads.
- Flats and residents appear.
- You can add or update residents.
- Parking data appears.
- Expenses and dues can be added.

## 11. If something breaks
Use Copilot Agent with prompts like:

```text
I am getting an error while running the FastAPI backend. Please inspect the code, explain the issue, and suggest a fix.
```

Or:

```text
The frontend is failing to load data from the backend. Please inspect the API integration and fix the issue.
```

## 12. Recommended order
Follow this order:

1. Set up the backend.
2. Seed the database.
3. Verify the API works.
4. Build the frontend UI.
5. Connect the UI to the API.
6. Test the full app locally.

## 13. First milestone
A good first milestone is:

- Backend starts successfully
- Database is seeded
- Swagger docs open
- Frontend opens without errors
- One page can display flats from the backend

If you want, I can next help you with the first Copilot Agent prompt in a more detailed, copy-paste-ready form.