import psycopg2
import utils
import json

config = utils.get_config()

PG_HOST=config['postgre']['host']
PG_USER=config['postgre']['user']
PG_DB=config['postgre']['database']
PG_PWD=config['postgre']['password']
CONN_STRING='host={host} dbname={db} user={user} password={pwd}'.format(host=PG_HOST,
    db=PG_DB, user=PG_USER, pwd=PG_PWD)


def copy_file(sql, filename, mode='w'):

    with psycopg2.connect(CONN_STRING) as conn:
        with conn.cursor() as cur:
            with open(filename, mode) as file:
                cur.copy_expert(sql, file)

def run_query(sql):

    with psycopg2.connect(CONN_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

#copy_to_file("COPY (SELECT * FROM cyclones where dt = '2015-01-01') TO STDOUT WITH CSV DELIMITER ';'", "./mafile")

#copy_file("COPY cyclones_stage FROM STDIN DELIMITER ';' CSV HEADER", './csv_dir/cyclones_20151111.csv', 'r')

#run_query('truncate table cyclones_stage')
