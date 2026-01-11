from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.protected import router as protected_router


app = FastAPI(title=settings.app_name)

app.include_router(health_router)
app.include_router(protected_router)


