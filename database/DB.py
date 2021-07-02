from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from database.models.base import Base


class DB:
    def __init__(self, uri="sqlite:///user_data/jogo_gourmet.db"):
        self.engine = create_engine(url=uri)
        self.session_maker = sessionmaker(bind=self.engine)

    def create_database(self):
        Base.metadata.create_all(self.engine)

    @contextmanager
    def db_session(self):
        """
        Creates a context with an open SQLAlchemy session.
        """
        session = scoped_session(session_factory=self.session_maker)
        yield session
        session.commit()
        session.close()


if __name__ == "__main__":
    database = DB()
    database.create_database()
