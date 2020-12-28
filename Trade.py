from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy import inspect
import matplotlib as plt
import pandas as pd


buying_power = 50000

cart = []

columns = ['trade_id', 'openClose', 'time', 'contracts', 'quantities',
           'prices', 'total', 'debitCredit', 'width']


def make_sqlite_table(table_name):

    metadata = MetaData()
    trades = Table(f'{table_name}', metadata,
                   Column('trade_id', Integer),
                   Column('openClose', Integer),
                   Column('time', Integer),
                   Column('contracts', String),   # tuple
                   Column('quantities', String),  # tuple
                   Column('prices', String),      # tuple
                   Column('total', Integer),      # total of prices
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


test_data = [[123, 1, 12321321321, f'(AAPL_121120P123, AAPL_121120P123, AAPL_121120P123, AAPL_121120P123)',
              f'(1, 1, 1, 1)', f'(100, 50, 110, 60)', 90, -90, 8]]

test_data = pd.DataFrame(test_data, columns=columns)

make_sqlite_table('iron_condors')
add_rows(test_data, 'iron_condors')
show_table('iron_condors')


# this func will act as a checkout cart, outputting the combination
# of contracts needed to buy/sell to create the explicit option spread
# output: tuple with only strings of contract(s) symbol/id
def basket():

    global cart

    return cart

