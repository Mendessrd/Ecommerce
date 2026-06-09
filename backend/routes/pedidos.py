from fastapi import APIRouter

from backend.services.pedidos import (
    criar_pedido,
    listar_pedidos_usuario
)

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post("")
def pedidos(data: dict):

    ok = criar_pedido(
        data["uid"],
        data["pid"],
        data["qtd"]
    )

    return {"success": ok}


@router.get("/{uid}")
def pedidos_usuario(uid: int):

    return listar_pedidos_usuario(uid)