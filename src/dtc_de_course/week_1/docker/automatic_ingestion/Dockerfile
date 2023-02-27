FROM python:3.9.1

RUN pip install pandas pyarrow sqlalchemy psycopg2-binary

WORKDIR /app
COPY data_ingest.py data_ingest.py

ENTRYPOINT [ "python", "data_ingest.py"]
