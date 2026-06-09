from fastapi import APIRouter

from backend.services.usuarios import (
    criar_usuario,
    login_user
)

router = APIRouter()


@router.post("/login")
def login(data: dict):

    user = login_user(
        data["email"],
        data["senha"]
    )

    if not user:
        return {"error": "invalid"}

    return user


@router.post("/usuarios")
def usuarios(data: dict):

    ok = criar_usuario(
        data["nome"],
        data["email"],
        data["senha"]
    )

    return {"success": ok}