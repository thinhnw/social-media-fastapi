from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, 
                        server_default=func.now())
    owner_id = Column(Integer, 
                      ForeignKey("users.id", ondelete="CASCADE"),
                      nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, 
                        server_default=func.now())
    

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, 
                     ForeignKey("users.id", ondelete="CASCADE"), 
                     primary_key=True)
    post_id = Column(Integer, 
                     ForeignKey("posts.id", ondelete="CASCADE"), 
                     primary_key=True)