from sqlalchemy import Column, Integer, String
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="employee")
    leave_balance = Column(Integer, default=10)


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    from_date = Column(String)   # ✅ NEW
    to_date = Column(String)     # ✅ NEW
    status = Column(String, default="Pending")