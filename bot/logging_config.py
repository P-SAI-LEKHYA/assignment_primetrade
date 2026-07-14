import logging
def setup_logging():
    logger_format="%(asctime)s [%(levelname)s %(name)s:%(message)s]"
    logging.basicConfig(
        level=logging.INFO,
        format=logger_format,
        handlers=[
            logging.FileHandler("events.log"),
            logging.StreamHandler(),
        ]
    
    )
    return logging.getLogger("Trading Bot")