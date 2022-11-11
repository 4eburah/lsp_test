import argparse
import datetime
import calendar

import postgre

def validate_cli_options(options):
    '''Validates command line options'''
    assert options.month is not None, \
        'Month to unload must be specified as argument as YYYYMM'

    try:
        datetime.datetime.strptime(options.month, '%Y%m')
    except ValueError:
        raise ValueError("Incorrect month format, should be YYYYMM")


def get_cli_options():
    '''Returns command line options'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-month', help = 'Month to unload like YYYYMM')
    parser.add_argument('-out_dir', default = './csv_dir', help = 'Output dir for csv files')
    options = parser.parse_args()
    validate_cli_options(options)
    return options


if __name__ == '__main__':
    options = get_cli_options()

    start_date = datetime.datetime.strptime(options.month, '%Y%m').date()
    end_date = datetime.date(start_date.year, start_date.month, calendar.monthrange(start_date.year, start_date.month)[-1])

    while start_date < end_date:
        cur_date_str = start_date.strftime("%Y-%m-%d")
        cur_date_str_nodash = start_date.strftime("%Y%m%d")

        sql="""COPY (select id, dt, status 
                from (SELECT id, dt, status,
                    row_number() over (partition by id order by tm desc) as rn
                    FROM cyclones where dt = '{dt}') a
                where rn = 1) TO STDOUT WITH CSV DELIMITER ';'""".format(dt=cur_date_str)

        start_date += datetime.timedelta(days=1)

        out_file_name = f'{options.out_dir}/cyclones_{cur_date_str_nodash}.csv'
        print(f'writing to {out_file_name}')

        postgre.copy_file(sql=sql, filename=out_file_name, mode='w')
