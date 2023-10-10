# Simple Aggregator Service
Simple FastAPI service that exposes an endpoint `/events/{customer_id}` to fetch the count of events in hour buckets between start_timestamp and end_timestamp


## Assumptions
### Goals
1. Calculate the count of events for a customer id in hour buckets and a http service to surface the answers. 
2. Only READ APIs are provided and No write APIs are supported. The backend is bootstrapped with the events in csv files.

### Non Goals
Generally out of order data, late data needs to be handled in a streaming world with checkpointing and watermarking solutions but given that the input is batch based and no write apis are supported, they are out of scope.

## Solution
### Considerations
#### DuckDB as a backend
Given that the usecase is Analytical in workload, an OLAP database would suit us. Looking at possible solutions, I chose duckdb which is an inprocess OLAP database that performs efficient aggregations. 

##### Alternatives
Other similar solutions would be 
1. polars, pandas, 
2. sqllite database
3. Writing the count logic from scratch with dicts

Using duckdb was simple, and scales to increased workloads. Arguably polars would also perform well and performance [benchmarks](https://www.pola.rs/benchmarks.html) showed that duckdb is equivalent. 
3. might not scale to increased workloads. duckdb-engine provides a interface similar to SqlAlchemy but it was a bit overkill just to surface the read endpoints.

## Running the service
The duckdb OLAP database is bootstrapped with any data in `simple-aggregator-python/data/*.csv` during startup. You can add the events in csv format (as one or multiple files) in the path mentioned 
```
# config.yaml
data_path: 'data/*.csv'
```

if you just want to run the service
```
make start-service
```

### Endpoints
/events/{customerID}?start_timestamp=YYYY-mm-DD HH:MM:SS&end_timestamp=YYYY-mm-DD HH:MM:SS
note the date format

#### Sample request:
1. Go to following link/browser - http://0.0.0.0:8000/events/b4f9279a0196e40632e947dd1a88e857?start_timestamp=2021-03-01%2000:00:00&end_timestamp=2021-03-01%2010:00:00
2. submitting a curl request 


### Pseudocode
At a very high level, the duckdb query truncates the timestamp to hour and groups by customer_id, filters between the arbitary timestamps. 
```
        SELECT date_trunc( 'hour', eventTime) as hour_bucket,
        count(eventType) as num_events
    
        FROM
        {table_name}
    
        WHERE
        customerId IN ('{input_customer_id}') AND
        eventTime >= strptime('{event_start_time}', '%Y-%m-%d %H:%M:%S')  AND 
        eventTime <= strptime('{event_end_time}', '%Y-%m-%d %H:%M:%S')
    
        GROUP BY 
        customerId,
        date_trunc( 'hour', eventTime)
    
        ORDER BY date_trunc( 'hour', eventTime)
```

### Code Structure

```
simple-aggregator-python
├── simple_aggregator_python
│   ├── __init__.py
│   ├── app.py -> FastAPI application
│   ├── containers.py -> contains the dependency injector components
│   ├── domain_model.py -> Follows DDD to define the business logic (basically the duckdb based business logic
│   ├── routers.py -> Router file that contains read endpoints
│   ├── schema.py -> Pydantic request and response schema definitions
│   ├── service.py -> follows service pattern to decouple the application and service related bits. here it just does some bookkeeping and calls the domain model
├── tests
│   └── __init__.py
│   └── test_domain_model.py -> tests the business logic
│   └── test_e2e.py -> uses FastAPI testclient to test the api end to end
│   └── test_service.py -> tests the service layer by mocking the calls to and from business logic
├── poetry.lock
├── pyproject.toml
├── README.md
├── config.yaml -> configuration 
```

## Testing
Testing was done with pytest

```
(simple-aggregator-python-py3.10) chellamsrinivasansayiram@Chellams-MacBook-Pro simple-aggregator-python % pytest tests
============================================================================= test session starts ==============================================================================
platform darwin -- Python 3.10.13, pytest-6.2.5, py-1.11.0, pluggy-1.3.0
rootdir: /Users/chellamsrinivasansayiram/projects/metronome_project/simple-aggregator-python
plugins: mock-3.11.1, anyio-3.7.1
collected 7 items                                                                                                                                                              

tests/test_domain_model.py ...                                                                                                                                           [ 42%]
tests/test_e2e.py ...                                                                                                                                                    [ 85%]
tests/test_service.py .                                                                                                                                                  [100%]

=============================================================================== warnings summary ===============================================================================
../../../.pyenv/versions/3.10.13/lib/python3.10/inspect.py:469
  /Users/chellamsrinivasansayiram/.pyenv/versions/3.10.13/lib/python3.10/inspect.py:469: PydanticDeprecatedSince20: The `__fields__` attribute is deprecated, use `model_fields` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.4/migration/
    value = getattr(object, key)

../../../Library/Caches/pypoetry/virtualenvs/simple-aggregator-python-mvavQuZt-py3.10/lib/python3.10/site-packages/pydantic/_internal/_model_construction.py:249
  /Users/chellamsrinivasansayiram/Library/Caches/pypoetry/virtualenvs/simple-aggregator-python-mvavQuZt-py3.10/lib/python3.10/site-packages/pydantic/_internal/_model_construction.py:249: PydanticDeprecatedSince20: The `__fields__` attribute is deprecated, use `model_fields` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.4/migration/
    warnings.warn('The `__fields__` attribute is deprecated, use `model_fields` instead.', DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/warnings.html
======================================================================== 7 passed, 2 warnings in 0.70s =========================================================================
(simple-aggregator-python-py3.10) chellamsrinivasansayiram@Chellams-MacBook-Pro simple-aggregator-python % 

```

