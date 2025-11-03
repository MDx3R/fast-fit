from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastfit.identity.application.interfaces.services.token_intospector import (
    ITokenIntrospector,
)
from fastfit.identity.domain.value_objects.descriptor import IdentityDescriptor


def get_access_token(request: Request) -> str | None:
    return request.cookies.get("access_token")


def get_refresh_token(request: Request) -> str | None:
    return request.cookies.get("refresh_token")


def is_authenticated(
    token: Annotated[str | None, Depends(get_access_token)],
) -> bool:
    return token is not None


def require_authenticated(
    authenticated: Annotated[bool, Depends(is_authenticated)],
) -> None:
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )


def is_unauthenticated(
    authenticated: Annotated[bool, Depends(is_authenticated)],
) -> bool:
    return not authenticated


def require_unauthenticated(
    authenticated: Annotated[bool, Depends(is_authenticated)],
) -> None:
    if authenticated:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are already logged in",
        )


async def get_descriptor(
    request: Request,
    token: Annotated[str, Depends(get_access_token)],
    token_introspector: Annotated[ITokenIntrospector, Depends()],
    _: Annotated[None, Depends(require_authenticated)],
) -> IdentityDescriptor:
    if hasattr(request.state, "user"):
        user: IdentityDescriptor = request.state.user
        return user

    user = await token_introspector.extract_user(token)
    request.state.user = user
    return user
