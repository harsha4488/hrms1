from app.database import SessionLocal
from app.models import Employee

@app.on_event("startup")
def create_admin():
    db = SessionLocal()

    admin = db.query(Employee).filter_by(email="admin@test.com").first()

    if not admin:
        db.add(Employee(
            name="Admin",
            email="admin@test.com",
            password="admin123",
            role="admin"
        ))
        db.commit()
        print("Admin created")