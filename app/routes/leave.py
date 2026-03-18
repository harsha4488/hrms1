from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.database import SessionLocal
from app.models import Leave

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Apply Leave Page
@router.get("/apply-leave")
def apply_leave_page(request: Request):
    return templates.TemplateResponse("apply_leave.html", {"request": request})


# Apply Leave Logic
@router.post("/apply-leave")
def apply_leave(
    request: Request,
    from_date: str = Form(...),
    to_date: str = Form(...)
):
    user_id = request.session.get("user_id")

    db = SessionLocal()

    leave = Leave(
        employee_id=user_id,
        from_date=from_date,
        to_date=to_date
    )

    db.add(leave)
    db.commit()

    return RedirectResponse("/my-leaves", status_code=303)


# My Leaves
@router.get("/my-leaves")
def my_leaves(request: Request):
    user_id = request.session.get("user_id")

    db = SessionLocal()
    leaves = db.query(Leave).filter_by(employee_id=user_id).all()

    return templates.TemplateResponse(
        "my_leaves.html",
        {"request": request, "leaves": leaves}
    )


# Admin View Leaves
@router.get("/admin/leaves")
def admin_leaves(request: Request):
    if request.session.get("role") != "admin":
        return RedirectResponse("/")

    db = SessionLocal()
    leaves = db.query(Leave).all()

    return templates.TemplateResponse(
        "admin_leaves.html",
        {"request": request, "leaves": leaves}
    )


# Approve Leave
@router.get("/approve/{leave_id}")
def approve(leave_id: int):
    db = SessionLocal()
    leave = db.query(Leave).get(leave_id)

    leave.status = "Approved"
    db.commit()

    return RedirectResponse("/admin/leaves", status_code=303)


@router.get("/reject/{leave_id}")
def reject(leave_id: int):
    db = SessionLocal()
    leave = db.query(Leave).get(leave_id)

    leave.status = "Rejected"
    db.commit()

    return RedirectResponse("/admin/leaves", status_code=303)
