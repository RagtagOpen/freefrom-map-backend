# FreeFrom Map Backend

## Overview

Welcome to the FreeFrom Map project backend! This page is under construction so expect more information soon.

## Local Development Setup

This is a Python Flask app. Follow these steps to run it locally:

### Install Python

If you don't already have it installed, install Python 3. You can check that you have it installed using this command:

```
python3 --version
```

This should return something like `Python 3.7.3`.

### Install Postgres

Install and run a PostgreSQL on your computer.

### Set up database roles

1. Start a Postgres client session: `psql`
2. Create a new user: `create user "freefrom_map_user";`
3. Create a database: `create database "freefrom_map_dev";`
4. Give the user permissions on your database: `grant all privileges on database freefrom_map_dev to freefrom_map_user;`
5. Quit psql: `\q`

### Set up environment variables

Use the provided template to set up a .env file with some environment variables you'll need:

```
cp .env.template .env
```

`.env` is included in the `.gitignore` for this repo and won't be included when you commit your changes.

### Start the virtual environment (aka venv)

We use [venv](https://docs.python.org/3/library/venv.html) to ensure that every developer is using the same dependency versions.

```
python3 -m venv env
source env/bin/activate
```

Now, when you run `which python`, you should get something like: `/path/to/your/repo/env/bin/python`. You can deactivate the venv at any time by running `deactivate`.

You only have to run `python3 -m venv env` once, but you should run `source env/bin/activate` every time you work on this repository.

### Install the requirements

```
pip3 install -r requirements.txt
```

### Migrate the database

```
python manage.py db migrate
python manage.py db upgrade
```

## Running the application

Run the application with the following command:

```
python3 manage.py runserver
```

Then, in your browser, navigate to `localhost:5000/`. You should see the message "Hello world!" on your screen.

## Running tests

Run tests with the following command:

```
python3 -m unittest
```

## Deploying the application

Deployment will require the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), and access to the `freefrom-map-api` app on Heroku (ask in #proj-freefrom-map-dev). 

From the command line, log in to your Heroku account:

```
heroku login
```

Add a remote to the `freefrom-map-api` Heroku app to your local repository: 

```
heroku git:remote -a freefrom-map-api
```

If any of the changes require new environment variables, they can be set with the command:

```
heroku config:set VARIABLE=value
```

To push your local changes to Heroku, this command will deploy the latest committed version of your branch to `heroku/main`:

```
git push heroku main
```

If your changes have any migrations, migrate the remote database:

```
heroku run python manage.py db upgrade
```

## API Reference
The following section describes the FreeFrom map backend API. All responses will be formatted as JSON, and all
request bodies should be provided as JSON.

### Categories
A category represents a group of criteria in the map scorecard. A category has the following fields:

|  Name  |   Type  |    Notes    |
|--------|---------|-------------|
| id     | Integer | Primary key |
| title  | String  |             |
| active | Boolean |             |

#### GET /categories

This endpoint returns a list of all existing categories. It will return an empty array if no categories exist.

#### GET /categories/<id>

This endpoint returns one category corresponding to the id provided in the request. If no category with that
id exists, it will return a 404 response code.

### Criteria

A criterion represents one measure in the state scorecard to determine whether a state has strong survivor wealth policies.

|         Name        |   Type   |    Notes    |
|---------------------|----------|-------------|
| id                  | Integer  | Primary key |
| category_id         | Integer  | Foreign key |
| title               | String   |             |
| recommendation_text | String   |             |
| active              | Boolean  |             |

### GET /criteria

This endpoint returns a list of all existing criteria. It will return an empty array if no criteria exist.

### GET /criteria/<id>

This endpoint returns one criterion corresponding to the id provided in the request. If no criterion with that
id exists, it will return a 404 response code.
