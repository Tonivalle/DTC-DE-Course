from datetime import timedelta
from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket


@flow
def etl_multiple_dates(
    months: list[int] = [1, 2],
    year: int = 2022,
    color: str = "yellow",
):  # pylint: disable=dangerous-default-value
    for month in months:
        etl_web_to_gcs(month=month, year=year, color=color)


@flow()
def etl_web_to_gcs(month: int, year: int, color: str) -> None:
    """Main ETL Function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}.parquet"
    dataset_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_file}"

    dataset = get_data(dataset_url)
    data_file_path = write_local(df=dataset, color=color, dataset_file=dataset_file)  # type: ignore
    write_gcs(path=data_file_path)


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(weeks=1))
def get_data(url: str) -> pd.DataFrame:
    data = pd.read_parquet(url)
    return data


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{color}/{dataset_file}")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, compression="gzip")
    return path


@task
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("dte-bucket-block")
    gcs_block.upload_from_path(from_path=path, to_path=path)


if __name__ == "__main__":
    etl_multiple_dates()
