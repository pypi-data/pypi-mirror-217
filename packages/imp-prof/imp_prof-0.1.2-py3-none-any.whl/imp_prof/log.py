#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import logging.config
import typing


class LikeContext:
    client_ip: typing.Optional[str]
    request_id: typing.Optional[str]


class LogConfig(typing.TypedDict):
    version: str
    disable_existing_loggers: bool
    formatters: typing.Dict[str, typing.Dict[str, str]]
    handlers: typing.Dict[str, typing.Dict[str, str]]
    loggers: typing.Dict[str, typing.Dict[str, typing.Any]]


class TraceRequest(logging.Filter):
    """
    This is a filter which injects request origin information into the log.
    """

    __slots__ = (
        "current_context",
        "version",
        "build_number",
    )

    DEFAULT: typing.ClassVar[str] = "n-a"
    current_context: typing.Optional[LikeContext]
    version: str
    build_number: str

    def __init__(self, name: str = "") -> None:
        super(TraceRequest, self).__init__(name=name)
        self.current_context = None
        self.version = "0.0.0"
        self.build_number = "0"

    def filter(self, record: logging.LogRecord) -> bool:
        """Decorate log record with request origin information"""
        if self.current_context:
            record.client_ip = self.current_context.client_ip or TraceRequest.DEFAULT
            record.request_id = self.current_context.request_id or TraceRequest.DEFAULT
        else:
            record.client_ip = TraceRequest.DEFAULT
            record.request_id = TraceRequest.DEFAULT
        record.version = self.version
        record.build_number = self.build_number
        return True


class CasinoInfo(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    DEFAULT = "n-a"
    casino_id: str

    def __init__(self, casino_id: typing.Union[int, None, str] = None, name: str = ""):
        super(CasinoInfo, self).__init__(name=name)
        if casino_id is None:
            casino_id = CasinoInfo.DEFAULT
        self.casino_id = str(casino_id)

    def filter(self, record):
        record.casino_id = self.casino_id
        return True


NOTICE = 25
logging.addLevelName(NOTICE, "NOTICE")

_logger_name = "imp"
_main_logger = None
tracing_context: TraceRequest = TraceRequest()


def debug(msg, *args, **kwargs) -> None:
    logging.getLogger(_logger_name).debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs) -> None:
    logging.getLogger(_logger_name).info(msg, *args, **kwargs)


def notice(msg, *args, **kwargs) -> None:
    logging.getLogger(_logger_name).log(NOTICE, msg, *args, **kwargs)


def warn(msg, *args, **kwargs) -> None:
    logging.getLogger(_logger_name).warning(msg, *args, **kwargs)


def warning(msg, *args, **kwargs) -> None:
    logging.getLogger(_logger_name).warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs) -> None:
    logging.getLogger(_logger_name).error(msg, *args, **kwargs)


def get_logger() -> logging.Logger:
    global _main_logger
    if not _main_logger:
        _main_logger = logging.getLogger(_logger_name)
    return _main_logger


def configure(
    log_config: typing.Optional[LogConfig] = None,
    verbose: int = 0,
    version: typing.Sequence[int] = (0, 0, 0),
    build_number: str = "0",
) -> None:
    """
    Configure the logger.

    :param log_config: serialized log config: see https://www.python.org/dev/peps/pep-0391/
    :param verbose: how much details we log
    :param version: app version
    :param build_number: app build number
    """
    global _main_logger
    if log_config:
        if verbose:
            log_config["loggers"][_logger_name]["level"] = "DEBUG"
        logging.config.dictConfig(log_config)
        _main_logger = None
        debug("LOG_CONF resolved and set up")
    else:
        notice("using default logger set up")

    tracing_context.version = ".".join(map(str, version))
    tracing_context.build_number = str(build_number)

    get_logger().addFilter(tracing_context)
    info("App logger bound")
