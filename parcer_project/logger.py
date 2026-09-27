import logging
from pathlib import Path


def setup_logger(log_file: str = "app.log") -> logging.Logger:
    logger = logging.getLogger("transaction_parser")
    logger.setLevel(logging.INFO)

    # Защита от дублирования обработчиков при повторном вызове
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. Вывод в файл app.log
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()