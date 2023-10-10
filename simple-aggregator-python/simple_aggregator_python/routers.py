from dependency_injector.wiring import inject,Provide
from fastapi import APIRouter, Depends
from simple_aggregator_python.containers import SimpleAggregatorContainer
from simple_aggregator_python.schema import SimpleAggregatorResponseItems
from simple_aggregator_python.service import SimpleAggregatorService
import logging

events_in_hour_router = APIRouter()

@events_in_hour_router.get("/")
def welcome():
    return "Simple Aggregator Service"

@events_in_hour_router.get("/events/{customer_id}")
@inject
def count_events(customer_id: str, start_timestamp: str, end_timestamp: str, simple_aggregator_service: SimpleAggregatorService = Depends(Provide[SimpleAggregatorContainer.simple_aggregator_service])) -> SimpleAggregatorResponseItems:
    logging.info(f"Counting events for {customer_id} from {start_timestamp} to {end_timestamp}")
    return simple_aggregator_service.count_events(customer_id, start_timestamp, end_timestamp)
