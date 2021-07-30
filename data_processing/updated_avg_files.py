"""
Say you 
Initially This script takes the Options_averages_calls.db & Options_averages_puts.db files created with contracts_avg_volume.py 
combines it with the
"""

import sqlite3
import os
import pandas as pd
import time
from sqlalchemy import create_engine
from pandas.io.sql import DatabaseError

os.system('afplay /System/Library/Sounds/Sosumi.aiff')


def get_time_now():
    curr_time = time.localtime()
    curr_clock = time.strftime("%H:%M:%S", curr_time)
    curr_m = time.strftime('%m')
    curr_y_d = time.strftime('%d%Y')

    int_curr_clock = int(f'{curr_clock[:2]}{curr_clock[3:5]}')

    return int_curr_clock, curr_m, curr_y_d


t, mon, day = get_time_now()


def add_rows(clean_data, table_name, calls_puts, d):
    temp_d = d
    # d = int(d) - 10000 # for doing averages of yesterday
    d = int(d)

    if temp_d[0] == '0':
        engine = create_engine(f'sqlite:///Options_averages_{calls_puts}_0{d}.db', echo=False)
    else:
        engine = create_engine(f'sqlite:///Options_averages_{calls_puts}_{d}.db', echo=False)

    clean_data.to_sql(table_name, con=engine, if_exists='append', index_label='index')

    return 0


def update_averages(data_file, call_file, put_file):

    con = sqlite3.connect(f'AvgData/{data_file}')  # next mining day file
    con_c = sqlite3.connect(f'{call_file}')  # last average file
    con_p = sqlite3.connect(f'{put_file}')  # last average file

    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

    for tab in cursor.fetchall():

        Tab = str(tab[0])
        temp_date = (mon+day)[:4]

        if Tab[0][0] == 'c':
            
            calls = pd.read_sql_query(
                f'SELECT symbol, totalVolume, quoteTimeInLong FROM \'{Tab}\' WHERE (totalVolume > 10) AND (symbol LIKE \"%!_07%\" ESCAPE \"!\" OR symbol LIKE \"%!_08%\" ESCAPE \"!\") ', con)
            
            symbol_count = 0

            for i, r in calls.iterrows():
                temp_sym = r['symbol']
                temp_stock = temp_sym.split('_')[0]
                next_date = temp_sym.split('_')[1][:4]

                if next_date < (mon+day)[:4]:
                    continue

                if next_date >= temp_date:
                    temp_date = next_date
                    try:
                        temp_calls = pd.read_sql_query(f'SELECT * FROM \'{Tab + temp_date}\' ', con_c)

                        if temp_sym in temp_calls.values:

                            temp_row = temp_calls.loc[temp_calls['symbol'] == temp_sym].copy()
                            temp_row.drop(['index'], axis='columns', inplace=True)
                            temp_row.index = [symbol_count]

                            temp_avg = temp_row['avgVolume'] * temp_row['daysComputed']
                            temp_days = temp_row['daysComputed'] + 1
                            temp_avg = (temp_avg + r['totalVolume']) // temp_days
                            temp_row.at[symbol_count, 'avgVolume'] = temp_avg
                            temp_row.at[symbol_count, 'daysComputed'] = temp_days

                            symbol_count = symbol_count + 1
                            add_rows(temp_row, f'c{temp_stock}{next_date}', 'calls', f'{mon}{day}')

                        else:

                            new_row = {'symbol': [temp_sym], 'avgVolume': [r['totalVolume']], 'daysComputed': [1]}
                            working_new = pd.DataFrame(data=new_row)
                            working_new.index = [symbol_count]
                            add_rows(working_new, f'c{temp_stock}{next_date}', 'calls', f'{mon}{day}')
                            symbol_count = symbol_count + 1

                    except DatabaseError as e:
                        if e.args[0].startswith('Execution failed on sql'):

                            new_row = {'symbol': [temp_sym], 'avgVolume': [r['totalVolume']], 'daysComputed': [1]}
                            working_new = pd.DataFrame(data=new_row)
                            working_new.index = [symbol_count]
                            add_rows(working_new, f'c{temp_stock}{next_date}', 'calls', f'{mon}{day}')
                            symbol_count = symbol_count + 1

                        else:
                            pass
                else:
                    pass

        else:

            puts = pd.read_sql_query(
                f'SELECT symbol, totalVolume, quoteTimeInLong FROM \'{Tab}\' WHERE (totalVolume > 10) AND (symbol LIKE \"%!_07%\" ESCAPE \"!\" OR symbol LIKE \"%!_08%\" ESCAPE \"!\") ', con)
            
            symbol_count = 0

            for i, r in puts.iterrows():
                temp_sym = r['symbol']
                temp_stock = temp_sym.split('_')[0]
                next_date = temp_sym.split('_')[1][:4]

                if next_date < (mon + day)[:4]:
                    continue

                if next_date >= temp_date:
                    temp_date = next_date

                    try:
                        temp_puts = pd.read_sql_query(f'SELECT * FROM \'{Tab + temp_date}\' ', con_p)

                        if temp_sym in temp_puts.values:

                            temp_row = temp_puts.loc[temp_puts['symbol'] == temp_sym].copy()
                            temp_row.drop(['index'], axis='columns', inplace=True)
                            temp_row.index = [symbol_count]

                            temp_avg = temp_row['avgVolume'] * temp_row['daysComputed']
                            temp_days = temp_row['daysComputed'] + 1
                            temp_avg = (temp_avg + r['totalVolume']) // temp_days
                            temp_row.at[symbol_count, 'avgVolume'] = temp_avg
                            temp_row.at[symbol_count, 'daysComputed'] = temp_days

                            symbol_count = symbol_count + 1
                            add_rows(temp_row, f'p{temp_stock}{next_date}', 'puts', f'{mon}{day}')

                        else:

                            new_row = {'symbol': [temp_sym], 'avgVolume': [r['totalVolume']], 'daysComputed': [1]}
                            working_new = pd.DataFrame(data=new_row)
                            working_new.index = [symbol_count]

                            add_rows(working_new, f'p{temp_stock}{next_date}', 'puts', f'{mon}{day}')
                            symbol_count = symbol_count + 1

                    except DatabaseError as e:

                        if e.args[0].startswith('Execution failed on sql'):

                            new_row = {'symbol': [temp_sym], 'avgVolume': [r['totalVolume']], 'daysComputed': [1]}
                            working_new = pd.DataFrame(data=new_row)
                            working_new.index = [symbol_count]
                            add_rows(working_new, f'p{temp_stock}{next_date}', 'puts', f'{mon}{day}')
                            symbol_count = symbol_count + 1

                        else:
                            pass
                else:
                    pass

    con_c.close()
    con_p.close()
    con.close()

    return 0

# update_averages(Data file of mined data from previous day )
update_averages('Options_jul282021.db', 'Options_averages_calls_07272021.db', 'Options_averages_puts_07272021.db')
os.system('say "Finished processing the average volume files."')
os.system('afplay /System/Library/Sounds/Sosumi.aiff')

