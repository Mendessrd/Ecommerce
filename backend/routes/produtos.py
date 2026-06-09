from fastapi import APIRouter

from backend.services.produtos import (
    listar_produtos,
    criar_produto,
    atualizar_produto
)

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.get("")
def produtos():

    return listar_produtos()


@router.post("")
def novo_produto(data: dict):

    ok = criar_produto(
        data["nome"],
        data["descricao"],
        data["preco"],
        data["estoque"],
        data["categoria_id"]
    )

    return {"success": ok}


@router.put("/{pid}")
def editar_produto(pid: int, data: dict):

    ok = atualizar_produto(
        pid,
        data["nome"],
        data["descricao"],
        data["preco"],
        data["estoque"],
        data["categoria_id"]
    )

    return {"success": ok}