from typing import List

from pydantic import BaseModel


class SimpleAggregatorResponseItem(BaseModel):
    hour_bucket: str
    num_events: int


class SimpleAggregatorResponseItems(BaseModel):
    customer_id: str
    data: List[SimpleAggregatorResponseItem]
