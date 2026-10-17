from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .variables import KEY_VALIDITY, T0

router = APIRouter()
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent / "web"
)

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "key_validity": KEY_VALIDITY,
            "t0": T0.isoformat(),
        },
    )
