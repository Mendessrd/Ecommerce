from typing import Any, Dict, List

from backend.db import supabase


def listar_produtos() -> List[Dict[str, Any]]:
    try:
        result = (
            supabase
            .table("produtos")
            .select("""
                id,
                nome,
                preco,
                estoque,
                categorias(nome)
            """)
            .order("id")
            .execute()
        )

        data = getattr(result, "data", None)
        if not data or not isinstance(data, list):
            return []

        produtos: List[Dict[str, Any]] = []

        for p in data:
            if not isinstance(p, dict):
                continue

            categoria = None
            categorias = p.get("categorias")
            if isinstance(categorias, dict):
                categoria = categorias.get("nome")

            produtos.append({
                "id": p.get("id"),
                "nome": p.get("nome"),
                "preco": float(p.get("preco", 0)),
                "estoque": p.get("estoque"),
                "categoria": categoria
            })

        return produtos

    except Exception as e:
        print(e)
        return []


def criar_produto(
    nome: str,
    descricao: str,
    preco: float,
    estoque: int,
    categoria_id: int
) -> bool:
    try:
        result = supabase.table("produtos").insert({
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "estoque": estoque,
            "categoria_id": categoria_id
        }).execute()

        return bool(getattr(result, "data", None))

    except Exception as e:
        print(e)
        return False


def atualizar_produto(
    pid: int,
    nome: str,
    descricao: str,
    preco: float,
    estoque: int,
    categoria_id: int
) -> bool:
    try:
        result = (
            supabase
            .table("produtos")
            .update({
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "estoque": estoque,
                "categoria_id": categoria_id
            })
            .eq("id", pid)
            .execute()
        )

        return bool(getattr(result, "data", None))

    except Exception as e:
        print(e)
        return False