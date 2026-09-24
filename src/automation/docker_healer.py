import logging
import docker
from docker.errors import NotFound, APIError

logger = logging.getLogger("uvicorn.error")


class DockerHealer:

    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            logger.error(f"[DOCKER] Não foi possível conectar ao Daemon do Docker: {str(e)}")
            self.client = None

    def restart_container(self, container_name: str) -> tuple[bool, str]:
        if not self.client:
            msg = "Conexão com o Docker não está disponível no servidor."
            logger.error(f"[DOCKER] {msg}")
            return False, msg

        try:
            logger.info(f"[DOCKER] Buscando o container: '{container_name}'...")
            container = self.client.containers.get(container_name)

            logger.info(f"[DOCKER] Estado atual do container '{container_name}': {container.status}")
            
            container.restart()
            
            logger.info(f"[DOCKER] Container '{container_name}' reiniciado com sucesso!")
            return True, f"Container '{container_name}' reiniciado com sucesso."

        except NotFound:
            msg = f"Container '{container_name}' não foi encontrado no host."
            logger.error(f"[DOCKER] {msg}")
            return False, msg

        except APIError as e:
            msg = f"Erro da API do Docker ao tentar reiniciar '{container_name}': {e.explanation}"
            logger.error(f"[DOCKER] {msg}")
            return False, msg


docker_healer = DockerHealer()