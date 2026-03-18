from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine, SessionLocal
from app.models import Employee
from app.routes import auth, employee, leave

app = FastAPI()

# ✅ Session middleware (REQUIRED for login)
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)


# ✅ Auto-create users (FIXES Render login issue)
@app.on_event("startup")
def create_default_users():
    db = SessionLocal()

    try:
        # Admin
        admin = db.query(Employee).filter_by(email="admin@test.com").first()
        if not admin:
            db.add(Employee(
                name="Admin",
                email="admin@test.com",
                password="admin123",
                role="admin"
            ))

        # Employee
        emp = db.query(Employee).filter_by(email="user@test.com").first()
        if not emp:
            db.add(Employee(
                name="User",
                email="user@test.com",
                password="1234",
                role="employee"
            ))

        db.commit()
        print("Default users created")

    except Exception as e:
        print("Startup error:", e)

    finally:
        db.close()


# ✅ Include routes
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(leave.router)