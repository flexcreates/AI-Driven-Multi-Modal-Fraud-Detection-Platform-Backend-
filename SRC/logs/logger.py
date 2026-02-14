import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure log directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(LOG_DIR, exist_ok=True)

# Log format
FORMATTER = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s")

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger based on the component name.
    Routes logs to specific files:
    - api.* -> logs/api.log
    - database.* -> logs/database.log
    - models.* -> logs/models.log
    - main -> logs/backend_main.log
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all logs

    # Avoid adding multiple handlers if logger is already configured
    if logger.hasHandlers():
        return logger

    # Determine log file based on name prefix
    if name.startswith("api"):
        log_file = "api.log"
    elif name.startswith("database"):
        log_file = "database.log"
    elif name.startswith("models"):
        log_file = "models.log"
    else:
        log_file = "backend_main.log"

    file_path = os.path.join(LOG_DIR, log_file)

    # File Handler (Rotating: 5MB max, keep 3 backups)
    file_handler = RotatingFileHandler(file_path, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.DEBUG)

    # Console Handler (Optional: for seeing logs in docker/terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
