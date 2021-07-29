import sqlite3
import os
import pandas as pd
import numpy as np
import csv
import time

import pandas.io.sql
from sqlalchemy import create_engine
from pandas.io.sql import DatabaseError

directory = '/Users/.../NewData/'

contracts_calls = set()
contracts_puts = set()

volumes_calls = {}
volumes_puts = {}

Contracts_calls = []
Contracts_puts = []

column_names = ['symbol', 'avgVolume', 'daysComputed']


def get_time_now():
    curr_time = time.localtime()
    curr_clock = time.strftime("%H:%M:%S", curr_time)
    curr_m = time.strftime('%m')
    curr_y_d = time.strftime('%d%Y')

    int_curr_clock = int(f'{curr_clock[:2]}{curr_clock[3:5]}')

    return int_curr_clock, curr_m, curr_y_d


def add_column_csv(f_name, arr):
    arr = np.array(arr)
    np.savetxt(f_name, arr, delimiter=',', fmt='%s', header='contracts', comments='')


def add_contracts(df, call_put):
    for i, j in df.iterrows():
        if call_put == 'calls':
            contracts_calls.add(str(j['symbol']))
        elif call_put == 'puts':
            contracts_puts.add(str(j['symbol']))
        else:
            continue


def get_uniques_columns():  # get unique symbols from all files in directory

    for F_name in os.listdir(directory):
        if F_name.endswith(".db"):
        
            print(os.path.join(directory, F_name))
            con = sqlite3.connect(f'NewData/{F_name}')
            cursor = con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

            for tab in cursor.fetchall():
                s_table = str(tab[0])
                
                if tab[0][0] == 'c':
                    calls = pd.read_sql_query(f'SELECT DISTINCT symbol FROM \'{s_table}\' WHERE totalVolume > 5" ', con)
                    add_contracts(calls, 'calls')
                else:
                    puts = pd.read_sql_query(f'SELECT DISTINCT symbol FROM \'{s_table}\' WHERE totalVolume > 5 AND ', con)
                    add_contracts(puts, 'puts')
        else:
            continue

    print(len(contracts_calls), ' unique call contracts')
    print(len(contracts_puts), ' unique put contracts')

    con.close()


get_uniques_columns()


def write_uniques(to_file_calls, to_file_puts):
    # This block with write all unique contracts to a file
    symbols_calls = []
    symbols_puts = []
    
    for i in contracts_calls:
        symbols_calls.append(str(i))

    for i in contracts_puts:
        symbols_puts.append(str(i))

    add_column_csv(to_file_calls, sorted(symbols_calls))
    add_column_csv(to_file_puts, sorted(symbols_puts))


write_uniques('unique_data_calls.csv', 'unique_data_puts.csv')


def read_uniques(file_name, calls_puts):
    get_symbols = pd.read_csv(file_name)
    if calls_puts == 'calls':
        for i, row in get_symbols.iterrows():
            Contracts_calls.append(row['contracts'])
    if calls_puts == 'puts':
        for i, row in get_symbols.iterrows():
            Contracts_puts.append(row['contracts'])


read_uniques('unique_data_calls.csv', 'calls')
read_uniques('unique_data_puts.csv', 'puts')


# read unique_data.csv to make list of lists for volume
def make_call_list():
    for sym in Contracts_calls:
        if int(sym.split("_")[1][:2]) >= 7:
            volumes_calls[sym] = [0, 0]


def make_put_list():
    for sym in Contracts_puts:
        if int(sym.split("_")[1][:2]) >= 7:
            volumes_puts[sym] = [0, 0]


def add_rows(clean_data, table_name):

    engine = create_engine(f'sqlite:///Options_averages.db', echo=False)
    clean_data.to_sql(table_name, con=engine, if_exists='append', index_label='index')

    return 0


def clean_chain(raw):
    global column_names
    clean = pd.DataFrame(raw, columns=column_names)

    return clean


make_call_list()
make_put_list()

trade_days_2021 = {'jan': [4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 19, 20, 21, 22, 25, 26, 27, 28, 29],
                   'feb': [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 16, 17, 18, 19, 22, 23, 24, 25, 26],
                   'mar': [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 29, 30, 31],
                   'apr': [1, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 26, 27, 28, 29, 30],
                   'may': [3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28],
                   'jun': [1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 28, 29, 30],
                   'jul': [1, 2, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 26, 27, 28, 29, 30],
                   'aug': [2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 30, 31],
                   'sep': [1, 2, 3, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 27, 28, 29, 30],
                   'oct': [1, 4, 5, 6, 7, 8, 12, 13, 14, 15, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29],
                   'nov': [1, 2, 3, 4, 5, 8, 9, 10, 12, 15, 16, 17, 18, 19, 22, 23, 24, 29, 30],
                   'dec': [1, 2, 3, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 27, 28, 29, 30]}

t, mon, day = get_time_now()
month = list(trade_days_2021.keys())[int(mon) - 1]

daily_avg_file_c = f'calls_avg_{month}{day}.csv'
daily_avg_file_p = f'puts_avg_{month}{day}.csv'


print('Extracting Call volume data...\n')

call_dict = {}
c_count = 0
last_x = ''

for x in sorted(volumes_calls.keys()):
    
    t = x.split("_")

    if x == last_x:
        pass
    else:
        last_x = x

        for filename in os.listdir(directory):
            if filename.endswith(".db"):
                con = sqlite3.connect(f'NewData/{filename}')
                try:
                    data = pd.read_sql_query('SELECT symbol, totalVolume, quoteTimeInLong '
                                             f'FROM \'c{t[0]}\' WHERE totalVolume > 5 AND ORDER BY quoteTimeInLong DESC', con)

                    dict_copy = data.to_dict('records')
                    call_dict[f'{filename}'] = dict_copy

                except DatabaseError as e:
                    # print(e)
                    continue
                con.close()

    table = t[0] + t[1][:4]
    not_here_count_c = 0
    temp_avg = 0
    temp_cnt = 0

    # for each symbol in volumes_puts{} get avg from all saved files
    for key, value in call_dict.items():
        for r in value:
            if x == r['symbol']:
                temp_vol = volumes_calls[x][0]
                temp_cnt = volumes_calls[x][1] + 1
                temp_avg = int((temp_vol + int(r['totalVolume'])) / temp_cnt)
                volumes_calls[x][0] = temp_avg
                volumes_calls[x][1] = temp_cnt
                
                break

    temp_data = {'symbol': [x], 'avgVolume': [temp_avg], 'daysComputed': [temp_cnt]}
    working_call_data = pd.DataFrame(data=temp_data)
    add_rows(working_call_data, f'c{table}')
    
print('Extracting Put volume data...\n')

p_count = 0
for x in sorted(volumes_puts.keys()):
    # print(x)
    t = x.split("_")
    table = t[0] + t[1][:4]
    not_here_count_p = 0
    temp_avg = 0

    for filename in os.listdir(directory):
        if filename.endswith(".db"):
            con = sqlite3.connect(f'NewData/{filename}')
            try:
                data = pd.read_sql_query('SELECT symbol, totalVolume, quoteTimeInLong '
                                         f'FROM \'p{t[0]}\' WHERE totalVolume > 5 AND ORDER BY quoteTimeInLong DESC', con)
            except DatabaseError as e:
                # print(e)
                continue
            if not set([x]).issubset(data['symbol']):
                not_here_count_p = not_here_count_p + 1

            else:
                # for each symbol in volumes_puts{} get avg from all saved files
                dict_copy = data.to_dict('records')
                for r in dict_copy:
                    if x == r['symbol']:
                        temp_vol = volumes_puts[x][0]
                        temp_cnt = volumes_puts[x][1] + 1
                        temp_avg = int((temp_vol + int(r['totalVolume'])) / temp_cnt)
                        volumes_puts[x][0] = temp_avg
                        volumes_puts[x][1] = temp_cnt
                        break

    temp_data = {'symbol': [x], 'avgVolume': [temp_avg], 'daysComputed': [temp_cnt]}
    working_put_data = pd.DataFrame(data=temp_data)
    add_rows(working_put_data, f'p{table}')
    p_count = p_count + 1
    print(p_count)

