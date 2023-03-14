# Data Visualization

## Using Google Looker Studio

Google Looker Studio (formerly Google Data Studio) allows us to easily explore BigQuery data. The url is [this one](https://lookerstudio.google.com/).

!!! info
    Google Looker studio allows to connect to a postgres, MySQL... database, but you need to have it visible (you need to pass the IP and port for the configuration).

Clicking on Create and then on Data Source will allow us to link up BigQuery to it. Navigate to BigQuery and then input your project and dataset information.

On that is done we can `Create a Report` to explore the data. In here, if we want to filter the data, we can use [Controls](https://support.google.com/looker-studio/answer/6312144?hl=en#zippy=%2Cin-this-article), that let us specify ranges, use sliders, dropdowns... or separate series by using the `Breakdown dimension` parameter.

More comprehensive tutorial in [here](https://www.youtube.com/watch?v=39nLTs74A3E&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=39).

![dashboard](https://www.benlcollins.com/wp-content/uploads/2016/07/mobile_dashboard.gif)

## Using Metabase on local

If you are using a postgres environment on your local machine you can also use the open-source edition of [Metabase](https://www.metabase.com/docs/latest/installation-and-operation/installing-metabase) to visualize the deta and create the reports.

The prefered way is to use a docker container that contains Metabase and is on the same network as your postgres database.

Tutorial is in [here](https://www.youtube.com/watch?v=BnLkrA7a6gM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=41).

![metabase](https://www.metabase.com/images/stats-dashboard.svg)