from fastapi import FastAPI
from src.api.v1.endpoints.webhooks import router as webhooks_router

app = FastAPI(
    title="Auto-Heal Incident Bot API",
    description="API para recebimento de alertar e automação de respostas e incidentes",
    version="1.0.0"
)

app.include_router(webhooks_router, prefix="/api/v1/webhooks", tags=["Webhooks"])

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bem vindo à API do Auto-Heal Incident Bot!",
        "docs": "Acesse http://127.0.0.1:8000/docs para ver a documentação interativa."
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "active", "service": "Auto-Heal API" }