from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from src.auth import auth_router

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

# including routers
app.include_router(users_router)
app.include_router(auth_router)
