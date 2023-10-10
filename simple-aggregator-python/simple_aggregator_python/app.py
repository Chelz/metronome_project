from fastapi import FastAPI
from simple_aggregator_python.routers import events_in_hour_router
from simple_aggregator_python.containers import SimpleAggregatorContainer
import logging
def create_app():
    logging.info(f"Creating FASTAPI Application....")
    container = SimpleAggregatorContainer()
    app = FastAPI()
    app.include_router(events_in_hour_router)
    app.container = container
    return app

app = create_app()




