from sqlalchemy import create_engine
from td.client import TDClient
from datetime import datetime
from td import exceptions
import datetime
import pandas as pd
import sqlite3
import time


TDSession = TDClient(
    client_id='AYGTNN1VCCC3GV7SBFAGT3SZC8AXEPBE',
    redirect_uri='https://127.0.0.1',
    credentials_path='/Users/Sato/Documents/PycharmProjects/open_interest/td_state.json'
)

TDSession.login()


def human_time(epoch):
    new_time = datetime.fromtimestamp(int(epoch) / 1000)
    output = new_time.strftime('%Y-%m-%d %H:%M:%S')

    return output


def get_time_now():
    curr_time = time.localtime()
    curr_clock = time.strftime("%H:%M:%S", curr_time)

    int_curr_clock = int(f'{curr_clock[:2]}{curr_clock[3:5]}')

    return int_curr_clock


def history(symbol):
    quotes = TDClient.get_price_history(TDSession, symbol=symbol, period_type='day',
                                        period=1, frequency_type='minute', frequency=1,
                                        extended_hours=False)
    # start_date = 1606086000000, end_date = 1606341600000,

    return quotes


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

# test_quote_time_epoch = test_quotes_2D['AMD']['regularMarketTradeTimeInLong']
# human_time(test_quote_time_epoch)

trade_days_2021 = [[4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 19, 20, 21, 22, 25, 26, 27, 28, 29],
                   [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 16, 17, 18, 19, 22, 23, 24, 25, 26],
                   [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 29, 30, 31],
                   [5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 26, 27, 28, 29, 30],
                   [3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28],
                   [1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 28, 29, 30],
                   [1, 2, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 26, 27, 28, 29, 30],
                   [2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 30, 31],
                   [1, 2, 3, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 27, 28, 29, 30],
                   [1, 4, 5, 6, 7, 8, 12, 13, 14, 15, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29],
                   [1, 2, 3, 4, 5, 8, 9, 10, 12, 15, 16, 17, 18, 19, 22, 23, 24, 29, 30],
                   [1, 2, 3, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 27, 28, 29, 30]]
month, day = 0, 10
# if get_time_now()

today = trade_days_2021[month][day]

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

stocks = ['AAL', 'AAPL', 'AMD', 'AMZN', 'APA', 'ATVI', 'AXP', 'BABA', 'BAC', 'BUD', 'C', 'CAT',
          'CME', 'CMG', 'CSCO', 'DAL', 'DIS', 'EA', 'FB', 'GOOG', 'GS', 'HD', 'IBM', 'JNJ', 'JPM',
          'MCD', 'MSFT', 'MU', 'NEE', 'NFLX', 'NVDA', 'ORCL', 'PEP', 'PYPL', 'QQQ', 'ROKU', 'SBUX',
          'SNAP', 'SPY', 'SQ', 'TSLA', 'TWTR', 'ULTA', 'UPS', 'V', 'VXX', 'WMT', 'YUM',
          'VDE', 'XLB', 'XLI', 'VCR', 'VDC', 'XLV', 'XLF', 'VGT', 'XLC', 'XLU', 'VNQ']

# print(len(opt_column_names))
# print(len(columns_unwanted))
# print(len(columns_wanted))
# print(len(stocks))

# /\ This segment was used to sort out unique columns after i hard coded the columns i wanted
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


'''
for i in opt_column_names:
    for j in columns_wanted:
        if i == j:
            outs.append(i)
'''


# print(outs)
# print(len(outs))
# unique_list(outs)

# \/


def get_chain(stock):
    opt_lookup = TDSession.get_options_chain(
        option_chain={'symbol': stock, 'strikeCount': 50,
                      'toDate': '2021-3-26'})

    return opt_lookup


'''
def narrow_print():
    opt_lookup = get_chain('SPY')
    narrow = opt_lookup['putExpDateMap']['2020-11-27:1']['363.0'][0]
    for m in narrow.keys():
        print(m, narrow[m])
    return 0
'''


def raw_chain(raw, put_call):
    cp = f'{put_call}ExpDateMap'
    raw_data = [[]]
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
                        raw_data.append([])

                raw_data[r].append(unit)

    return raw_data


def clean_chain(raw):
    df_cp = pd.DataFrame(raw, columns=opt_column_names)
    clean = df_cp.drop(columns=columns_unwanted)

    return clean


def make_sqlite_table(table_name):
    engine = create_engine('sqlite:///Options.db', echo=False)
    table_columns = pd.DataFrame(columns=columns_wanted)
    table_columns.to_sql(table_name, con=engine)

    return 0


def add_rows(clean_data, table_name):
    engine = create_engine('sqlite:///Options.db', echo=False)
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


pulls = 0
failed_pulls = 0


def get_next_chains():
    x = 0
    global pulls
    global failed_pulls

    for stock in stocks:
        error = False
        try:
            chain = get_chain(stock)
        except (exceptions.ServerError, exceptions.GeneralError, exceptions.ExdLmtError):
            error = True
            failed_pulls = failed_pulls + 1
            print('A server error occurred')

        if not error:
            try:
                add_rows(clean_chain(raw_chain(chain, 'call')), 'calls')
                pulls = pulls + 1

            except ValueError:
                print(f'{x}: Calls for {stock} did not have values for this iteration')
                failed_pulls = failed_pulls + 1

            try:
                add_rows(clean_chain(raw_chain(chain, 'put')), 'puts')
                pulls = pulls + 1

            except ValueError:
                print(f'{x}: Puts for {stock} did not have values for this iteration')
                failed_pulls = failed_pulls + 1

        print(f'{x}: {stock}')
        x = x + 1
        time.sleep(2)

    return 0


def start():
    pull_count = 0
    end_t = 1600

    while get_time_now() < end_t:
        get_next_chains()
        pull_count = pull_count + 1
        print(pull_count)

    print('option market closed')

    print(f'failed_pulls: {failed_pulls}')
    print(f'pulls: {pulls}')

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
    while get_time_now() < 930:
        print(f'{get_time_now()}: Market closed.')
        time.sleep(5)
    start()
    return 0


main()
