# Data Lake
## What is a Data Lake
A data Lake is a __storage repository__ that holds a vast amount of raw data in its native format, coming from many sources,  until it is needed for analytics applications. 

* The main goal is to ingest data as quickly as posible and making it available rapidly and efficiently.

* The data can be __structured__, __semi-structured__ or __unstructured__. 

* Usually, data is assigned __METADATA__ for faster access.

* It needs to be secure, scalable and inexpensive.

## Data Lake vs Data Warehouse

| :material-waves: __Data Lakes__ :material-waves: | :material-warehouse: __Data Warehouses__ :material-warehouse: |
| :---------------: | :--------------------------------------------: |
| Unstructured data, in its raw form.<br> aaa| Structured, transformed data. |
|Used for stream processing, Machine Learning and Real-time Analysis|Used for Batch Processing, BI, Reporting, Data Visualization|
|__ELT__ (Extract, Load, Transform). In this process, the data is extracted from its source for storage in the data lake, and structured only when needed.<br>Useful for large amounts of data.|__ETL__ (Extract, Transform, Load). In this process, data is extracted from its source(s), scrubbed, then structured so it's ready for business-end analysis.<br>Better for smaller amounts of data.|
|Usualy inexpensive and easier to maintain.|More costly and requires more management.|

## Problems of Data Lake
One of the problems is the conversion of a Data Lake into a Data Swamp. It is a collection point for a lot of miscellaneous data that no longer has any sort of structure and the result of poor data management and governance.

When there is no versioning or incompatible schemas for the same data (i.e. The same data in the same route is saved as a _.pickle_ and then as a _.parquet_, making accessing it harder and harder with time and new formats.)

If there is no METADATA, there is a risk of data becoming unusable, be it from not knowing the source, the use cases...

Its effectiveness gets restricted if there is no way to _JOIN_, for the lack of a _KEY_ element or the difference in structure or schema.

## Cloud providers' Data Lakes

| :fontawesome-brands-aws: AWS | :material-google-cloud: GCP  | :material-microsoft-azure: Azure |
| :---------------: | :--------------------------------------------: | :----: |
| S3 | Google Cloud Storage | Azure Blob |