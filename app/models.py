from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.sql.expression import null
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Posts(Base):
    __tablename__ ='posts'
    id = Column(Integer, nullable = False, primary_key = True)
    title = Column(String, nullable=False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable=False, server_default=text('true'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))

    owner_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable = False)
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable = False, primary_key = True)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))