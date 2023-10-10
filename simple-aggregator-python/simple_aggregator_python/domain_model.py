import logging
from abc import ABC, abstractmethod

import duckdb

logger = logging.getLogger("simple-aggregator-logger")


class CountEventsByCustomerId(ABC):
    @abstractmethod
    def count_events(self, *args, **kwargs):
        raise NotImplementedError


class CountEventsByCustomerIdWithDuckDB(CountEventsByCustomerId):
    def __init__(self, data_path, table_name, bootstrap_from_filepath=True):
        self.data_path = data_path
        self.table_name = table_name
        logger.info(f"Table Name: {self.table_name}, Data Path: {self.data_path}")

        create_table_sql_stmt = f"""
        CREATE TABLE {self.table_name}(customerId VARCHAR, eventType VARCHAR, transactionId VARCHAR, eventTime TIMESTAMP);
        """
        self.run_sql_statement(create_table_sql_stmt)

        if bootstrap_from_filepath:
            self.create_table_from_file_path()

    def create_table_from_file_path(self):
        bootstrap_data = f"""
        COPY {self.table_name} FROM '{self.data_path}' (AUTO_DETECT true);
        """
        self.run_sql_statement(bootstrap_data)

    def run_sql_statement(cls, sql_stmt):
        return duckdb.sql(sql_stmt)

    def count_events(self, customer_id, start_timestamp, end_timestamp):
        group_by_statement = """
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
        """
        _groupby_statement = group_by_statement.format(
            table_name=self.table_name,
            input_customer_id=customer_id,
            event_start_time=start_timestamp,
            event_end_time=end_timestamp,
        )
        logger.info(f"Running the following query: {_groupby_statement}")
        response = self.run_sql_statement(_groupby_statement).df()
        return response
