from typing import List, Any, Union, Optional

from database import DB
from database.models import Base


class Operation:

    def __init__(self, database: DB, table: Base):
        self.database = database
        self.table = table

    def add(self, obj):
        with self.database.db_session() as session:
            if isinstance(obj, self.table):
                session.add(obj)
                session.commit()
                session.refresh(obj)
                session.expunge(obj)

                return obj

    def get(self, obj: Union[Any, int]) -> Optional[Any]:
        if isinstance(obj, self.table):
            return obj
        with self.database.db_session() as session:
            result = session.query(self.table).get(obj)

            if result is not None:
                session.expunge(result)

            return result

    def find_all(self) -> List[Any]:
        with self.database.db_session() as session:
            result = session.query(self.table).all()

            return result

    def find_where(self, where) -> List[Any]:
        with self.database.db_session() as session:
            result = session.query(self.table).filter(where).all()

            return result

    def delete_all(self):
        with self.database.db_session() as session:
            session.query(self.table).delete()
