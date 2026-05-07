from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.signature_routes import router as signature_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.APP_DEBUG,
    version="0.1.0",
)

# 👇 AQUÍ agregas CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 Luego registras rutas
app.include_router(router)
app.include_router(signature_router)