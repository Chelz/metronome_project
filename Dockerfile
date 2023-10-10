FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    net-tools

WORKDIR /app

COPY simple-aggregator-python .

COPY simple-aggregator-python/data/events.csv .

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "simple_aggregator_python.app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
