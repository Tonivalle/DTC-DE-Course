# Automatic Ingestion

## Automating the pipeline

We are going to refactor the code to automate the ingestion of data into the database.

The command to test the pipeline is:
```properties
python ./src/dtc_de_course/week_1/docker/automatic_ingestion/data_ingest.py  \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet
```

We create the image for the container using the following command and docker file:

=== "Console"

    ```properties
    docker build -t taxi_ingest:v0.0.1 ./src/dtc_de_course/week_1/docker/automatic_ingestion
    ```

=== "Dockerfile"

    ```Dockerfile
    FROM python:3.9.1

    RUN pip install pandas pyarrow sqlalchemy psycopg2-binary

    WORKDIR /app
    COPY data_ingest.py data_ingest.py

    ENTRYPOINT [ "python", "data_ingest.py"]

    ```

This allows us to run this container with the following command:

```properties hl_lines="1 4"
docker run -it --network=pg-network taxi_ingest:v0.0.1 \
  --user=root\
  --password=root \
  --host=pg-database \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet
```

!!! warning
    Be careful to add the network (so the containers can see each other) and change the `--host` to `pg-database` since the hostname of the container is not `localhost` (our computer) anymore but `pg-database`.
