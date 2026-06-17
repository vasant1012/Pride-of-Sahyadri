import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Create logs directory if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Common formatter (with file + line number)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",  # NOQA E501
    datefmt="%Y-%m-%d %H:%M"
)


logger = logging.getLogger("pipeline")
logger.setLevel(logging.DEBUG)

# File handler
fileName = f"rag_pipeline_{datetime.now().strftime('%Y%m%d')}.log"
file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, fileName), maxBytes=5 * 1024 * 1024, backupCount=3  # NOQA E501
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
