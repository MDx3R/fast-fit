from typing import Annotated
from urllib.parse import quote

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastfit.auth.application.dtos.commands.logout_command import LogoutCommand
from fastfit.auth.application.dtos.models.auth_tokens import AuthTokens
from fastfit.auth.application.interfaces.usecases.command.logout_use_case import (
    ILogoutUseCase,
)
from fastfit.auth.application.interfaces.usecases.command.send_code_use_case import (
    ISendCodeUseCase,
    SendCodeCommand,
)
from fastfit.auth.application.interfaces.usecases.command.verify_code_use_case import (
    IVerifyCodeUseCase,
    VerifyCodeCommand,
)
from fastfit.identity.presentation.http.fastapi.auth import (
    get_access_token,
    get_refresh_token,
)


# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

auth_router = APIRouter()


# GET endpoint to render the login page
@auth_router.get("/login", name="login")
async def get_login(
    request: Request, token: Annotated[str | None, Depends(get_access_token)]
) -> Response:
    if token:
        return RedirectResponse(url="/menu", status_code=303)

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "phone_placeholder": "+79991234567",
            "code_placeholder": "Введите код",
            "button_text": "Получить код",
            "login_button_text": "Войти",
            "form_description": "Мы отправим код подтверждения на ваш номер телефона.",
            "error_message": None,
        },
    )


# POST endpoint to handle login form submission (phone number and code verification)
@auth_router.post("/login")
async def post_login(  # noqa: PLR0913
    request: Request,
    token: Annotated[str | None, Depends(get_access_token)],
    send_code_use_case: Annotated[ISendCodeUseCase, Depends()],
    verify_code_use_case: Annotated[IVerifyCodeUseCase, Depends()],
    phone: Annotated[str, Form()],
    code: Annotated[str | None, Form()] = None,
) -> Response:
    if token:
        return RedirectResponse(url="/menu", status_code=303)

    code = code or None
    try:
        if code is None:
            # Step 1: Send verification code
            send_command = SendCodeCommand(phone_number=phone)
            await send_code_use_case.execute(send_command)
            # Render login page with code input field visible
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "phone_placeholder": phone,
                    "code_placeholder": "Введите код",
                    "button_text": "Войти",
                    "login_button_text": "Войти",
                    "form_description": "Введите код, отправленный на ваш номер телефона.",
                    "error_message": None,
                    "show_code_field": True,
                },
            )
        else:
            # Step 2: Verify code
            verify_command = VerifyCodeCommand(phone_number=phone, code=code)
            auth_tokens: AuthTokens = await verify_code_use_case.execute(verify_command)
            # Set token in cookies (or session, depending on your auth mechanism)
            response = RedirectResponse(url="/menu", status_code=303)
            response.set_cookie(
                key="access_token", value=auth_tokens.access_token, httponly=True
            )
            response.set_cookie(
                key="refresh_token", value=auth_tokens.refresh_token, httponly=True
            )
            return response
    except Exception as e:
        # Render login page with error message
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "phone_placeholder": phone or "+79991234567",
                "code_placeholder": "Введите код",
                "button_text": "Получить код" if code is None else "Войти",
                "login_button_text": "Войти",
                "form_description": "Мы отправим код подтверждения на ваш номер телефона.",
                "error_message": quote(str(e)),
                "show_code_field": code is not None,
            },
        )


# POST endpoint for logout
@auth_router.get("/logout", name="logout")
async def logout(
    token: Annotated[str | None, Depends(get_refresh_token)],
    logout_use_case: Annotated[ILogoutUseCase, Depends()],
) -> RedirectResponse:
    if not token:
        return RedirectResponse(url="/menu", status_code=303)

    try:
        command = LogoutCommand(refresh_token=token)
        await logout_use_case.execute(command)

        # Clear the auth token cookie and redirect to login
        response = RedirectResponse(url="/menu", status_code=303)
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")

        return response
    except Exception as e:
        # Redirect to login with an error message (could be stored in session or query param)
        response = RedirectResponse(url="/menu", status_code=303)
        response.set_cookie(key="error_message", value=quote(str(e)), httponly=True)
        return response
