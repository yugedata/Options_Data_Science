from sqlalchemy import create_engine
import sqlite3
import os
import pandas as pd

# file_date = ""

read_directory = '/Users/sato/PycharmProjects/open_interest/Data/'
write_directory = '/Users/sato/PycharmProjects/open_interest/Data_Library/'
substring = '_'

columns = ['index', 'putCall', 'symbol', 'exchangeName', 'bid', 'ask', 'last',
            'highPrice', 'lowPrice', 'openPrice', 'closePrice', 'totalVolume', 'quoteTimeInLong', 'netChange',
            'volatility', 'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue',
            'theoreticalVolatility', 'strikePrice', 'expirationDate', 'daysToExpiration', 'percentChange']


def add_rows(clean_data, table_name, file_date):

    engine = create_engine(f'sqlite:///Data_Library/{file_date}', echo=False)
    clean_data.to_sql(table_name, con=engine, if_exists='append')

    return 0


# sorting tickers is working but writing to new file is not
for filename in os.listdir(read_directory):
    if filename.endswith(".db"):
        print(filename)
        con = sqlite3.connect(f'{read_directory}{filename}')
        df = pd.read_sql_query('''SELECT * FROM calls''', con)

        # df = df.drop(columns='index').to_numpy()
        df = df.to_numpy()
        temp_df = []
        temp_equity = 0

        for i in df:
            if int(i[0]) == 0:
                if temp_equity:
                    go_df = pd.DataFrame(temp_df, columns=columns)
                    add_rows(go_df.drop(columns=['index']), f'c{temp_equity}', filename)
                    temp_df = []

                temp_df.append(i)
                temp_contract = i[2]
                temp_equity = temp_contract.partition(substring)[0]
            else:
                temp_df.append(i)

for filename in os.listdir(read_directory):
    if filename.endswith(".db"):
        print(filename)
        con = sqlite3.connect(f'{read_directory}{filename}')
        df = pd.read_sql_query('''SELECT * FROM puts''', con)

        # df = df.drop(columns='index').to_numpy()
        df = df.to_numpy()
        temp_df = []
        temp_equity = 0

        for i in df:
            if int(i[0]) == 0:
                if temp_equity:
                    go_df = pd.DataFrame(temp_df, columns=columns)
                    add_rows(go_df.drop(columns=['index']), f'p{temp_equity}', filename)
                    temp_df = []

                temp_df.append(i)
                temp_contract = i[2]
                temp_equity = temp_contract.partition(substring)[0]
            else:
                temp_df.append(i)
