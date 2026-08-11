from fastapi import APIRouter, status 
from src.schemas.webhook_payload import IncidentWebhook

router = APIRouter()

@router.post("/alert", status_code=status.HTTP_202_ACCEPTED)
async def receive_alert(payload: IncidentWebhook):
    print(f"[INCIDENTE DETECTADO] Serviço: {payload.service_name}")
    print(f"Status: {payload.status} | Erro: {payload.error_message}")

    return {
        "status": "received",
        "message": f"Alerta do serviço {payload.service_name} registrado com sucesso."
    }