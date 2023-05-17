import logging.config

import colorlog

# Definir níveis de cores
LOG_LEVELS = {
    "DEBUG": "blue",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

# Configuração do logger
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored_formatter": {
                "()": colorlog.ColoredFormatter,
                "format": (
                    "%(asctime)s - %(log_color)s%(levelname)s%(reset)s -"
                    " %(message)s"
                ),
                "log_colors": LOG_LEVELS,
                "secondary_log_colors": {},
                "style": "%",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "colored_formatter",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }
)
