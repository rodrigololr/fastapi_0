from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from fast_zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
