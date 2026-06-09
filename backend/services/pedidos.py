from typing import Any, Dict, List, Optional

from backend.db import supabase


def criar_pedido(uid: int, pid: int, qtd: int) -> bool:
    try:
        produto_result = (
            supabase
            .table("produtos")
            .select("id,preco,estoque")
            .eq("id", pid)
            .single()
            .execute()
        )

        produto = getattr(produto_result, "data", None)
        if not produto or not isinstance(produto, dict):
            return False

        estoque = produto.get("estoque")
        preco = produto.get("preco")
        if estoque is None or preco is None:
            return False

        if not isinstance(qtd, int) or qtd <= 0 or estoque < qtd:
            return False

        total = float(preco) * qtd
        pedido_result = (
            supabase
            .table("pedidos")
            .insert({
                "usuario_id": uid,
                "total": total
            })
            .execute()
        )

        pedido_data = getattr(pedido_result, "data", None)
        if not pedido_data or not isinstance(pedido_data, list):
            return False

        pedido_id = pedido_data[0].get("id") if isinstance(pedido_data[0], dict) else None
        if pedido_id is None:
            return False

        item_result = (
            supabase
            .table("pedidos_itens")
            .insert({
                "pedido_id": pedido_id,
                "produto_id": pid,
                "quantidade": qtd,
                "preco_unitario": float(preco)
            })
            .execute()
        )

        if not getattr(item_result, "data", None):
            return False

        supabase.table("produtos").update({"estoque": estoque - qtd}).eq("id", pid).execute()
        return True

    except Exception as e:
        print(e)
        return False


def listar_pedidos_usuario(uid: int) -> List[Dict[str, Any]]:
    try:
        pedidos_result = (
            supabase
            .table("pedidos")
            .select("""
                id,
                status,
                criado_em,
                pedidos_itens(
                    quantidade,
                    preco_unitario,
                    produtos(nome)
                )
            """)
            .eq("usuario_id", uid)
            .order("criado_em", desc=True)
            .execute()
        )

        pedidos_data = getattr(pedidos_result, "data", None)
        if not pedidos_data or not isinstance(pedidos_data, list):
            return []

        resultado: List[Dict[str, Any]] = []

        for pedido in pedidos_data:
            if not isinstance(pedido, dict):
                continue

            itens = pedido.get("pedidos_itens")
            if not itens or not isinstance(itens, list):
                continue

            for item in itens:
                if not isinstance(item, dict):
                    continue

                produto_nome = None
                produtos = item.get("produtos")
                if isinstance(produtos, dict):
                    produto_nome = produtos.get("nome")

                preco_unitario = item.get("preco_unitario", 0)
                quantidade = item.get("quantidade", 0)

                resultado.append({
                    "pedido_id": pedido.get("id"),
                    "produto": produto_nome,
                    "quantidade": quantidade,
                    "preco_unitario": float(preco_unitario),
                    "total": float(quantidade) * float(preco_unitario),
                    "status": pedido.get("status"),
                    "data": pedido.get("criado_em")
                })

        return resultado

    except Exception as e:
        print(e)
        return []