import datetime as dt
import typing

from fastapi import APIRouter, Request
from pydantic import BaseModel, fields

from . import (
    info,
    messaging,
)

__all__ = (
    "main_router",
    "meta_router",
    "birth_time",
)
birth_time = dt.datetime.utcnow()
main_router = APIRouter()
meta_router = APIRouter(
    prefix="/meta",
    tags=["meta"],
)


class Index(BaseModel):
    """Brief API info page."""

    server: str = fields.Field(..., title="server", description="technical server name")
    build: str = fields.Field(..., title="build", description="build number, usually timestamp")
    version: str = fields.Field("0.1.0", title="version", description="server version in format major.minor.fix")


@main_router.get("/", response_model=Index)
async def index():
    """Title page with basic info."""
    return {
        "server": info.name_unify,
        "build": info.__build__,
        "version": info.__version__,
    }


class Meta(BaseModel):
    """Server meta info"""

    server: str = fields.Field(..., title="server", description="service name")
    build: str = fields.Field(..., title="build", description="build number, usually timestamp")
    version: typing.Sequence[int] = fields.Field(
        ..., example=[0, 1, 0], title="version", description="format [major, minor, fix]"
    )
    birth_time: dt.datetime = fields.Field(..., title="birth_time", description=" stamp of server start")
    author: str = fields.Field(..., title="author", description="project author")


@meta_router.get("/", response_model=Meta)
async def about_server() -> Meta:
    """Info about this app."""
    return Meta(
        server=info.name_unify,
        build=info.__build__,
        version=info.version,
        birth_time=birth_time,
        author=info.__author__,
    )


class Ping(BaseModel):
    """Is alive?"""

    success: bool = fields.Field(..., title="success", description="it is alive!")


@meta_router.get("/ping", response_model=Ping)
async def ping() -> Ping:
    """Is this app alive?"""
    return Ping(success=True)


@meta_router.get("/rabbit_mq", response_model=Ping)
async def ping_rabbit_mq(request: Request) -> Ping:
    """Is rabbit_mq reachable by this app?"""
    consumer: messaging.consumer.AsyncConsumer = getattr(request.app.state, info.CONSUMER_NAME, None)
    return Ping(
        success=(consumer is not None) and (not await consumer.is_closed()),
    )
