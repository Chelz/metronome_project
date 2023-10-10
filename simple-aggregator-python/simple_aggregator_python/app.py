import logging
import sys

from fastapi import FastAPI

from simple_aggregator_python.containers import SimpleAggregatorContainer
from simple_aggregator_python.routers import events_in_hour_router

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "simple-aggregator-logger": {"handlers": ["default"], "level": "DEBUG"},
    },
}

from logging.config import dictConfig

dictConfig(log_config)

logger = logging.getLogger("simple-aggregator-logger")


def create_app():
    logger.info(f"Creating FASTAPI Application....")
    container = SimpleAggregatorContainer()
    app = FastAPI()
    app.include_router(events_in_hour_router)
    app.container = container
    return app


app = create_app()
