import asyncio
import typing

import fastapi
import fastapi.middleware.cors

from . import (
    info,
    log,
    envs,
    loader,
    messaging,
    metric,
    routes,
)


def create_app(verbose: int = 0) -> fastapi.FastAPI:
    """Web application factory"""
    config = loader.Config(root_path=__file__)
    config.from_py_file("./default_config.py")
    config.from_py_file("/etc/imp-prof/config.py", silent=True)
    config.from_mapping(
        envs.load_environs(
            model=config,
            prefix="IMP_PROF_",
        )
    )
    verbose = max(config.get("VERBOSE") or 0, verbose)
    log.configure(
        config.get("LOG_CONF"),
        verbose=verbose,
        version=info.version,
        build_number=config.get("BUILD_NUMBER") or "",
    )
    promethean = metric.Recorder()

    async def record_message(message: messaging.JsonType) -> None:
        records: typing.Sequence[dict]
        if isinstance(message, dict):
            records = (message,)
        elif isinstance(message, (list, tuple)):
            records = message
        else:
            return
        for record in records:
            if not isinstance(record, dict):
                continue
            try:
                if not promethean.write(record):
                    log.warning(f"Message is not in valid format {record}")
            except (AttributeError, TypeError) as e:
                log.error(f"promethean.record failed on {record} with error {e}")

    pika_consumer = messaging.consumer.AsyncConsumer(
        record_message,
        **config.get_namespace("AMQP_"),
    )

    app = fastapi.FastAPI(
        version=info.__version__,
        title=info.name,
        debug=bool(verbose),
        description=info.description,
        contact=info.contact,
    )
    app.include_router(routes.main_router)
    app.include_router(routes.meta_router)
    app.add_middleware(
        fastapi.middleware.cors.CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setattr(app.state, info.CONSUMER_NAME, pika_consumer)

    @app.on_event("startup")
    async def startup() -> None:
        promethean.expose(app)
        loop = asyncio.get_running_loop()
        task = loop.create_task(pika_consumer.consume(loop))
        await task

    return app
