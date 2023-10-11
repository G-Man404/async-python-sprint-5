from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Authorizations(Base):
    __tablename__ = "authorizations"

    id = Column(Integer, primary_key=True)
    auth_token = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users")
    auth_data = Column(DateTime, index=True, default=datetime.utcnow)

    __mapper_args__ = {"eager_defaults": True}
