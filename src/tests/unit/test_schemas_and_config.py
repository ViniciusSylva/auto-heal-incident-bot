import pytest
from pydantic import ValidationError
from src.core.config import settings
from src.schemas.webhook_payload import IncidentWebhook


def test_settings_load_defaults():
    """Garante que as configurações padrão do sistema são carregadas corretamente."""
    assert settings.PROJECT_NAME == "Auto-Heal Incident Bot API"
    assert settings.VERSION == "1.0.0"
    assert settings.API_V1_STR == "/api/v1"


def test_incident_webhook_valid_payload():
    """Testa a criação de um payload de webhook válido."""
    payload_data = {
        "service_name": "app-victim",
        "status": "CRITICAL",
        "error_message": "Database connection timeout",
        "environment": "production",
        "details": "Port 5432 unreachable",
    }
    webhook = IncidentWebhook(**payload_data)

    assert webhook.service_name == "app-victim"
    assert webhook.status == "CRITICAL"
    assert webhook.environment == "production"


def test_incident_webhook_default_values():
    """Garante que os valores padrão do schema (environment e details) funcionam."""
    payload_data = {
        "service_name": "payment-api",
        "status": "DOWN",
        "error_message": "Out of memory",
    }
    webhook = IncidentWebhook(**payload_data)

    assert webhook.environment == "prod"
    assert webhook.details is None


def test_incident_webhook_invalid_payload():
    """Garante que faltar campos obrigatórios dispara um erro de validação do Pydantic."""
    with pytest.raises(ValidationError):
        IncidentWebhook(service_name="auth-service", status="CRITICAL")