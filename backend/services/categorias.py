from backend.db import supabase


def listar_categorias():
    try:
        result = (
            supabase
            .table("categorias")
            .select("id,nome")
            .order("nome")
            .execute()
        )

        print("CATEGORIAS:", result.data)

        return result.data

    except Exception as e:
        print("ERRO LISTAR CATEGORIAS:", repr(e))
        return []

def criar_categoria(nome):
    try:
        result = (
            supabase
            .table("categorias")
            .insert({"nome": nome})
            .execute()
        )

        print("CATEGORIA:", result.data)

        return True

    except Exception as e:
        print("ERRO CATEGORIA:", repr(e))
        return False