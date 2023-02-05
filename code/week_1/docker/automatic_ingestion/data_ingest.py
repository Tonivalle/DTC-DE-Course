import argparse
import logging
import os
from typing import Dict

import pandas
import pyarrow.parquet as parquet  # type: ignore
from sqlalchemy import Engine, engine

logging.basicConfig(format="%(asctime)s - %(levelname)s: %(message)s")


def pipeline():

    logging.info("Starting data ingestion...")
    params = _parse_params()

    data_file = _download_data(params)
    df = _generate_df(data_file)
    engine = _create_engine(params)

    logging.info("Writing data to Database...")
    _write_to_table(df, engine)

    logging.info("Removing raw data file...")
    _remove_raw_data_file(data_file)
    logging.info("All done!")


def _parse_params() -> Dict:
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--user", required=True, help="user name for postgres")
    parser.add_argument("--password", required=True, help="password for postgres")
    parser.add_argument("--host", required=True, help="host for postgres")
    parser.add_argument("--port", required=True, help="port for postgres")
    parser.add_argument("--db", required=True, help="database name for postgres")
    parser.add_argument("--url", required=True, help="url of the csv file")
    parser.add_argument(
        "--table_name",
        required=True,
        help="name of the table where we will write the results to",
    )
    return vars(parser.parse_args())


def _download_data(params: Dict) -> str:
    os.system(f"curl -O -L {params['url']}")
    file_name = params["url"].split("/")[-1]
    return f"./{file_name}"


def _generate_df(data_file: str) -> pandas.DataFrame:
    data = parquet.read_table(data_file)
    return data.to_pandas()


def _create_engine(params: Dict) -> Engine:
    return engine.create_engine(
        f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['db']}"
    )


def _write_to_table(df: pandas.DataFrame, engine):
    df.to_sql(
        name="yellow_taxi_data", con=engine, if_exists="replace", chunksize=100_000
    )


def _remove_raw_data_file(data_file: str):
    os.remove(data_file)


if __name__ == "__main__":
    pipeline()
