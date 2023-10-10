from dependency_injector import containers, providers

from simple_aggregator_python.domain_model import CountEventsByCustomerIdWithDuckDB
from simple_aggregator_python.service import SimpleAggregatorService


class SimpleAggregatorContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["simple_aggregator_python.routers"]
    )

    config = providers.Configuration(
        yaml_files=["config.yaml"]
    )
    domain_model = providers.Singleton(
        CountEventsByCustomerIdWithDuckDB,
        data_path=config.data_path,
        table_name=config.table_name,
    )
    simple_aggregator_service = providers.Factory(
        SimpleAggregatorService, domain_model=domain_model
    )
