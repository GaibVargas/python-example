import atexit
import json
import logging
import logging.config
from queue import Queue
from threading import Lock
from pathlib import Path
from typing import Any
from logging.handlers import QueueHandler, QueueListener

from infra.config import settings


class LoggingManager:
    """
    Gerenciador de configuração de logging com fila (QueueHandler/QueueListener).

    - Configura logging apenas uma vez (lazy initialization)
    - Carrega formato e handlers do arquivo JSON
    - Define o nível via .env (LOG_LEVEL)
    - Usa fila para escrita assíncrona (melhor desempenho)
    """

    _configured = False
    _lock = Lock()
    _queue_listener: QueueListener | None = None

    @classmethod
    def _load_config(cls) -> Any:
        config_path = Path(__file__).parent / "logger_config.json"
        if not config_path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {config_path}"
            )
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def _configure_logging(cls) -> None:
        with cls._lock:
            if cls._configured:
                return

            log_level = settings.log_level.upper()

            config = cls._load_config()
            config["root"]["level"] = log_level
            for handler in config.get("handlers", {}).values():
                handler["level"] = log_level

            logging.config.dictConfig(config)

            log_queue: Queue[logging.LogRecord] = Queue(-1)
            queue_handler = QueueHandler(log_queue)

            root_logger = logging.getLogger()
            root_logger.handlers = [queue_handler]

            console_handler = logging.getHandlerByName("stdout")
            if console_handler is None:
                raise RuntimeError(
                    "Handler 'stdout' não encontrado na configuração de logging."
                )
            console_handler.setLevel(log_level)

            cls._queue_listener = QueueListener(log_queue, console_handler)
            cls._queue_listener.start()
            atexit.register(cls.shutdown)

            cls._configured = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if not cls._configured:
            cls._configure_logging()
        return logging.getLogger(name)

    @classmethod
    def shutdown(cls) -> None:
        if cls._queue_listener:
            cls._queue_listener.stop() # Faz flush dos logs pendentes
        logging.shutdown()
