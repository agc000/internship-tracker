from fastapi import FastAPI

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.protected import router as protected_router
from app.api.v1.endpoints.applications import router as applications_router

app = FastAPI(title="Internship Tracker")

app.include_router(health_router)
app.include_router(protected_router)
app.include_router(applications_router)




