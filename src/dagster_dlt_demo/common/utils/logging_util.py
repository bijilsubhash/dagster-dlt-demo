import logging
import logging.config


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        }
    },
    "loggers": {"": {"handlers": ["stdout"], "level": "INFO"}},
}

logging.config.dictConfig(LOGGING)


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message, exc_info=True)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

    def critical(self, message):
        self.logger.critical(message, exc_info=True)
