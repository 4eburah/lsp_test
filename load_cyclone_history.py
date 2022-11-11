import os
import argparse
import datetime

import utils
import postgre

def validate_cli_options(options):
    '''Validates command line options'''
    assert options.file is not None, \
        'Please provide file to load via -file argument'

    if not os.path.isfile(options.file):
        print(f'no such file {options.file}')
        exit()

    if os.stat(options.file).st_size == 0:
        print(f'file {options.file} is empty')
        exit()


def get_cli_options():
    '''Returns command line options'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', help = 'file with day of cyclones data')
    options = parser.parse_args()
    validate_cli_options(options)
    return options


def load_file_to_stage(filename):
    return

options = get_cli_options()
config = utils.get_config()

print(f'processing {options.file}')

# load file to stage table

trunc_sql = 'truncate table cyclones_stage'
postgre.run_query(trunc_sql)

copy_sql = "COPY cyclones_stage FROM STDIN DELIMITER ';' CSV"
postgre.copy_file(sql=copy_sql, filename=options.file, mode='r')

# merge stage to history

load_dt = options.file.split('.')[-2].split('_')[-1]
merge_sql = open(config['sql']['merge_sql'], 'r').read()
merge_sql = merge_sql.replace('*load_date*', load_dt)

postgre.run_query(merge_sql)
