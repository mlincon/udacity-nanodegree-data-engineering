import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

import logging
logging.basicConfig(level=logging.DEBUG)

def load_staging_tables(cur, conn):
    """
    Load the JSON files from S3 to the specified Redshift cluster.

    :param cur: database cursor object
    :param conn: connection string to Redshift cluster
    """
    for query in copy_table_queries:
        logging.info(f'Executing query:\n {query}')
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Insert into fact and dimensional table from the staging tables

    :param cur: database cursor object
    :param conn: connection string to Redshift cluster
    """
    for query in insert_table_queries:
        logging.info(f'Executing query:\n {query}')
        cur.execute(query)
        conn.commit()


def main():
    """
    Parse the config file to get the required credentials for connecting with Redshift.
    Insert data into staging, fact and dimensional tables.
    """

    logging.info('Parsing config file for connection details')
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    logging.info('Attempting to connect to Redshift cluster')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    logging.info('Cursor obtained')

    logging.info('Copying data from S3 to Redshift in staging tables')
    load_staging_tables(cur, conn)

    logging.info('Inserting data in fact and dimension tables from staging')
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()