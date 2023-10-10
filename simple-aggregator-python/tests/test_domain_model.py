import pandas as pd
import duckdb
import pytest

from simple_aggregator_python.domain_model import CountEventsByCustomerIdWithDuckDB


@pytest.fixture(scope='session')
def input_pandas_df():
    events = pd.DataFrame.from_dict(
        {
            'customerId': ['1', '1', '2'],
            'eventType': ['INGEST', 'INGEST', 'INGEST'],
            'transactionId': ['101', '102', '103'],
            'eventTime': ['2023-01-01T00:00:00', '2023-01-01T00:15:00', '2023-01-01T01:03:00'],
        },
        # dtype={'eventTime': Datetime, 'customerId': str, 'eventType': str, 'transactionId': str}
    )
    print (events)
    return events

@pytest.fixture(scope='session')
def domain_model(input_pandas_df):
    domain_model = CountEventsByCustomerIdWithDuckDB('', 'events', bootstrap_from_filepath=False)
    duckdb.sql('INSERT INTO events SELECT * from input_pandas_df')
    return domain_model

def _convert_to_list(df):
    return df.to_dict(orient='records')

def test_count_events_with_valid_customer_id(domain_model):
    response = domain_model.count_events(customer_id=1, start_timestamp='2023-01-01 00:00:00', end_timestamp='2023-01-01 00:02:00')
    response_dict = _convert_to_list(response)
    assert len(response_dict) == 1
    assert response_dict[0]['num_events'] == 1

    response = domain_model.count_events(customer_id=1, start_timestamp='2023-01-01 00:00:00', end_timestamp='2023-01-01 01:20:00')
    response_dict = _convert_to_list(response)
    assert len(response_dict) == 1
    assert response_dict[0]['num_events'] == 2


def test_count_events_with_invalid_customer_id(domain_model):
    response = domain_model.count_events(customer_id=5, start_timestamp='2023-01-01 00:00:00', end_timestamp='2023-01-01 00:02:00')
    response_dict = _convert_to_list(response)
    assert len(response_dict) == 0


def test_count_events_with_invalid_date_ranges(domain_model):
    response = domain_model.count_events(customer_id=5, start_timestamp='2023-01-02 00:00:00', end_timestamp='2023-01-02 00:02:00')
    response_dict = _convert_to_list(response)
    assert len(response_dict) == 0
