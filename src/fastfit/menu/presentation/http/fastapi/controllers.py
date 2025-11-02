from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

menu_router = APIRouter()


@menu_router.get("/menu")
async def get_login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("menu.html", {})
