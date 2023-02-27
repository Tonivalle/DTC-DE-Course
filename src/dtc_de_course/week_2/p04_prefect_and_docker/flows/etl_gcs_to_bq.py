from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query"""
    COLOR = "yellow"
    YEAR = 2022
    MONTH = 1

    path = extract_from_gcs(COLOR, YEAR, MONTH)
    df = transform_data(path)
    write_to_bq(df)


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Extract data from GCS"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}.parquet"
    gcs_path = Path(f"data/{color}/{dataset_file}")

    local_data_path = Path(__file__).parents[3]
    gcs_block = GcsBucket.load("dte-bucket-block")
    gcs_block.get_directory(from_path=gcs_path, local_path=local_data_path)
    return local_data_path / "data" / color / dataset_file


@task(log_prints=True)
def transform_data(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df["passenger_count"].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df


@task
def write_to_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("dte-gcp-credential")

    df.to_gbq(
        destination_table="trips_data_all.rides",
        project_id="vast-bounty-142716",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


if __name__ == "__main__":
    etl_gcs_to_bq()
