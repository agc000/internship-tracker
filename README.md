# Internship Application Tracker API

This is a backend only REST API for tracking internship applications. 
Designed using FastAPI, PostgreSQL and SQLModel. Supports CRUD operations with filtering, pagination and sorting.

Designed as a production ready backend service consumed by SwaggerUI, cmd-line tools, and future frontend. 

--- 
## Tech Stack
- **FastAPI** - API Framework
- **SQLMODEL / SQLAlchemy** - Object-Relational-Mapping and DB access
- **PostgreSQL** - persistent storage (local via Docker, cloud-ready)
- **Alembic** - DB migrations
- **Pydantic** — request/response validation
- **Docker** — local database environment
- **Uvicorn** — ASGI server
- **Railway** - Cloud Deployment with API + Postgres
 ---

## Features

- API-key authenticated endpoints
- Create, read, update, and delete internship applications
- Filter by company and status
- Pagination (`skip`, `limit`)
- Sorting with enum-based validation
- Automatic request validation and error handling
- Swagger UI for interactive testing
---
## Deployment 
This service utilizes Railway deployment managed with a PostgreSQL database
Live Url: https://web-production-d9381.up.railway.app/docs



---
## Running the Project Local
### 1. Start PostgreSQL (Docker)
```bash
docker start internship-tracker-db
```
### 2. Start the API server
``` bash
uvicorn app.main:app --reload
```
### 3. Open the Swagger UI, Navigate to: 
```bash
http://localhost:8000/docs
```
