import logging
import typing

__all__ = (
    "LoggerLike",
    "JsonType",
)
LoggerLike = typing.Union[logging.Logger, logging.LoggerAdapter]
JsonType = typing.Union[str, int, float, bool, None, list["JsonType"], dict["str", "JsonType"]]
