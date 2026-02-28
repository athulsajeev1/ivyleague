---
description: How to run IvyLeague Connect
---

### 1. Start the Database
Ensure Docker is running, then execute:
```powershell
docker-compose up -d
```

### 2. Setup and Run Backend
Navigate to the backend directory, install dependencies, and start the server:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Setup and Run Frontend (Requires Node.js)
Navigate to the frontend directory and start the dev server:
```powershell
cd ../frontend
npm install
npm run dev
```

> [!NOTE]
> Since Node.js environment was not detected in my shell, you may need to ensure it is installed on your system before running the frontend steps.
