from sqlalchemy import create_engine
from td.client import TDClient
from datetime import datetime
from td import exceptions
from requests.exceptions import ConnectionError
import datetime
import pandas as pd
import sqlite3
import time
import credentials

print("- Modules imported -")


def make_sqlite_table(table_name):
    engine = create_engine('sqlite:///Options_temp.db', echo=False)
    table_columns = pd.DataFrame(columns=columns_wanted)
    table_columns.to_sql(table_name, con=engine)

    return 0


def add_rows(clean_data, table_name):
    global file_date
    engine = create_engine(f'sqlite:///Data/Options_{file_date}.db', echo=False)
    clean_data.to_sql(table_name, con=engine, if_exists='append', index_label='index')

    return 0


def delete_row(table_name, column, argument):
    conn = sqlite3.connect('Options.db')
    con = conn.cursor()
    con.execute(f'DELETE FROM {table_name} WHERE {column}={argument}')
    conn.commit()
    conn.close()

    return 0


def delete_db_table(table_name):
    conn = sqlite3.connect('options.db')
    con = conn.cursor()
    con.execute(f'DROP TABLE {table_name}')
    conn.commit()
    conn.close()

    return 0


def show_db_table(puts_calls):
    conn = sqlite3.connect('options.db')
    con = conn.cursor()
    for row in con.execute(f'SELECT * FROM {puts_calls}'):
        print(row)
    conn.close()

    return 0


TDSession = TDClient(
    client_id=credentials.client_id,
    redirect_uri='https://127.0.0.1',
    credentials_path=credentials.json_path  #  Users/user/.../Project/td_state.json
)

TDSession.login()
print("- TD connection made -")


def human_time(epoch):
    new_time = datetime.fromtimestamp(int(epoch) / 1000)
    output = new_time.strftime('%Y-%m-%d %H:%M:%S')

    return output


def get_time_now():
    curr_time = time.localtime()
    curr_clock = time.strftime("%H:%M:%S", curr_time)
    curr_m = time.strftime('%m')
    curr_y_d = time.strftime('%d%Y')

    int_curr_clock = int(f'{curr_clock[:2]}{curr_clock[3:5]}')

    return int_curr_clock, curr_m, curr_y_d


def history(symbol):
    quotes = TDClient.get_price_history(TDSession, symbol=symbol, period_type='day',
                                        period=1, frequency_type='minute', frequency=1,
                                        extended_hours=False)
    # start_date = 1606086000000, end_date = 1606341600000,

    return quotes


cur_weekly = 0
cur_stocks = ['AAPL']

'''
test_quotes_2D = TDClient.get_quotes(TDSession, instruments=['AMD', 'AAPL'])


def stats_list():
    stats_wanted = ['symbol', 'bidPrice', 'bidSize', 'bidId', 'askPrice', 'askId',
                    'lastPrice', 'lastSize', 'lastId', 'openPrice', 'highPrice',
                    'lowPrice', 'bidTick', 'closePrice', 'netChange', 'totalVolume',
                    'quoteTimeInLong', 'tradeTimeInLong', 'exchange',
                    'exchangeName', 'volatility',
                    'regularMarketLastPrice', 'regularMarketNetChange',
                    'regularMarketTradeTimeInLong', 'netPercentChangeInDouble',
                    'markChangeInDouble', 'markPercentChangeInDouble',
                    'regularMarketPercentChangeInDouble']

    output_stats = []

    for key in test_quotes_2D['AMD'].keys():
        for i in stats_wanted:
            if key == i:
                output_stats.append(key)

    return output_stats
'''

file_date = 0

trade_days_2021 = {'jan': [4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 19, 20, 21, 22, 25, 26, 27, 28, 29],
                   'feb': [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 16, 17, 18, 19, 22, 23, 24, 25, 26],
                   'mar': [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 29, 30, 31],
                   'apr': [5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 26, 27, 28, 29, 30],
                   'may': [3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28],
                   'jun': [1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 28, 29, 30],
                   'jul': [1, 2, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 26, 27, 28, 29, 30],
                   'aug': [2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 30, 31],
                   'sep': [1, 2, 3, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 27, 28, 29, 30],
                   'oct': [1, 4, 5, 6, 7, 8, 12, 13, 14, 15, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29],
                   'nov': [1, 2, 3, 4, 5, 8, 9, 10, 12, 15, 16, 17, 18, 19, 22, 23, 24, 29, 30],
                   'dec': [1, 2, 3, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 27, 28, 29, 30]}

opt_column_names = ['putCall', 'symbol', 'description', 'exchangeName', 'bid', 'ask', 'last', 'mark', 'bidSize',
                    'askSize', 'bidAskSize', 'lastSize', 'highPrice', 'lowPrice', 'openPrice', 'closePrice',
                    'totalVolume', 'tradeDate', 'tradeTimeInLong', 'quoteTimeInLong', 'netChange', 'volatility',
                    'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue', 'theoreticalOptionValue',
                    'theoreticalVolatility', 'optionDeliverablesList', 'strikePrice', 'expirationDate',
                    'daysToExpiration',
                    'expirationType', 'lastTradingDay', 'multiplier', 'settlementType', 'deliverableNote',
                    'isIndexOption', 'percentChange', 'markChange', 'markPercentChange', 'mini', 'inTheMoney',
                    'nonStandard']

columns_unwanted = ['description', 'mark', 'bidSize', 'askSize', 'bidAskSize', 'lastSize', 'tradeDate',
                    'tradeTimeInLong', 'theoreticalOptionValue', 'optionDeliverablesList',
                    'expirationType', 'lastTradingDay', 'multiplier', 'settlementType', 'deliverableNote',
                    'isIndexOption', 'markChange', 'markPercentChange', 'nonStandard', 'inTheMoney', 'mini']

columns_wanted = ['putCall', 'symbol', 'exchangeName', 'bid', 'ask', 'last', 'highPrice',
                  'lowPrice', 'openPrice', 'closePrice', 'totalVolume', 'quoteTimeInLong',
                  'netChange', 'volatility', 'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue',
                  'theoreticalVolatility', 'strikePrice', 'expirationDate', 'daysToExpiration', 'percentChange']

stocks = ['AAL', 'AAPL', 'AMD', 'AMZN', 'APA', 'ATVI', 'AXP', 'BABA', 'CME', 'CMG', 'CSCO',
          'DAL', 'DIS', 'EA', 'FB', 'GME', 'GOOG', 'GS', 'HD', 'IBM', 'JNJ', 'JPM',
          'MCD', 'MSFT', 'MU', 'NEE', 'NFLX', 'NVDA', 'ORCL', 'PEP', 'PYPL', 'QQQ', 'ROKU', 'SBUX',
          'SNAP', 'SPY', 'SQ', 'TSLA', 'TWTR', 'ULTA', 'UPS', 'V', 'VXX', 'WMT', 'YUM',
          'VDE', 'XLB', 'XLI', 'VCR', 'VDC', 'XLV', 'XLF', 'VGT', 'XLC', 'XLU', 'VNQ']

# This segment was used to sort out unique columns after i hard coded the columns i wanted
'''
# print(len(opt_column_names))
# print(len(columns_unwanted))
# print(len(columns_wanted))
# print(len(stocks))
outs = []


def unique_list(n):
    output = []

    for x in n:
        if x not in output:
            output.append(x)
        else:
            print(x)
    print(len(output))

    return 0



for i in opt_column_names:
    for j in columns_wanted:
        if i == j:
            outs.append(i)


print(outs)
print(len(outs))
unique_list(outs)
'''
trade_stocks = ['AAPL', 'SPY', 'ROKU', 'TSLA', 'GME']


def get_weekly_data(clean):
    # get data for just the stuff we want to use
    for r in clean.iterrows():
        if r[1][-2] == 'symbol':
            print(r[1])
        if r[0] == 'bid':
            print(r[1])
        print(r[1][2])

    return 0


def get_stock(stock):  # pass an array of ticker(s) for stock
    stock_lookup = TDSession.get_quotes(instruments=stock)

    return stock_lookup


def raw_stock(raw):
    clean_stock_data = [[]]

    for i in raw.keys():
        print(i)

    return clean_stock_data


def pandas_stock_data(arr):
    pandas_data = []
    return pandas_data


def get_next_stock():
    global pulls
    global failed_pulls

    for stock in trade_stocks:
        error = False

        try:
            stock_data = get_stock(stock)

        except (exceptions.ServerError, exceptions.GeneralError, exceptions.ExdLmtError, ConnectionError):
            error = True
            failed_pulls = failed_pulls + 1
            print('A server error occurred')

        if not error:
            try:
                clean_stock_data = pandas_stock_data(raw_stock(stock_data))
                # add_rows(clean_stock_data) UNCOMMENT TO ADD TO STOCKS.DB
                pulls = pulls + 1

            except ValueError:
                print(ValueError.with_traceback())
                print(f'{stock} did not have values for this iteration')
                failed_pulls = failed_pulls + 1

        print(stock)
        time.sleep(1)
    return 0


def get_chain(stock):
    opt_lookup = TDSession.get_options_chain(
        option_chain={'symbol': stock, 'strikeCount': 50,
                      'toDate': '2021-4-23'})

    return opt_lookup


def raw_chain(raw, put_call):
    cp = f'{put_call}ExpDateMap'
    clean_data = [[]]
    r = -1
    for k in raw[cp].keys():
        # print(k, raw[k], '\n')
        for strike in raw[cp][k].keys():
            # print(strike, raw[k][strike])
            for a in raw[cp][k][strike][0].keys():
                # if r == -1:
                #    print(raw[cp][k][strike][0].keys())
                unit = raw[cp][k][strike][0][a]
                if unit == put_call.upper():
                    r = r + 1
                    if r > 0:
                        clean_data.append([])

                clean_data[r].append(unit)

    return clean_data


def pandas_chain(clean):

    df_cp = pd.DataFrame(clean, columns=opt_column_names)
    panda_data = df_cp.drop(columns=columns_unwanted)

    return panda_data


pulls = 0
failed_pulls = 0


def get_next_chains():
    x = 0
    global pulls
    global failed_pulls
    global cur_stocks

    for stock in stocks:
        error = False

        try:
            chain = get_chain(stock)

        except (exceptions.ServerError, exceptions.GeneralError, exceptions.ExdLmtError, ConnectionError):
            error = True
            failed_pulls = failed_pulls + 1
            print('A server error occurred')

        if not error:
            try:
                clean = pandas_chain(raw_chain(chain, 'call'))
                add_rows(clean, 'calls')
                for s in cur_stocks:
                    if s == stock:
                        get_weekly_data(clean)
                pulls = pulls + 1

            except ValueError:
                print(ValueError.with_traceback())
                print(f'{x}: Calls for {stock} did not have values for this iteration')
                failed_pulls = failed_pulls + 1

            try:
                get_clean = pandas_chain(raw_chain(chain, 'put'))
                add_rows(get_clean, 'puts')
                pulls = pulls + 1

            except ValueError:
                print(f'{x}: Puts for {stock} did not have values for this iteration')
                failed_pulls = failed_pulls + 1

        print(f'{x}: {stock}')
        x = x + 1
        time.sleep(2)

    return 0


# |SQLite management| #
#
# make_sqlite_table('calls')  # inputs: puts|calls
# make_sqlite_table('puts')  # inputs: puts|calls
# delete_db_table('calls')
# delete_db_table('puts')
# show_db_table('calls')
# show_db_table('puts')
# add_rows(clean_chain(raw_chain(get_chain('SPY'), 'put')), 'puts')  # raw_chain(,'put|call')), 'puts|calls')
# delete_row('puts', '', 1321354652)


def main():
    global file_date
    global trade_stocks

    t, mon, day = get_time_now()
    mon = list(trade_days_2021.keys())[int(mon) - 1]
    '''  # uncomment for LIVE
    while True:
        if (t < 930) or (t > 1600):
            print(f'{t}: Market closed {mon}{day}'.upper())
            time.sleep(10)
        else:
            break
    '''
    # uncomment below line when TESTING on live data
    file_date = f'temp'
    # uncomment below line to save and analyze live data
    # file_date = f'{mon}{day}'

    pull_count = 0
    end_t = 1600

    while get_time_now()[0]:  # < end_t: insert segment to run LIVE
        # get_next_stock()
        get_next_chains()
        pull_count = pull_count + 1
        print(pull_count)

    print('option market closed')
    print(f'failed_pulls: {failed_pulls}')
    print(f'pulls: {pulls}')

    return 0


main()
