#### Project Summary
The startup Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app

Task: Create a ETL pipeline for a database hosted on Redshift. Load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

#### How to Run
- install the minimum required packages as provided in the `requirements.txt` file
```
pip install -r requirements.txt
```
- set-up Redshift cluster and collect the required parameters as in the file `dwh.cfg`
- create the staging and analytics tables
```python
python3 create_tables.py
```
- insert records in each of the tables
```python
python3 etl.py
```

#### File Explanations
- `create_tables.py`: Create the required staging and analytics tables in the database. Drop the tables at first if they already exists
- `etl.py`: Parse the song and log json data from the `data` folder and insert the records in the appropriate tables
- `dwh.cfg` contains the required parameters for connecting to the Redshift cluster
- `requirements.txt` contains the minimum required python packages
- `check_tables.ipynb` connects with the database in Redshift and simply counts the number of rows in each of the tables

#### Data Source
S3 Link: https://s3.console.aws.amazon.com/s3/buckets/udacity-dend