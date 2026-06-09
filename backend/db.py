import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL não encontrada no arquivo .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY não encontrada no arquivo .env")

try:
    supabase: Client = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )
    print("✅ Conectado ao Supabase com sucesso")
except Exception as e:
    print(f"❌ Erro ao conectar ao Supabase: {e}")
    raise

def get_supabase() -> Client:
    """
    Retorna a instância do cliente Supabase.
    """
    return supabase