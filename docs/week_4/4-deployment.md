# Model Deployment

## What is deployment

Process of running the models we created in our development environment in a production environment.

Development and later deployment allows us to continue building models and testing them without affecting our production environment.

A deployment environment will normally have a different schema in our data warehouse and ideally a different user.

A development - deployment workflow will be something like: 

* Develop in a user branch
* Open a PR to merge into the main branch 
* Merge the branch to the main branch
* Run the new models in the production environment using the main branch 
* Schedule the models

Another important part of deployment is the practice of regularly merging development branches into a central repository, after which automated builds and tests are run. The goal is to reduce adding bugs to the production code and maintain a more stable project. 

dbt allows us to enable CI on pull requests, enabled via webhooks from GitHub. No PR will be able to be merged unless the run has been completed successfully.


## dbt Cloud

It has integration with dbt out of the box and allows us to schedule and run jobs, have live documentation, logs...

We will create a new environment called `Production`. On the configuration we can set a curstom branch to be used for this environmeent, but by default it is the main branch for Deployment Environments.

Once created, we can go to jobs and create one to run the project, schedule it...

## On local

We can instead build to a local server by creating or modifying the `~/.dbt/profiles.yml` which is a global config file for our user. In there we can specify the environments:

```yaml
dbt_project:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: user
      password: password
      port: 5432
      dbname: test_db
      schema: public
      threads: 1
      connect_timeout: 30
    prod:
      type: postgres
      host: localhost
      user: admin
      password: root
      port: 5432
      dbname: production
      schema: master
      threads: 1
      connect_timeout: 30
```
The `target` parameter specifies the default environment when not passing one.