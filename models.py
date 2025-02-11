from sqlalchemy import column, Integer, String, Boolean, Column
from database import  Base

class User(Base):
    __table_name__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Integer, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
