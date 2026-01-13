from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlmodel import select

from app.core.security import verify_api_key
from app.db import get_session
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class ApplicationSortField(str, Enum):
    id = "id"
    applied_date = "applied_date"
    company = "company"
    status = "status"


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
def list_applications(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    sort_by: ApplicationSortField = ApplicationSortField.id,
    order: SortOrder = SortOrder.desc,
):
    stmt = select(Application)

    if status:
        stmt = stmt.where(Application.status == status)

    if company:
        stmt = stmt.where(Application.company == company)

    sort_column = getattr(Application, sort_by.value)
    stmt = stmt.order_by(
        sort_column.asc() if order == SortOrder.asc else sort_column.desc()
    )

    stmt = stmt.offset(skip).limit(limit)

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
