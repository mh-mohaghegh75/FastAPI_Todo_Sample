from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
import enum


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)

    # I don't know what is this shit
    todos = relationship("Todos", back_populates="owner")
    address = relationship("address", back_populates="user_address")


class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # also this shit below
    owner = relationship("Users", back_populates="todos")


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postalcode = Column(String)

    # also this shit below
    user_address = relationship("Users", back_populates="address")


class Job(str, enum.Enum):
    student = "Student"
    employee = "Employee"
    jobless = "Jobless"
    other = "Other"
