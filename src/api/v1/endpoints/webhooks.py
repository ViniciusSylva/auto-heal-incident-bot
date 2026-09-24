import logging
from fastapi import APIRouter, status, Depends
from src.schemas.webhook_payload import IncidentWebhook
from src.core.security import verify_api_key

# Configuração do logger padrão da aplicação
logger = logging.getLogger("uvicorn.error")

router = APIRouter()


@router.post(
    "/alert",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(verify_api_key)]
)
async def receive_alert(payload: IncidentWebhook):
    logger.info(
        f"[INCIDENTE DETECTADO] Serviço: {payload.service_name} | "
        f"Status: {payload.status} | Erro: {payload.error_message}"
    )

    return {
        "status": "received",
        "message": f"Alerta do serviço {payload.service_name} registrado com sucesso."
    }