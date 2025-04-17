from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from sqlalchemy.orm import Session
from db import SessionLocal

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/journal"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    posted_date = Column(Date, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)


def get_all_entries() -> list[dict]:
    db = SessionLocal()
    try:
        entries = db.query(Entry).all()
        return [
            {
                "id": e.id,
                "posted_date": e.posted_date.isoformat(),
                "title": e.title,
                "body": e.body,
            }
            for e in entries
        ]
    finally:
        db.close()


def get_entry(entry_id: int) -> dict | None:
    db = SessionLocal()
    try:
        e = db.query(Entry).filter(Entry.id == entry_id).first()
        if not e:
            return None
        return {
            "id": e.id,
            "posted_date": e.posted_date.isoformat(),
            "title": e.title,
            "body": e.body,
        }
    finally:
        db.close()


def add_entry(data: dict) -> dict:
    db = SessionLocal()
    try:
        entry = Entry(
            posted_date=datetime.fromisoformat(data["posted_date"]).date(),
            title=data["title"],
            body=data["body"],
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return {
            "id": entry.id,
            "posted_date": entry.posted_date.isoformat(),
            "title": entry.title,
            "body": entry.body,
        }
    finally:
        db.close()


def delete_entry(entry_id: int) -> bool:
    db: Session = SessionLocal()
    try:
        entry = db.query(JournalEntry).get(entry_id)
        if entry is None:
            return False
        db.delete(entry)
        db.commit()
        return True
    finally:
        db.close()


def update_entry(entry_id: int, data: dict):
    db: Session = SessionLocal()
    try:
        entry = db.query(JournalEntry).get(entry_id)
        if entry is None:
            return None
        for field, value in data.items():
            if hasattr(entry, field):
                setattr(entry, field, value)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()
