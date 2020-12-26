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

While .env.template contains some non-sensitive environment variables, there are a few that you'll
need to get from the team. Ask in the #proj-freefrom-map-dev channel for these variables.

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
python3 manage.py db migrate
python3 manage.py db upgrade
```

If you receive a "Target database is not up to date." error, try `python3 manage.py db stamp head`

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

## Linting

Before merging your code, check that it passes the linter (PEP8 style):

```
flake8
```

## API Reference
The following section describes the FreeFrom map backend API. All responses will be formatted as JSON, and all
request bodies should be provided as JSON.

### States

A state has the following fields:

|       Name        |          Type         |    Notes    |
|-------------------|-----------------------|-------------|
| code              | String                | Primary key |
| name              | String                |             |
| innovative_idea   | String                |             |
| honorable_mention | String                |             |
| grade             | StateGrade            | The most recent grade for the state.      |
| category_grades   | [StateCategoryGrade]  | The most recent grade for each category.  |
| criterion_scores  | [Score]               | The most recent score for each criterion. |
| links             | [Link]                |             |

#### GET /states/{code}

This endpoint returns the state corresponding to the state code provided in the request. If no state with that code exists, it will return a 404 response code.

### Categories
A category represents a group of subcategories in the map scorecard. A category has the following fields:

|  Name  |   Type  |    Notes    |
|--------|---------|-------------|
| id     | Integer | Primary key |
| title  | String  |             |
| active | Boolean |             |

#### GET /categories

This endpoint returns a list of all existing categories. It will return an empty array if no categories exist.

#### GET /categories/{id}

This endpoint returns one category corresponding to the id provided in the request. If no category with that
id exists, it will return a 404 response code.

### Subcategories
A subcategory represents a group of criteria in the map scorecard. A category has the following fields:

|  Name       |   Type  |    Notes    |
|-------------|---------|-------------|
| id          | Integer | Primary key |
| category_id | Integer |             |
| title       | String  |             |
| active      | Boolean |             |

#### GET /subcategories

This endpoint returns a list of all existing subcategories. It will return an empty array if no subcategories exist.

Accepts an optional query paramater `withCriteria`. If `withCriteria=true` is provided, this will return an array of the subcategories' criteria in the response body. 

#### GET /subcategories/{id}

This endpoint returns one subcategory corresponding to the id provided in the request. If no subcategory with that
id exists, it will return a 404 response code.

Accepts an optional query paramater `withCriteria`. If `withCriteria=true` is provided, this will return an array of the subcategory's criteria in the response body. 

#### POST /subcategories

This endpoint creates a subcategory. It accepts a JSON body with the following format:

|  Name       |   Type  |    Notes                                                         |
|-------------|---------|------------------------------------------------------------------|
| category_id | Integer | *Required*. The category ID to which the subcategory is related. |
| title       | String  | *Optional*.                                                      |
| help_text   | String  | *Optional*.                                                      |
| active      | Boolean | *Optional*. Defaults to `true`.                                  |

#### PUT /subcategories/{id}

This endpoint changes a subcategory's details. It accepts a JSON body with the following format:

|  Name       |   Type  |    Notes                                                         |
|-------------|---------|------------------------------------------------------------------|
| category_id | Integer | *Optional*. The category ID to which the subcategory is related. This cannot be changed, and will return a 400 if it differs from the existing value. |
| title       | String  | *Optional*.                                                      |
| help_text   | String  | *Optional*.                                                      |
| active      | Boolean | *Optional*. Once a subcategory is deactivated, it cannot be reactivated. |

### Criteria

A criterion represents one measure in the state scorecard to determine whether a state has strong survivor wealth policies.

|         Name        |   Type   |    Notes    |
|---------------------|----------|-------------|
| id                  | Integer  | Primary key |
| subcategory_id      | Integer  | Foreign key |
| title               | String   |             |
| recommendation_text | String   |             |
| active              | Boolean  |             |

#### GET /criteria

This endpoint returns a list of all existing criteria. It will return an empty array if no criteria exist.

#### GET /criteria/{id}

This endpoint returns one criterion corresponding to the id provided in the request. If no criterion with that
id exists, it will return a 404 response code.

### Grades

A **state grade** represents the overall grade assigned to a state based on their survivor wealth policies.

|    Name    |  Type   |          Notes          |
|------------|---------|-------------------------|
| id         | Integer | Primary key             |
| state_code | String  |                         |
| grade      | Integer | One of (-1, 0, 1, 2, 3) |

A **state category grade** represents the grade assigned to a state based on a specific category.

|    Name     |  Type   |          Notes          |
|-------------|---------|-------------------------|
| id          | Integer | Primary key             |
| state_code  | String  |                         |
| category_id | Integer |                         |
| grade       | Integer | One of (-1, 0, 1, 2, 3) |

#### GET /grades/{code}

Returns the state's overall grade, and its grades for each category. If no state with that code exists, it will return a 404 response code.
