from typing import Any, Dict, Optional

from backend.db import supabase


def criar_usuario(nome, email, senha):
    try:
        result = (
            supabase
            .table("usuarios")
            .insert({
                "nome": nome,
                "email": email,
                "senha": senha,
                "role": "cliente"
            })
            .execute()
        )

        print("RESULTADO:", result.data)

        return len(result.data) > 0

    except Exception as e:
        print("ERRO:", repr(e))
        return False


def login_user(email: str, senha: str) -> Optional[Dict[str, Any]]:
    try:
        result = (
            supabase
            .table("usuarios")
            .select("id,nome,role")
            .eq("email", email)
            .eq("senha", senha)
            .execute()
        )

        data = getattr(result, "data", None)
        if not data or not isinstance(data, list):
            return None

        user = data[0]
        if not isinstance(user, dict):
            return None

        return {
            "id": user.get("id"),
            "nome": user.get("nome"),
            "role": user.get("role")
        }

    except Exception as e:
        print(e)
        return None