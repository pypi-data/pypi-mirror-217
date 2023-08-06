#!/usr/bin/python3
# -*- coding: utf-8 -*-

# RabbitMQ
AMQP_HOST = "localhost"
AMQP_PORT = 5672
AMQP_RETRY_DELAY = 0.137
AMQP_RETRY = 3
AMQP_PREFETCH_COUNT = 127
AMQP_EXCHANGE_NAME = "profiling"
AMQP_EXCHANGE_TYPE = "fanout"
AMQP_QUEUE_NAME = "imp_prof"
AMQP_QUEUE_ROUTING_KEY = "*"

BUILD_NUMBER = 0

# logging
# noinspection SpellCheckingInspection
LOG_CONF = {  # see https://www.python.org/dev/peps/pep-0391/
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "general": {
            "format": "IMP-PROF: %(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "general",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "imp": {
            "level": "INFO",
            "handlers": ["stdout"],
            "propagate": False,
        }
    },
}
