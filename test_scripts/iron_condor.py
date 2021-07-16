from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, REAL
from sqlalchemy.sql import text
from sqlalchemy import inspect
import matplotlib as plt
import pandas as pd

# full program is hidden, contact me for sample trader


buying_power = 50000

cart = []

columns = ['trade_id', 'openClose', 'time', 'daysLeft', 'outsideCall', 'insideCall',
           'insidePut', 'outsidePut', 'quantity', 'costOutCall', 'costInCall',
           'costInPut', 'costOutPut', 'total', 'debitCredit', 'width']

stocks = ['AAPL', 'AMZN', 'SPY', 'AMD', 'NVDA', 'NFLX', 'QQQ', 'ROKU']

current_data = []

for s in stocks:
    current_data.append(s)


def make_sqlite_table(table_name):

    metadata = MetaData()
    trades = Table(f'{table_name}', metadata,
                   Column('trade_id', Integer),
                   Column('openClose', Integer),
                   Column('time', Integer),
                   Column('daysLeft', Integer),
                   Column('outsideCall', String),
                   Column('insideCall', String),
                   Column('insidePut', String),
                   Column('outsidePut', String),
                   Column('quantity', Integer),
                   Column('costOutCall', REAL),
                   Column('costInCall', REAL),
                   Column('costInPut', REAL),
                   Column('costOutPut', REAL),
                   Column('total', Integer),
                   Column('debitCredit', Integer),
                   Column('width', Integer))

    engine = create_engine('sqlite:///Trades.db', echo=False)
    metadata.create_all(engine)

    inspector = inspect(engine)
    inspector.get_columns(f'{table_name}')

    return 0


def add_rows(clean_data, table_name):

    engine = create_engine('sqlite:///Trades.db', echo=False)
    clean_data.to_sql(table_name, con=engine, if_exists='append', index_label='rowid')

    return 0


def show_table(table_name):

    engine = create_engine('sqlite:///Trades.db', echo=False)
    with engine.connect() as con:

        rs = con.execute(f'SELECT * FROM {table_name}')
        for row in rs:
            print(row)

    return 0


def delete_row(table_name, column, argument):

    engine = create_engine('sqlite:///Trades.db', echo=False)
    with engine.connect() as con:

        con.execute(f'DELETE FROM {table_name} WHERE {column}={argument}')

    return 0


def buy_call(symbol, strikePrice, ask, quoteTimeInLong):

    return 0


def buy_put(symbol, strikePrice, ask, quoteTimeInLong):

    return 0


def sell_call(symbol, strikePrice, bid, quoteTimeInLong):

    return 0


def sell_put(symbol, strikePrice, bid, quoteTimeInLong):

    return 0


def open_iron_condor():

    return 0


def close_iron_condor():

    return 0


test_data = [[123, 1, 12321321321, 5, 110, 100, 90, 80, 1, 8.36, -10.30, -12.50,
             9.20, -4.30, 0, 10]]

test_data = pd.DataFrame(test_data, columns=columns)

# make_sqlite_table('iron_condors')
add_rows(test_data, 'iron_condors')
show_table('iron_condors')



