from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine, SessionLocal
from app.models import Employee
from app.routes import auth, employee, leave

app = FastAPI()

# ✅ Session middleware
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# ✅ Create tables
Base.metadata.create_all(bind=engine)


# 🔥 REFRESH USERS (SAFE RESET)
@app.on_event("startup")
def refresh_users():
    db = SessionLocal()

    try:
        # ❌ DELETE ONLY USERS (NOT TABLES)
        db.query(Employee).delete()

        # ✅ RECREATE ADMIN
        db.add(Employee(
            name="Admin",
            email="admin@test.com",
            password="admin123",
            role="admin"
        ))

        # ✅ RECREATE EMPLOYEE
        db.add(Employee(
            name="User",
            email="user@test.com",
            password="1234",
            role="employee"
        ))

        db.commit()
        print("Users refreshed")

    except Exception as e:
        print("Startup error:", e)

    finally:
        db.close()


# ✅ Include routes
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(leave.router)