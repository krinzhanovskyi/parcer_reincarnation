import logging
import sys


def setup_logger(log_file: str = "app.log") -> logging.Logger:
    """
    Configures the logger.
    Should be called once from the main entry point.
    """
    logger = logging.getLogger("transaction_parser")
    logger.setLevel(logging.INFO)

    # Prevent adding duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console output (stream to stdout instead of default stderr for INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File output
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger