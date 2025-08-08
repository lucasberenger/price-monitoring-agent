import logging


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    logging.basicConfig(
        level=logging.DEBUG,
        encoding='utf-8',
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="app.log",
    )

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(ch)

    return logger