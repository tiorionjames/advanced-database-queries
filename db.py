from sqlalchemy import create_engine, Column, Date, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'postgresql+psycopg://postgres:postgres@localhost:5432/journal'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entry'
    # add all of the columns for Entry here
    # the id field has already been done as an example
    id = Column(Integer, primary_key=True)

    # NOTE: this method is not required by SQLAlchemy, but is very useful
    # when you want to turn an Entry into an equivalent dictionary
    def to_dict(self) -> dict:
        # return a dictionary with all of the fields defined above
        # the id field has already been done as an example
        return {
            'id': self.id,
            # finish this off
        }


def get_all_entries() -> list[dict]:
    return []


def add_entry(entry: dict) -> dict:
    return None


def get_entry(entry_id: int) -> dict | None:
    return None


def delete_entry(entry_id: int) -> None:
    return False


def update_entry(entry: dict) -> dict | None:
    return None
