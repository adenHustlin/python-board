from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    boards = relationship("Board", back_populates="owner")
    posts = relationship("Post", back_populates="author")


class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    public = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("account.id"))
    post_count = Column(Integer, default=0)
    owner = relationship("Account", back_populates="boards")
    posts = relationship("Post", back_populates="board")


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    board_id = Column(Integer, ForeignKey("board.id"))
    author_id = Column(Integer, ForeignKey("account.id"))

    board = relationship("Board", back_populates="posts")
    author = relationship("Account", back_populates="posts")
