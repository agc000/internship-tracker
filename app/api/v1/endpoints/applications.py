from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select

from app.core.security import verify_api_key
from app.db import get_session
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=Application, dependencies=[Depends(verify_api_key)])
def create_application(
    data: ApplicationCreate,
    session: Session = Depends(get_session),
):
    payload = data.model_dump()

    if payload.get("applied_date") is None:
        payload["applied_date"] = datetime.utcnow()

    application = Application(**payload)
    session.add(application)
    session.commit()
    session.refresh(application)
    return application


@router.get("", response_model=List[Application], dependencies=[Depends(verify_api_key)])
def list_applications(session: Session = Depends(get_session)):
    stmt = select(Application).order_by(Application.id.desc())
    result = session.execute(stmt)
    return result.scalars().all()


@router.get("/{id}", response_model=Application, dependencies=[Depends(verify_api_key)])
def get_application(id: int, session: Session = Depends(get_session)):
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.patch("/{id}", response_model=Application, dependencies=[Depends(verify_api_key)])
def update_application(
    id: int,
    data: ApplicationUpdate,
    session: Session = Depends(get_session),
):
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(application, key, value)

    session.add(application)
    session.commit()
    session.refresh(application)
    return application


@router.delete("/{id}", dependencies=[Depends(verify_api_key)])
def delete_application(id: int, session: Session = Depends(get_session)):
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    session.delete(application)
    session.commit()
    return {"ok": True}
