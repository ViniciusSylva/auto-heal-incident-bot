import logging
from fastapi import APIRouter, BackgroundTasks, Depends, status
from src.automation.docker_healer import docker_healer
from src.core.security import verify_api_key
from src.schemas.webhook_payload import IncidentWebhook
from src.services.notifier import notifier_service

logger = logging.getLogger("uvicorn.error")

router = APIRouter()


async def process_incident_task(payload: IncidentWebhook) -> None:
    logger.info(f"[BACKGROUND TASK] Tratando incidente do serviço: {payload.service_name}")

    await notifier_service.send_notification(
        title=f"🚨 Incidente Detectado: {payload.service_name}",
        description=(
            f"**Ambiente:** {payload.environment}\n"
            f"**Status:** {payload.status}\n"
            f"**Erro:** {payload.error_message}\n\n"
            f"⏳ *Iniciando autocura via Docker...*"
        ),
        color=15158332,
    )

    success, message = docker_healer.restart_container(container_name=payload.service_name)

    if success:
        await notifier_service.send_notification(
            title=f"✅ Autocura Concluída: {payload.service_name}",
            description=f"Container reiniciado com sucesso.\n\n**Detalhes:** {message}",
            color=3066993,
        )
    else:
        await notifier_service.send_notification(
            title=f"❌ Falha na Autocura: {payload.service_name}",
            description=f"Não foi possível reiniciar o serviço.\n\n**Erro:** {message}",
            color=15158332,
        )


@router.post("/alert", status_code=status.HTTP_202_ACCEPTED)
async def receive_alert(
    payload: IncidentWebhook,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),  # Injeção direta como argumento do endpoint!
):
    logger.info(f"[WEBHOOK RECEBIDO] Alerta do serviço: {payload.service_name}")

    background_tasks.add_task(process_incident_task, payload)

    return {
        "status": "accepted",
        "message": f"Alerta do serviço '{payload.service_name}' recebido. Processo de autocura iniciado em background.",
    }