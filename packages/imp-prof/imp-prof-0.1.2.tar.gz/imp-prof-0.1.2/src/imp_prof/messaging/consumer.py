import asyncio
import logging
import typing

import aio_pika
import orjson
from aio_pika.abc import AbstractRobustExchange, AbstractRobustQueue, AbstractRobustChannel, AbstractRobustConnection

from . import types as messaging_types

MessageHandler = typing.Callable[[messaging_types.JsonType], typing.Awaitable[typing.Any]]

__all__ = (
    "MessageHandler",
    "AsyncConsumer",
)


class AsyncConsumer:
    """Asynchronous AMQP consumer"""

    __slots__ = (
        "message_handler",
        "connection_parameters",
        "prefetch_count",
        "connection",
        "queue_name",
        "exchange_name",
        "exchange_type",
        "routing_key",
        "logger",
    )
    message_handler: MessageHandler
    queue_name: str
    exchange_name: str
    exchange_type: typing.Union[str, aio_pika.ExchangeType]
    routing_key: str
    connection_parameters: dict[str, typing.Any]
    prefetch_count: int
    connection: typing.Optional[aio_pika.abc.AbstractRobustConnection]
    logger: messaging_types.LoggerLike

    def __init__(
        self,
        message_handler: MessageHandler,
        prefetch_count: int = 255,
        host: str = "127.0.0.1",
        port: int = 5672,
        queue_name: str = "profiling",
        exchange_name: str = "profiling",
        exchange_type: typing.Union[str, aio_pika.ExchangeType] = aio_pika.ExchangeType.FANOUT,
        routing_key: typing.Union[None, str] = None,
        logger: typing.Optional[messaging_types.LoggerLike] = None,
        **kwargs,
    ) -> None:
        """
        Define consumer. Connection si not established yet. See `self.consume`.

        :param message_handler: callback to process incoming message
        :param prefetch_count: buffer to get more messages from queue at once, can lead to speed up
        :param host: rabbitMQ server host
        :param port: rabbitMQ server port
        :param queue_name: queue name to consume
        :param exchange_name: exchange name to bind queue with
        :param exchange_type: exchange type to bind queue with
        :param routing_key: subscribe queue to exchange
        :param logger: loging object to use
        :param kwargs: other connection params, like `timeout goes here`
        """
        self.logger = logger or logging.getLogger(__name__)
        self.message_handler = message_handler
        self.prefetch_count = prefetch_count
        self.connection_parameters = {**kwargs, "host": host, "port": port}
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_key = routing_key or "*"
        self.connection = None

    async def is_closed(self) -> bool:
        """Is `self.connection` established?"""
        return self.connection is None or self.connection.is_closed

    async def consume(
        self,
        loop: asyncio.AbstractEventLoop,
    ) -> AbstractRobustConnection:
        """
        Setup message listener with the current running loop.

        :param loop: active loop of async python to use
        """
        self.connection: AbstractRobustConnection = await aio_pika.connect_robust(
            loop=loop,
            **self.connection_parameters,
        )
        channel: AbstractRobustChannel = await self.connection.channel()
        await channel.set_qos(prefetch_count=self.prefetch_count)
        exchange: AbstractRobustExchange = await channel.declare_exchange(self.exchange_name, self.exchange_type)
        queue: AbstractRobustQueue = await channel.declare_queue(
            self.queue_name,
            durable=True,
            robust=True,
        )
        await queue.bind(exchange, self.routing_key)
        await queue.consume(self.process_incoming_message, no_ack=False)
        self.logger.info(f"{type(self).__qualname__} - established pika async listener")
        return self.connection

    async def process_incoming_message(
        self,
        message: aio_pika.abc.AbstractIncomingMessage,
    ) -> None:
        """
        Processing incoming message from RabbitMQ.

        :param message: incoming message is parsed as json and passed to `self.message_handler`
        """
        body = message.body
        await message.ack()
        if body:
            _ = await self.message_handler(orjson.loads(body))
