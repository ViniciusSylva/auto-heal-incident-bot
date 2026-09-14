from pydantic import BaseModel
from typing import Optional 

class IncidentWebhook(BaseModel):
    service_name: str
    status: str
    error_message: str
    environment: str = "prod"
    details: str | None = None