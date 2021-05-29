import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

import logging
logging.basicConfig(level=logging.DEBUG)

def drop_tables(cur, conn):
    """
    Before (re-)creating tables, drop the existing ones and start anew.

    :param cur: database cursor object
    :param conn: connection string to Redshift cluster
    """
    for query in drop_table_queries:
        logging.info(f'Executing query:\n {query}')
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Given the provided destination, create tables based on predefined sql instructions.

    :param cur: database cursor object
    :param conn: connection string to Redshift cluster
    """
    for query in create_table_queries:
        logging.info(f'Executing query:\n {query}')
        cur.execute(query)
        conn.commit()


def main():
    """
    Parse the config file to get the required credentials for connecting with Redshift.
    Drop any existing tables and then (re-)create the required tables.
    """

    logging.info('Parsing config file for connection details')
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    logging.info('Attempting to connect to Redshift cluster')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    logging.info('Cursor obtained')

    logging.info('Dropping any pre-existing tables')
    drop_tables(cur, conn)

    logging.info('Creating new tables')
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()