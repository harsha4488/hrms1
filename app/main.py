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


# ✅ SAFE seed (NO DB DELETE — prevents crash)
@app.on_event("startup")
def seed_users():
    db = SessionLocal()
    try:
        if not db.query(Employee).first():
            db.add(Employee(
                name="Admin",
                email="admin@test.com",
                password="admin123",
                role="admin"
            ))
            db.add(Employee(
                name="User",
                email="user@test.com",
                password="1234",
                role="employee"
            ))
            db.commit()
            print("Users created")
    except Exception as e:
        print("Startup error:", e)
    finally:
        db.close()


# ✅ IMPORTANT — include routers
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(leave.router)