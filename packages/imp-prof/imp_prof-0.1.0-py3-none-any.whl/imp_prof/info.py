name = "Imp-Prof"
name_unify = name.lower()
version = (0, 1, 0)
__version__ = ".".join(map(str, version))
__build__ = "2022-10-14T13:30:00.000+00:00"
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
