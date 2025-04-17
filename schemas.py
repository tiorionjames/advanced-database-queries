from pydantic import BaseModel
from datetime import date


class EntryCreate(BaseModel):
    posted_date: date
    title: str
    body: str


from pydantic import BaseModel
from typing import Optional
from datetime import date


class EntryUpdate(BaseModel):
    posted_date: Optional[date] = None
    title: Optional[str] = None
    body: Optional[str] = None


from pydantic import BaseModel
from datetime import date


class EntryOut(BaseModel):
    id: int
    posted_date: date
    title: str
    body: str

    class Config:
        orm_mode = True
