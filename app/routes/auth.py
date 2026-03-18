from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.models import Employee

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ================= EMPLOYEE LOGIN =================
@router.get("/", response_class=HTMLResponse)
def employee_login_page(request: Request):
    return templates.TemplateResponse("login_employee.html", {"request": request})


@router.post("/login")
def employee_login(request: Request, email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(Employee).filter(Employee.email == email).first()

    if user and user.password == password and user.role == "employee":
        request.session["user_id"] = user.id
        request.session["role"] = user.role
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse(
        "login_employee.html",
        {"request": request, "error": "Invalid employee credentials"}
    )


# ================= ADMIN LOGIN =================
@router.get("/admin", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse("login_admin.html", {"request": request})


@router.post("/admin-login")
def admin_login(request: Request, email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(Employee).filter(Employee.email == email).first()

    if user and user.password == password and user.role == "admin":
        request.session["user_id"] = user.id
        request.session["role"] = user.role
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse(
        "login_admin.html",
        {"request": request, "error": "Invalid admin credentials"}
    )


# ================= LOGOUT =================
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")