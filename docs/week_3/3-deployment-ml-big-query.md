# BigQuery Machine Learning Deployment

We may want to export the ML model that we created using Big Query and deploy it in a docker container.
The steps to do this are:

1. We authenticate and export the model to Google Storage.
```properties
gcloud auth login
bq --project_id vast-bounty-142716 \
    extract -m trips_data_all.tip_model \
    gs://taxi_ml_model/tip_model
```
2. We copy the model from Google storage to our local machine.
```properties
mkdir /tmp/model
gsutil cp -r gs://taxi_ml_model/tip_model /tmp/model
```
3. We move the model to the folder we will mount to the container. (This can be done in the same step as the one above) The 1 is the version of the model, which will be used later during the requests. 
```properties
mkdir -p serving_dir/tip_model/1
cp -r /tmp/model/tip_model/* serving_dir/tip_model/1
```

4. Using tensorflow's serving image we generate a container with the folder containing the model mounted.
```properties
docker pull tensorflow/serving
docker run -p 8501:8501 --mount type=bind,source=pwd/serving_dir/tip_model,target=/models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &
```

5. We can perform a POST request to the model to get a prediction with curl, Postman... on the model url, the v1 comes from the `1` subfolder created during step 3.
```properties
curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1/models/tip_model:predict
```
6. We can check 
```properties
http://localhost:8501/v1/models/tip_model
```