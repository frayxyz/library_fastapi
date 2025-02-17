from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)

    borrowed_books = relationship("Book", back_populates="borrowed_by")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=True)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    borrowed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    author = relationship("Author", back_populates="books")
    borrowed_by = relationship("User", back_populates="borrowed_books")