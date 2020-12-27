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

### Authentication

All endpoints that create and update resources require that an authentication token be passed in the request
header. To acquire an authentication token, you must request one from Auth0 using the FreeFrom Map client id
and secret. (Please post in the freefrom-map-dev Slack channel if you need access to the Auth0 tenant.)
To add the authentication token to your API request, add it to the `Authorization` header in the format
`Bearer <token>`, where "<token>" is replaced with the authentication token.

### States

A state has the following fields:

|       Name        |          Type         |    Notes    |
|-------------------|-----------------------|-------------|
| code              | String                | Primary key (e.g. "NY") |
| name              | String                |             |
| innovative_idea   | String                |             |
| honorable_mention | String                |             |
| grade             | StateGrade            | The most recent grade for the state.      |
| category_grades   | [StateCategoryGrade]  | The most recent grade for each category.  |
| criterion_scores  | [Score]               | The most recent score for each criterion. |
| links             | [Link]                |             |

#### GET /states

This endpoint returns information about all 50 states and DC.

#### GET /states/{code}

This endpoint returns the state corresponding to the state code provided in the request. If no state with that code exists, it will return a 404 response code.

#### PUT /states/{code} (UPCOMING)

This endpoint updates the state corresponding to the state code provided in the request. It requires [authentication](#Authentication)
and accepts a JSON body with the following format:

|       Name        |          Type         |    Notes    |
|-------------------|-----------------------|-------------|
| innovative_idea   | String                | *Optional*. |
| honorable_mention | String                | *Optional*. |

Note that it is not possible to update a state's name or code.

### Categories
A category represents a group of subcategories in the map scorecard. A category has the following fields:

|  Name  |   Type  |    Notes    |
|--------|---------|-------------|
| id     | Integer | Primary key |
| title  | String  |             |
| help_text  | String  |             |
| active | Boolean |             |

#### GET /categories

This endpoint returns a list of all existing categories. It will return an empty array if no categories exist.

#### GET /categories/{id}

This endpoint returns one category corresponding to the id provided in the request. If no category with that
id exists, it will return a 404 response code.

#### POST /categories

This endpoint creates a new category. It requires [authentication](#Authentication). It accepts the following
parameters in the request body as JSON:

|  Name      |   Type  |    Notes    |
|------------|---------|-------------|
| title      | String  | *Optional*. |
| help_text  | String  | *Optional*. |
| active     | Boolean | *Optional*. Defaults to `true`. Passing in `false` will create a deactivated category. A category cannot be reactivated once it has been deactivated. |

#### PUT /categories/{id}

This endpoint updates an existing category. It requires [authentication](#Authentication). It accepts the following
parameters in the request body as JSON:

|  Name      |   Type  |    Notes    |
|------------|---------|-------------|
| title      | String  | *Optional*. |
| help_text  | String  | *Optional*. |
| active     | Boolean | *Optional*. Passing in `false` will deactivate the category. A category cannot be reactivated once it has been deactivated. |

### Subcategories
A subcategory represents a group of criteria in the map scorecard. A category has the following fields:

|  Name           |   Type  |    Notes    |
|-----------------|---------|-------------|
| id              | Integer | Primary key |
| category_id     | Integer |             |
| title           | String  |             |
| help_text       | String  |             |
| active          | Boolean |             |

#### GET /subcategories

This endpoint returns a list of all existing subcategories. It will return an empty array if no subcategories exist.

Accepts an optional query paramater `withCriteria`. If `withCriteria=true` is provided, this will return an array of the subcategories' criteria in the response body.

#### GET /subcategories/{id}

This endpoint returns one subcategory corresponding to the id provided in the request. If no subcategory with that
id exists, it will return a 404 response code.

Accepts an optional query paramater `withCriteria`. If `withCriteria=true` is provided, this will return an array of the subcategory's criteria in the response body.

#### POST /subcategories

This endpoint creates a subcategory. It requires [authentication](#Authentication). It accepts a JSON body with the following format:

|  Name       |   Type  |    Notes                                                         |
|-------------|---------|------------------------------------------------------------------|
| category_id | Integer | *Required*. The category ID to which the subcategory is related. |
| title       | String  | *Optional*.                                                      |
| help_text   | String  | *Optional*.                                                      |
| active      | Boolean | *Optional*. Defaults to `true`. Passing in `false` will create a subcategory that is deactivated. Subcategories cannot be reactivated once they have been deactivated. |

#### PUT /subcategories/{id}

This endpoint changes a subcategory's details. It requires [authentication](#Authentication). It accepts a JSON body with the following format:

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
| help_text           | String   |             |
| active              | Boolean  |             |

#### GET /criteria

This endpoint returns a list of all existing criteria. It will return an empty array if no criteria exist.

#### GET /criteria/{id}

This endpoint returns one criterion corresponding to the id provided in the request. If no criterion with that
id exists, it will return a 404 response code.

#### POST /criteria

This endpoint creates a criterion. It requires [authentication](#Authentication). It accepts a JSON body with the following format:

|  Name                 |   Type  |    Notes                                                         |
|-----------------------|---------|------------------------------------------------------------------|
| subcategory_id        | Integer | *Required*. The subcategory ID to which the criterion is related.|
| title                 | String  | *Optional*.                                                      |
| recommendation_text   | String  | *Optional*.                                                      |
| help_text             | String  | *Optional*.                                                      |
| adverse               | Boolean | *Optional*. Defaults to `false`.                                 |
| active                | Boolean | *Optional*. Defaults to `true`. Passing in `false` will create a criterion that is deactivated. Criteria cannot be reactivated once they have been deactivated. |

#### PUT /criteria/{id}

This endpoint changes a criterion's details. It requires [authentication](#Authentication). It accepts a JSON body with the following format:

|  Name                 |   Type  |    Notes                                                         |
|-----------------------|---------|------------------------------------------------------------------|
| subcategory_id        | Integer | *Optional*. The subcategory ID to which the criterion is related. This cannot be changed, and will return a 400 if it differs from the existing value. |
| title                 | String  | *Optional*.                                                      |
| recommendation_text   | String  | *Optional*.                                                      |
| help_text             | String  | *Optional*.                                                      |
| adverse               | Boolean | *Optional*. Defaults to `false`.                                 |
| active                | Boolean | *Optional*. Passing in `false` will deactivate the criterion. Criteria cannot be reactivated once they have been deactivated. |

### Links

A link represents a web link to an external resource relating to a state and category.

|         Name        |   Type   |    Notes    |
|---------------------|----------|-------------|
| id                  | Integer  | Primary key |
| category_id         | Integer  | Foreign key |
| state_code          | String   | Foreign key |
| text                | String   |             |
| url                 | String   |             |
| active              | Boolean  |             |

#### GET /links

This endpoint returns a list of all existing links. It will return an empty array if no links exist.

#### GET /links/{id}

This endpoint returns one link corresponding to the id provided in the request. If no link with that
id exists, it will return a 404 response code.

#### POST /links

This endpoint creates a link. It requires [authentication](#Authentication). It accepts a JSON body with the following format:

|         Name        |   Type   |    Notes    |
|---------------------|----------|-------------|
| category_id         | Integer  | *Required*. The id of the category to which the subcategory is related. |
| state_code          | String   | *Required*. The state to which the subcategory is related. |
| text                | String   | *Optional*. |
| url                 | String   | *Optional*. |
| active              | Boolean  | *Optional*. Defaults to `true`. Passing in `false` will create a deactivated link. Links cannot be reactivated once they have been deactivated. |

#### PUT /links/{id}

This endpoint changes a link's details. It requires [authentication](#Authentication). It accepts a JSON body with the following format:

|         Name        |   Type   |    Notes    |
|---------------------|----------|-------------|
| category_id         | Integer  | *Optional*. The id of the category to which the subcategory is related. This cannot be changed, and will return a 400 if it differs from the existing value. |
| state_code          | String   | *Optional*. The state to which the subcategory is related. This cannot be changed, and will return a 400 if it differs from the existing value. |
| text                | String   | *Optional*. |
| url                 | String   | *Optional*. |
| active              | Boolean  | *Optional*. Passing in `false` will create a deactivated link. Links cannot be reactivated once they have been deactivated. |

### Scores

A score represents whether a state meets a certain criteria.

| Name            | Type    | Notes                   |
|-----------------|---------|-------------------------|
| id              | Integer | Primary key             |
| state_code      | String  | Foreign key             |
| criterion_id    | Integer | Foreign key             |
| meets_criterion | Boolean |                         |

#### POST /scores

This endpoint creates a new score. Note that scores CANNOT be updated, only overwritten. To overwrite
a score, create a new score for the same state and criterion.

This endpoint requires [authentication](#Authentication). It accepts a JSON body with the following format:

| Name            | Type    | Notes                                                     |
|-----------------|---------|-----------------------------------------------------------|
| state_code      | String  | *Required*. The state code to which the score is related. |
| criterion_id    | Integer | *Required*. The criterion to which the score is related.  |
| meets_criterion | Boolean | *Required*. Whether the state meets the criterion.        |

### Grades

A **state grade** represents the overall grade assigned to a state based on their survivor wealth policies.

|    Name    |  Type   |          Notes          |
|------------|---------|-------------------------|
| id         | Integer | Primary key             |
| state_code | String  | Foreign key             |
| grade      | Integer | One of (-1, 0, 1, 2, 3) |

A **state category grade** represents the grade assigned to a state based on a specific category.

|    Name     |  Type   |          Notes          |
|-------------|---------|-------------------------|
| id          | Integer | Primary key             |
| state_code  | String  | Foreign key             |
| category_id | Integer | Foreign key             |
| grade       | Integer | One of (-1, 0, 1, 2, 3) |

#### GET /grades/{code}

Returns the state's overall grade, and its grades for each category. If no state with that code exists, it will return a 404 response code.

#### POST /grades/{code} (UPCOMING)

This endpoint creates an overall state grade. Note that state grades CANNOT be updated, only overwritten. To overwrite a grade, create a new grade for the same state.

This endpoint requires [authentication](#Authentication). It accepts a JSON body with the following format:

|    Name    |  Type   |          Notes          |
|------------|---------|-------------------------|
| grade      | Integer | *Required*. One of (-1, 0, 1, 2, 3) |

#### POST /grades/{code}/categories/{id} (UPCOMING)

This endpoint creates a state category grade. Note that state category grades CANNOT be updated, only overwritten. To overwrite a grade, create a new grade for the same state and category.

This endpoint requires [authentication](#Authentication). It accepts a JSON body with the following format:

|    Name     |  Type   |          Notes          |
|-------------|---------|-------------------------|
| grade       | Integer | *Required*. One of (-1, 0, 1, 2, 3) |
