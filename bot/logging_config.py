import os
import logging
from rich.logging import RichHandler

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    
    log_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler for deep debugging
    file_handler = logging.FileHandler("logs/trading_bot.log")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)

    # Interactive Console Handler via Rich
    console_handler = RichHandler(rich_tracebacks=True, markup=True)
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, console_handler]
    )