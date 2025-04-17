from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/journal"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class Entry(Base):
    __tablename__ = "entry"

    id = Column(Integer, primary_key=True, index=True)
    posted_date = Column(Date, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "posted_date": self.posted_date.isoformat(),
            "title": self.title,
            "body": self.body,
        }


# create tables if they don't exist
Base.metadata.create_all(bind=engine)


def get_all_entries() -> list[dict]:
    db: Session = SessionLocal()
    try:
        return [entry.to_dict() for entry in db.query(Entry).all()]
    finally:
        db.close()


def add_entry(entry_data: dict) -> dict:
    db: Session = SessionLocal()
    try:
        entry = Entry(
            posted_date=datetime.fromisoformat(entry_data["posted_date"]).date(),
            title=entry_data["title"],
            body=entry_data["body"],
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry.to_dict()
    finally:
        db.close()


def get_entry(entry_id: int) -> dict | None:
    db: Session = SessionLocal()
    try:
        entry = db.query(Entry).filter(Entry.id == entry_id).first()
        return entry.to_dict() if entry else None
    finally:
        db.close()


def delete_entry(entry_id: int) -> bool:
    db: Session = SessionLocal()
    try:
        entry = db.query(Entry).filter(Entry.id == entry_id).first()
        if entry is None:
            return False
        db.delete(entry)
        db.commit()
        return True
    finally:
        db.close()


def update_entry(entry_id: int, data: dict) -> dict | None:
    db: Session = SessionLocal()
    try:
        entry = db.query(Entry).filter(Entry.id == entry_id).first()
        if entry is None:
            return None
        if "posted_date" in data:
            entry.posted_date = datetime.fromisoformat(data["posted_date"]).date()
        if "title" in data:
            entry.title = data["title"]
        if "body" in data:
            entry.body = data["body"]
        db.commit()
        db.refresh(entry)
        return entry.to_dict()
    finally:
        db.close()
