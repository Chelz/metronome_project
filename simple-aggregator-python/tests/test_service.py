from typing import List
from unittest.mock import patch

import pandas
import pytest
from pydantic import TypeAdapter

from simple_aggregator_python.domain_model import CountEventsByCustomerIdWithDuckDB
from simple_aggregator_python.schema import SimpleAggregatorResponseItems, SimpleAggregatorResponseItem
from simple_aggregator_python.service import SimpleAggregatorService
import json

@pytest.fixture
def domain_model_return_df():
    df = pandas.DataFrame.from_records([{'num_events': 2, 'hour_bucket': '2021-01-01 00:00:00'}, {'num_events': 2, 'hour_bucket': '2021-01-01 01:00:00'}])
    return df


def test_service(domain_model_return_df):
    with patch.object(CountEventsByCustomerIdWithDuckDB, 'count_events', return_value=domain_model_return_df) as mock_method:
        domain_model = CountEventsByCustomerIdWithDuckDB('', 'events2', False)
        service = SimpleAggregatorService(domain_model)
        res = service.count_events('1', '', '')

        ta = TypeAdapter(List[SimpleAggregatorResponseItem])
        m = ta.validate_json(domain_model_return_df.to_json(orient='records', date_format='iso'))

        expected_response = SimpleAggregatorResponseItems(
            data=m,
            customer_id='1'
        )
        assert expected_response == res