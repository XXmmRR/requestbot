from loguru import logger
import sys
import os

def setup_logging():
    log_folder = "/app/logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    logger.add(
        sys.stdout, 
        level="INFO", 
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )


    logger.add(
        f"{log_folder}/debug.log",
        rotation="10 MB",
        compression="zip",
        level="DEBUG",
        enqueue=True,
    )

    logger.add(
        f"{log_folder}/info.log",
        rotation="10 MB",
        compression="zip",
        level="INFO",
        enqueue=True,
    )

    logger.add(
        f"{log_folder}/error.log",
        rotation="10 MB",
        compression="zip",
        level="ERROR",
        enqueue=True,
    )