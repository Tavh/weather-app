import logging
import os
import sys

def configure_logging():
    """
    Configures the root logger with a consistent format and configurable level.
    """
    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] %(levelname)s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout
    )

    # Silence noisy libraries
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
