from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .variables import (
    CONTACT_EMAIL,
    HOSTING_LOG_NOTE,
    KEY_VALIDITY,
    OPERATOR_NAME,
    SOURCE_CODE_LINK,
    T0,
)

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
            "source_code_link": SOURCE_CODE_LINK,
        },
    )

@router.get("/privacy", response_class=HTMLResponse)
def privacy(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="privacy.html",
        context={
            "operator_name": OPERATOR_NAME,
            "contact_email": CONTACT_EMAIL,
            "hosting_log_note": HOSTING_LOG_NOTE,
        },
    )
