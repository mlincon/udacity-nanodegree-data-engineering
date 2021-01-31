## Project Summary
The startup Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app

Task: To define fact and dimension tables for a star schema for a particular analytic focus, and to write an ETL pipeline that transfers data from files in two local directories into these tables in database.

## How to Run
To create tables, run
```python
python3 create_tables.py
```

To insert records in the table
```python
python3 etl.py
```

## File Explanations
- `data`: Folder containing the song and log data in json format
- `create_tables.py`: Create the required tables in the database. Drop the tables at first if they already exists
- `etl.py`: Parse the song and log json data from the `data` folder and insert the records in the appropriate tables

Additionally, there are two notebooks for testing purpose:
- `etl.ipynb`
- `test.ipynb`

## Miscellaneous
---
#### Roles and Password in PostgreSQL

##### Role
- The default role/username is `postgres`
- To create a new rolw
    - Change to postgres account:  `sudo -i -u postgres`
    - Issue the `createuser --interactive` command
```
user-pc$           sudo -i -u postgres
postgres@user-pc$  createuser --interactive
```
- Then enter a user/role name and answer the prompts
##### Change password
- You can set up a new password
    - Change to postgres account:  `sudo -i -u postgres`
    - Access the Postgres prompt:  `psql`
    - Issue the `\password <username>` command
```
user-pc$           sudo -i -u postgres
postgres@user-pc$  psql
postgres=#$        \password <username>
```
- Then enter new password
- If no username is provided, then the default `postgres` role will be used

##### Create and delete DB
- From the `postgres` account use the command `createdb <db>` and `delete <db>` respectively
- From `psql` cli, use `CREATE DATABASE <db>;` and `DROP DATABASE <db>;` respectively
- Within `psql` use
    - `\list` or `\l` to list all databases
    - `\connect` or `\c` to switch database
    - `dt` to list all tables in a database
---
#### Setting up local DB instance via Docker

##### Get PostgreSQL
- Get the latest [image](https://hub.docker.com/_/postgres) of PostgreSQL:
`docker image pull postgres:latest`
- Create a container and specify the user and password alongside:
```
docker run -d \
    -n postgres \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=pass \
    postgres:latest
```
- Get the host address
`docker inspect postgres | grep "IPAddress"`
 e.g. as part of the default bridge network it can be `172.17.0.2`

##### Get pgAdmin4
- Get the latest [image](https://hub.docker.com/r/dpage/pgadmin4/) of pgAdmin4
`docker image pull dpage/pgadmin4`
- Create a container
```
docker run -p 85:80 \
    -n pgadmin \
    -e 'PGADMIN_DEFAULT_EMAIL=user@user.com' \
    -e 'PGADMIN_DEFAULT_PASSWORD=pass' \
    -d dpage/pgadmin4
```
- Go to `localhost:85` to start pgAdmin4
- Connect to the database created above, e.g.
```
host: 172.12.0.2
port: 5432
user: user
pass: pass
```

#### SQL from Jupyter Notebook
- Install the `ipython-sql` library:
`pip install ipython-sql`
- Other required libraries: `psycopg2` or `psycopg2-binary`
    - if the first one fails, install the second (binary) one
