import argparse
import os
from datetime import timedelta
from typing import Dict, Tuple

import pandas
import pyarrow.parquet as parquet
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector


@flow(name="Ingestion Flow")
def pipeline():

    params = _parse_params()

    df, data_file_route = _get_and_format_data(params)

    _write_to_table(df)

    _remove_raw_data_file(data_file_route)


@task(
    name="Parsing parameters",
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(weeks=1),
)
def _parse_params() -> Dict:

    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--url", required=True, help="url of the csv file")
    parser.add_argument(
        "--table_name",
        required=True,
        help="name of the table where we will write the results to",
    )
    return vars(parser.parse_args())


@task(
    name="Obtain data",
    retries=3,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(weeks=1),
)
def _get_and_format_data(params: Dict) -> Tuple[pandas.DataFrame, str]:
    data_file_route = _download_data(params)
    df = _generate_df(data_file_route)
    return df, data_file_route


def _download_data(params: Dict) -> str:
    os.system(f"curl -O -L {params['url']}")
    file_name = params["url"].split("/")[-1]
    return f"./{file_name}"


def _generate_df(data_file_route: str) -> pandas.DataFrame:
    data = parquet.read_table(data_file_route)
    return data.to_pandas()


@task(name="Write to SQL")
def _write_to_table(df: pandas.DataFrame):
    connection_block = SqlAlchemyConnector.load("postgres-connector")
    with connection_block.get_connection(begin=False) as engine:
        df.to_sql(
            name="yellow_taxi_data", con=engine, if_exists="replace", chunksize=100_000
        )


@task(name="Cleanup")
def _remove_raw_data_file(data_file: str):
    os.remove(data_file)


if __name__ == "__main__":
    pipeline()
