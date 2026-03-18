from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine, SessionLocal
from app.models import Employee
from app.routes import auth, employee, leave
import os

app = FastAPI()

# ✅ Session middleware (REQUIRED)
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")


# 🚨 RESET DB + SEED USERS (Render fix)
@app.on_event("startup")
def reset_and_seed():
    try:
        # 🔥 DELETE OLD DB (forces clean start)
        if os.path.exists("hrms.db"):
            os.remove("hrms.db")
            print("Old DB deleted")

        # ✅ Recreate tables
        Base.metadata.create_all(bind=engine)

        db = SessionLocal()

        # ✅ Create Admin
        db.add(Employee(
            name="Admin",
            email="admin@test.com",
            password="admin123",
            role="admin"
        ))

        # ✅ Create Employee
        db.add(Employee(
            name="User",
            email="user@test.com",
            password="1234",
            role="employee"
        ))

        db.commit()
        db.close()

        print("DB reset + users created")

    except Exception as e:
        print("Startup error:", e)


# ✅ Include routes
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(leave.router)