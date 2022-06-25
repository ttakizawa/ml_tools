from logging import getLogger, StreamHandler, Formatter, INFO


def get_logger(name: str = None, level=INFO):
    log_format = "%(asctime)s %(filename)s %(funcName)s "  \
                 "[%(levelname)s] %(message)s"

    date_format = "%Y-%m-%dT%H:%M:%S%z"
    logger = getLogger(name)
    logger.setLevel(level)
    sh = StreamHandler()
    sh.setLevel(level)
    formatter = Formatter(log_format, date_format)
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    return logger
