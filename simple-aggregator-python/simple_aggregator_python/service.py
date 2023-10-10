from typing import List

from pydantic import TypeAdapter

from simple_aggregator_python.schema import (
    SimpleAggregatorResponseItem,
    SimpleAggregatorResponseItems,
)


class SimpleAggregatorService:
    def __init__(self, domain_model):
        self.domain_model = domain_model

    def count_events(self, customer_id, start_timestamp, end_timestamp):
        response = self.domain_model.count_events(
            customer_id=customer_id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )
        ta = TypeAdapter(List[SimpleAggregatorResponseItem])
        m = ta.validate_json(response.to_json(orient="records", date_format="iso"))

        return SimpleAggregatorResponseItems(customer_id=customer_id, data=m)
