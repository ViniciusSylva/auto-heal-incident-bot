import logging
import httpx
from src.core.config import settings

logger = logging.getLogger("uvicorn.error")


class NotifierService:

    def __init__(self):
        self.webhook_url = settings.DISCORD_WEBHOOK_URL

    async def send_notification(self, title: str, description: str, color: int = 3447003) -> bool:
        if not self.webhook_url:
            logger.warning("[NOTIFIER] DISCORD_WEBHOOK_URL não configurada. Notificação ignorada.")
            return False

        payload = {
            "embeds": [
                {
                    "title": title,
                    "description": description,
                    "color": color,
                    "footer": {"text": "Auto-Heal Bot System"},
                }
            ]
        }

        try:
            # Uso do cliente HTTP assíncrono httpx
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(self.webhook_url, json=payload)
                response.raise_for_status()
                logger.info(f"[NOTIFIER] Notificação enviada com sucesso: '{title}'")
                return True
        except httpx.HTTPError as e:
            logger.error(f"[NOTIFIER] Erro ao enviar notificação para o Discord: {str(e)}")
            return False


notifier_service = NotifierService()