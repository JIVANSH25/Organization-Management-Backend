# Organization Management Backend (FastAPI + MongoDB)

A scalable, multi-tenant backend service built using **FastAPI**, **MongoDB**, and **JWT authentication**.
This project is designed as part of the *Backend Intern Assignment – Organization Management Service*.

---

## 🚀 Overview

This service enables:

* Creation and management of organizations (multi-tenant structure)
* Dynamic collection/database creation per organization
* Secure admin authentication via JWT
* CRUD operations on organization metadata
* Automatic syncing of collections on organization rename

---

## 🏗️ Architecture Summary

The system uses:

* **Master Database** → Stores global metadata
  (organizations, admin users, mapping to per-org collections)
* **Dynamic Collections** → Each organization receives its own MongoDB DB namespace
  (`org_<org_name>` pattern)
* **JWT-based authentication** for admin operations

---

## 📁 Project Structure

```
org-management-backend/
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
├─ .env
├─ requirements.txt
└─ README.md
```

---

## ⚙️ Tech Stack

* FastAPI
* MongoDB (Motor async driver)
* JWT Authentication
* bcrypt for hashing
* Pydantic v2

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
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```
MONGO_URI=<your-mongo-uri>
MASTER_DB=master_db
JWT_SECRET=supersecretreplace
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5️⃣ Run the Server

```bash
uvicorn app.main:app --reload
```

API URL:
[http://localhost:8000](http://localhost:8000)

Swagger Docs:
[http://localhost:8000/docs](http://localhost:8000/docs)

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

1. Admin created with organization
2. Admin logs in → gets JWT containing:

   * admin_id
   * org
3. Protected endpoints require Bearer token
4. Token verified on each request

---

## 🧱 Design Choices

### ✔ Multi-Tenant Structure

* Each organization gets its own DB namespace
* Prevents cross-organization data mixing

### ✔ Async MongoDB (Motor)

* High concurrency
* Non-blocking operations

### ✔ JWT for Stateless Auth

* Lightweight
* Ideal for microservices

---

## ⚖️ Trade-Offs & Considerations

### Pros

* Clear isolation between organizations
* Scales horizontally
* Simple, maintainable architecture

### Trade-Offs

* Too many DB namespaces may impact Mongo performance
* Renaming org requires database migration
* Backup strategy is more complex

### Potential Improvements

* Use single DB with "org_id" to reduce DB overhead
* Add message queues for rename migrations
* Implement RBAC
* Add audit logs, rate limiting, caching

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

JIVANSH ANAND
Backend Developer
GitHub: [your-username](https://github.com/JIVANSH25)

---


