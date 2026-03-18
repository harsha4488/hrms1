from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine
from app.routes import auth, employee, leave

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="secret")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(leave.router)