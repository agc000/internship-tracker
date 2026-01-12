from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Application(SQLModel, table=True):
    __tablename__ = "applications"

    id: Optional[int] = Field(default=None, primary_key=True)

    company: str
    role: str

    status: str = Field(default="applied", index=True)

    applied_date: datetime = Field(default_factory=datetime.utcnow)
