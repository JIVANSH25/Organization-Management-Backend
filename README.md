# Organization Management Backend (FastAPI + MongoDB)

A scalable, multi-tenant backend service built using **FastAPI**, **MongoDB**, and **JWT authentication**.
This project is designed as part of the *Backend Intern Assignment – Organization Management Service*.

---

## 🚀 Overview

This service enables:

* Creation and management of organizations (multi-tenant structure)
* Dynamic collection/database creation per organization
* Secure admin authentication powered by JWT
* CRUD operations on organization metadata
* Automatic syncing of collections on organization rename

---

## 🏗️ Architecture Summary

The system uses:

* **Master Database** → Stores global metadata
  (organizations, admin users, mapping to per-org collections)
* **Dynamic Collections** → Each organization receives its own MongoDB DB namespace
  (`org_<organization_name>` pattern)
* **JWT Authentication** → Used for validating admin access

---

## 📁 Project Structure

```
org-management-backend/
├─ api/
│  └─ index.py
│
├─ app/
│  ├─ main.py
│  ├─ config.py
│  ├─ db.py
│  ├─ dependencies.py
│  ├─ auth.py
│  ├─ crud.py
│  ├─ models.py
│  ├─ __init__.py
│  ├─ routers/
│  │   ├─ org.py
│  │   ├─ admin.py
│  │   └─ __init__.py
│
├─ .env
├─ requirements.txt
├─ vercel.json
└─ README.md
```

---

## ⚙️ Tech Stack

* FastAPI
* MongoDB (Motor async driver)
* JWT Authentication
* bcrypt password hashing
* Pydantic v2 for validation
* Mangum ASGI adapter (for Vercel deployment)

---

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/org-management-backend.git
cd org-management-backend
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate       # Linux / Mac
venv\Scripts\activate          # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Inside `.env`:

```
MONGO_URI=<your-mongo-uri>
MASTER_DB=master_db
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5️⃣ Run the Server Locally

```bash
uvicorn app.main:app --reload
```

Local API URL:
[http://localhost:8000](http://localhost:8000)

Swagger Docs:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🚀 Deploying to Vercel (Serverless)

### ✔ Required Files for Vercel

#### `api/index.py`

```python
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

#### `vercel.json`

```json
{
  "version": 2,
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    { "src": "/(.*)", "dest": "api/index.py" }
  ]
}
```

#### Required Packages (ensure in requirements.txt)

```
fastapi
uvicorn
mangum
motor
pymongo
dnspython
bcrypt
python-jose
pydantic
python-dotenv
```

After pushing to GitHub → Deploy via Vercel dashboard.

---

## 📌 API Endpoints

### 1. Create Organization

`POST /org/create`

### 2. Get Organization by Name

`GET /org/get/{org_name}`

### 3. Update Organization Name (Authenticated)

`PUT /org/update`

### 4. Delete Organization (Authenticated)

`DELETE /org/delete`

### 5. Admin Login

`POST /admin/login`

---

## 🔐 Authentication Flow

1. Admin is created along with the organization
2. Admin logs in → Receives JWT containing:

   * `admin_id`
   * `org`
3. Bearer token required for update/delete actions
4. Token verified in all protected routes

---

## 🧱 Design Choices

### ✔ Multi-Tenant Architecture

* Each organization gets separate DB namespace
* Ensures complete data isolation

### ✔ Async MongoDB (Motor)

* High concurrency
* Non-blocking DB operations

### ✔ Stateless JWT Authentication

* No session storage needed
* Lightweight and scalable

---

## ⚖️ Trade-Offs & Considerations

### Pros

* Strong tenant isolation
* Easy to scale horizontally
* Clean, modular architecture

### Cons

* Too many DB namespaces can slow MongoDB
* Renaming org → requires DB migration
* Backups more complex

### Possible Enhancements

* Replace multi-DB with single-DB + org_id
* Add message queues for rename migration
* RBAC (role-based access control)
* Audit logs, caching, rate limiting

---

## 🗺️ High-Level Architecture Diagram

```
                ┌───────────────────────────┐
                │        Client App          │
                └─────────────┬─────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │     FastAPI      │
                     │  (REST Backend)  │
                     └─────────┬────────┘
                               │
       ┌───────────────────────┼────────────────────────┐
       ▼                       ▼                        ▼
┌────────────┐        ┌────────────────┐       ┌────────────────────┐
│ Auth Layer │        │  CRUD Layer    │       │ Dependency Layer   │
└────────────┘        └────────────────┘       └────────────────────┘
                               │
                               ▼
                    ┌───────────────────────┐
                    │     MongoDB Master     │
                    └───────────┬───────────┘
                                │
                 ┌──────────────┴───────────────┐
                 ▼                                ▼
    ┌────────────────────┐         ┌─────────────────────────┐
    │ org_company1 DB    │         │ org_schoolX DB          │
    └────────────────────┘         └─────────────────────────┘
```

---

## 👤 Author

**JIVANSH ANAND**
Backend Developer
GitHub: [https://github.com/JIVANSH25](https://github.com/JIVANSH25)

