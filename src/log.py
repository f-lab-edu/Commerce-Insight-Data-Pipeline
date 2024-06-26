import sys

sys.path.append(".")
import logging
from logging.handlers import RotatingFileHandler
import os

log_dir = "./log"
os.makedirs(log_dir, exist_ok=True)
max_file_size = 1024 * 1024 * 10  # 10MB
backup_count = 5


def make_logger(name, filename):
    log_file = os.path.join(log_dir, filename)
    handler = RotatingFileHandler(
        log_file, maxBytes=max_file_size, backupCount=backup_count, encoding="utf-8"
    )
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


twitter_logger = make_logger("twitter", "twitter.log")
amazon_logger = make_logger("amazon", "amazon_product.log")
