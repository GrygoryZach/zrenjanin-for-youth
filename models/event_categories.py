from sqlalchemy import Column, Integer, String, ForeignKey
from db.db_session import SqlAlchemyBase


class EventCategory(SqlAlchemyBase):
    __tablename__ = 'event_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    parent_id = Column(Integer, ForeignKey("event_categories.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent": self.parent.to_dict() if self.parent_id is not None else None
        }
