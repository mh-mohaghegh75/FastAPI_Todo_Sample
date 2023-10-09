from typing import Optional

from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
import enum


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(100))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    todos = relationship("Todos", back_populates="owner")


class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(100))
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")


class Job(str, enum.Enum):
    student = "Student"
    employee = "Employee"
    jobless = "Jobless"
    other = "Other"
