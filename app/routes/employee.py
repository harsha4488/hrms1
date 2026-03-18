from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.database import SessionLocal
from app.models import Employee

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def dashboard(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse("/")

    db = SessionLocal()
    user = db.query(Employee).get(user_id)

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user}
    )


@router.get("/admin/employees")
def employees(request: Request):
    if request.session.get("role") != "admin":
        return RedirectResponse("/")

    db = SessionLocal()
    users = db.query(Employee).all()

    return templates.TemplateResponse(
        "employees.html",
        {"request": request, "users": users}
    )

@router.get("/debug/users")
def get_users():
    db = SessionLocal()
    users = db.query(Employee).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "password": u.password,
            "role": u.role
        }
        for u in users
    ]