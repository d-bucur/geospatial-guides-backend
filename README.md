# Description

This side project is a server for an application in which a user can search for guides for places nearby and
can fake "buy" and "download" them.

The REST interface can be found [here](https://app.swaggerhub.com/apis/sird0d0/guide-server/1.0.0#)

The app is based on a Postgres database with PostGIS extension installed to support geospatial queries.
It is a python Flask app using SQLAlchemy as on ORM and GeoAlchemy2 as an extension to support PostGIS functions.
It also supports Google SSO login from a client app

The app was originally run on Google Cloud so most deployment instructions reference this service.
Of course it can be run on other providers if some specific code in config is changed

# Local run

## Setup python environment
```
virtualenv -p python3 .env
source .env/bin/activate
pip install -r requirements.txt
```

## Database
Setup a Postgres instance (on Cloud SQL) with the PostGIS extension installed.
The schema will be created automatically by SQLAlchemy.
Data can be manually added the the database using the example queries under tools/db

## Database connection
In order to run locally you have to install [CloudSQL Proxy](https://cloud.google.com/sql/docs/postgres/sql-proxy).
This avoids having to whitelist IPs on the DB firewall
```
sudo wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O /etc/cloud_sql_proxy
sudo chmod +x /etc/cloud_sql_proxy
sudo ln -s /etc/cloud_sql_proxy /usr/bin/
```
[Authenticate the SDK](https://cloud.google.com/sql/docs/postgres/sql-proxy#gcloud)
```
gcloud auth login
```
Create proxy through Unix socket
```
cd ~
cloud_sql_proxy -instances=CLOUD_SQL_INSTANCE=tcp:5432
```

## Run

```
python main.py
```

# Deploy
It can be deployed to App Engine using the following command

```
gcloud app deploy .
```

The cloudbuild.yaml can also be used to setup automatic deploys from master branch using Cloud Build

# Test

## Setup
```
pip install -r test-requirements.txt
```

[Install](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community) docker and make
sure it is [runnable](https://docs.docker.com/install/linux/linux-postinstall/) from current user. Docker is used
to run the database in a container during integration tests


## Run
```
pytest
```
Run all tests

```
py.test --cov-report html --cov=. tests
```
Generates coverage report in htmlcov/index.html

## Linter
```
flake8
```

# Notes
The history of the git project has been removed to protect sensitive info