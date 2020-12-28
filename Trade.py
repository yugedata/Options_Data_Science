from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy import inspect
import matplotlib as plt
import pandas as pd


buying_power = 50000

# columns: trade_id, openClose, time, contracts, quantities, prices, total, gainLoss, type, width


def make_sqlite_table(table_name):

    metadata = MetaData()
    trades = Table('iron_condors', metadata,
                   Column('trade_id', Integer, primary_key=True),
                   Column('openClose', Integer),
                   Column('time', Integer),
                   Column('contracts', String),   # tuple
                   Column('quantities', String),  # tuple
                   Column('prices', String),      # tuple
                   Column('total', Integer),      # total of prices
                   Column('gainLoss', Integer),
                   Column('type', String),
                   Column('width', String))
    engine = create_engine('sqlite:///Trades.db', echo=False)
    metadata.create_all(engine)
    inspector = inspect(engine)
    inspector.get_columns('iron_condors')

    return 0


def add_rows(clean_data, table_name):

    engine = create_engine('sqlite:///Trades.db', echo=False)
    with engine.connect() as con:

        data = ({'trade_id': 1, 'openClose': 1, 'time': 1232456789,
                 'contracts': '(AAPL_121120P123, AAPL_121120P123, AAPL_121120P123, AAPL_121120P123)',
                 'quantities': '(1, 1, 1, 1)', 'prices': '(103, 50, 140, 60)',
                 'total': 353, 'gainLoss': -100, 'width': 'tight'})

        sql = text(f'''INSERT INTO {table_name}
                (trade_id, openClose, time, contracts, quantities, prices, total, gainLoss, type, width)
                VALUES(:time, :contracts, :quantities, :prices, :total, :gainLoss, :type, :width)''')

        for line in data:
            con.execute(sql, **line)

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


# this func will act as a checkout cart, outputting the combination
# of contracts needed to buy/sell to create the explicit option spread
# output: tuple with only strings of contract(s) symbol/id
def basket():
    cart = []
    return 0




