from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.models import Employee
from app.auth import hash_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/admin/create-user")
def create_user_page(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})


@router.post("/admin/create-user")
def create_user(name: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form(...)):
    db = SessionLocal()

    user = Employee(
        name=name,
        email=email,
        password=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()

    return {"message": "User created"}