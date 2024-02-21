from utils.customer_logger import CustomJsonFormatter

DB_DEBUG = True


if DB_DEBUG:
    LOGGING = {
        "disable_existing_loggers": False,
        "version": 1,
        "formatters": {
            "console": {
                "format": "%(name)s %(asctime)s %(levelname)s %(message)s",
            },
            "json_formatter": {
                "()": CustomJsonFormatter,
                "datefmt": "%Y-%m-%d %H:%M",
            },
        },
        "handlers": {
            "console": {
                # logging handler that outputs log messages to terminal
                "class": "logging.StreamHandler",
                "level": "DEBUG",  # message level to be written to console
                # "formatter": "json_formatter",  # apply the json_formatter
            },
        },
        "loggers": {
            "": {
                # this sets the root level logger to log debug and higher level
                # logs to console. All other loggers inherit settings from
                # the root level logger.
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,  # this tells logger to send logging message
                # to its parent (will send if set to True)
            },
            "django.db": {
                # django also has database level logging
                # "handlers": ["console"], # remove dublicate
                "level": "DEBUG",
                # "propagate": False, # remove dublicate
            },
        },
    }