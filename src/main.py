import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqladmin import Admin

# admin views
from src.admin import UsersAdmin, authentication_backend
from src.auth import auth_router
from src.database import db
from src.logger import log

# routers
from src.users import users_router
from src.utils import generate_endpoint_name

app = FastAPI(
    generate_unique_id_function=generate_endpoint_name,
    title="FastAPI",
    description="FastAPI",
    docs_url="/",
)
templates = Jinja2Templates(directory="src/templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
admin = Admin(app, db.get_engine(), authentication_backend=authentication_backend)
admin.add_model_view(UsersAdmin)
# including routers
app.include_router(users_router)
app.include_router(auth_router)

# including admin views


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    log(log.INFO, "Request handling time:\t %s", process_time)
    return response
