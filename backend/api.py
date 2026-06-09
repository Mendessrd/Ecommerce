from fastapi import FastAPI

from backend.routes.usuarios import router as usuarios_router
from backend.routes.produtos import router as produtos_router
from backend.routes.pedidos import router as pedidos_router
from backend.routes.categorias import router as categorias_router

app = FastAPI()

app.include_router(usuarios_router)
app.include_router(produtos_router)
app.include_router(pedidos_router)
app.include_router(categorias_router)