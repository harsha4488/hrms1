from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine, SessionLocal
from app.models import Employee
from app.routes import auth, employee, leave

app = FastAPI()

# ✅ Sessions
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# ✅ Create tables
Base.metadata.create_all(bind=engine)


# 🔥 REFRESH USERS (ADMIN + EMPLOYEE)
@app.on_event("startup")
def refresh_users():
    db = SessionLocal()

    try:
        # ❌ DELETE ALL USERS
        db.query(Employee).delete()

        # ✅ CREATE ADMIN
        db.add(Employee(
            name="Admin",
            email="admin@test.com",
            password="admin123",
            role="admin"
        ))

        # ✅ CREATE EMPLOYEE
        db.add(Employee(
            name="User",
            email="user@test.com",
            password="1234",
            role="employee"
        ))

        db.commit()
        print("Users refreshed successfully")

    except Exception as e:
        print("Error refreshing users:", e)

    finally:
        db.close()


# ✅ Routes
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(leave.router)

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    name: str
    email: str

@app.post("/register")   # 👈 ADD THIS
def register(emp: Employee):
    return {"message": "Employee registered", "data": emp}