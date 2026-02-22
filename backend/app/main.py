from app.core.security import AuthMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import auth, users, establishments, inspections

app = FastAPI(
    title="API Inspeção Sanitária",
    description="API para gestão de inspeções sanitárias",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/api/users", tags=["Usuários"])
app.include_router(
    establishments.router,
    prefix="/api/establishments",
    tags=["Estabelecimentos"]
)
app.include_router(
    inspections.router,
    prefix="/api/inspections",
    tags=["Inspeções"]
)


@app.get("/")
async def root():
    return {
        "message": "API Inspeção Sanitária",
        "version": "0.0.1",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
