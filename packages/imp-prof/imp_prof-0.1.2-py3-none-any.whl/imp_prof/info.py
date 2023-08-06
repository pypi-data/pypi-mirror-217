name = "Imp-Prof"
name_unify = name.lower()
version = (0, 1, 2)
__version__ = ".".join(map(str, version))
__build__ = "2023-07-03T15:00:00.000+00:00"
__author__ = "[tom trval](https://github.com/Ryu-CZ)"
description = (
    "Imp consumes log messages from [RabbitMQ](https://www.rabbitmq.com/) into [Prometheus](https://prometheus.io/) "
    "metrics published on API to be scraped "
)
contact = {
    "name": "support",
    "url": "https://en.kajot.cz/kontakt/",
    "email": "support@kajot.cz",
}
CONSUMER_NAME = "pika_consumer"
