import psycopg2
import json

import utils

config = utils.get_config()

PG_HOST=config['postgre']['host']
PG_USER=config['postgre']['user']
PG_DB=config['postgre']['database']
PG_PWD=config['postgre']['password']
CONN_STRING='host={host} dbname={db} user={user} password={pwd}'.format(host=PG_HOST,
    db=PG_DB, user=PG_USER, pwd=PG_PWD)


def copy_file(sql, filename, mode='w'):
    '''Copies data from/to db table from/to file
        mode -- w - write from db to file, r - write from file to db
    '''
    with psycopg2.connect(CONN_STRING) as conn:
        with conn.cursor() as cur:
            with open(filename, mode) as file:
                cur.copy_expert(sql, file)

def run_query(sql):
    '''Runs sql query'''
    with psycopg2.connect(CONN_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

