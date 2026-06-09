from fastapi import APIRouter

from backend.services.categorias import (
    listar_categorias,
    criar_categoria
)

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router.get("")
def categorias():

    return listar_categorias()


@router.post("")
def categoria(data: dict):

    ok = criar_categoria(
        data["nome"]
    )

    return {"success": ok}