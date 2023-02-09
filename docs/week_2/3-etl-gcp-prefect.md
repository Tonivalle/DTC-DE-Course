# ETL with GCP & Prefect

## Introduction

We are going to create an ETL pipeline to automatically ingest our data into Google Cloud Storage.

We need to already have the __infrastructure up__ to perform the operations.

## GCS Bucket

We start the prefect UI with `prefect orion start`. Here, we can create a `GCS Bucket` block. before we create we register the kind of block by:
```properties
prefect block register -m prefect_gcp
```

### GCP credentials block

To use the service account we generated in *week_1* we can use a `GCP Credentials Block` to store the credential info.

![credentials-block](./images/credentials-block.png)

### CGS Bucket block

We can put the credentials block we just created in a GCS Bucket block:

![bucket-block](./images/bucket-block.png)

### Coding the pipeline

Now we can put these blocks into our code! We will refactor the pipeline to use these classes. Right now we arent transforming the data after ingestion, but in the future we can add functions before the loading!

```python
from datetime import timedelta
from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket


@flow()
def etl_web_to_gcs() -> None:
    """Main ETL Function"""
    COLOR = "yellow"
    YEAR = 2022
    MONTH = 1

    dataset_file = f"{COLOR}_tripdata_{YEAR}-{MONTH:02}.parquet"
    dataset_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_file}"

    dataset = get_data(dataset_url)
    data_file_path = write_local(df=dataset, color=COLOR, dataset_file=dataset_file)
    write_gcs(path=data_file_path)


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(weeks=1))
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
    etl_web_to_gcs()
```