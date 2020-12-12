from sqlalchemy import create_engine
from td.client import TDClient
from datetime import datetime
from td.exceptions import ServerError
import datetime
import pandas as pd
import sqlite3
import time

TDSession = TDClient(
    client_id='JPAK1337',
    redirect_uri='http://127.0.0.1/',
    credentials_path='C:\\Users\\Josh\\Documents\\TradingCode\\Options_Data_Science\\token.json'
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


opt_column_names = ['putCall', 'symbol', 'description', 'exchangeName', 'bid', 'ask', 'last', 'mark', 'bidSize',
                    'askSize', 'bidAskSize', 'lastSize', 'highPrice', 'lowPrice', 'openPrice', 'closePrice',
                    'totalVolume', 'tradeDate', 'tradeTimeInLong', 'quoteTimeInLong', 'netChange', 'volatility',
                    'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue', 'theoreticalOptionValue',
                    'theoreticalVolatility', 'optionDeliverablesList', 'strikePrice', 'expirationDate', 'daysToExpiration',
                    'expirationType', 'lastTradingDay', 'multiplier', 'settlementType', 'deliverableNote',
                    'isIndexOption', 'percentChange', 'markChange', 'markPercentChange', 'mini', 'inTheMoney', 'nonStandard']

columns_unwanted = ['description', 'mark', 'bidSize', 'askSize', 'bidAskSize', 'lastSize', 'tradeDate',
                    'tradeTimeInLong', 'theoreticalOptionValue', 'optionDeliverablesList',
                    'expirationType', 'lastTradingDay', 'multiplier', 'settlementType', 'deliverableNote',
                    'isIndexOption', 'markChange', 'markPercentChange', 'nonStandard', 'inTheMoney', 'mini']

columns_wanted = ['putCall', 'symbol', 'exchangeName', 'bid', 'ask', 'last', 'highPrice',
                  'lowPrice', 'openPrice', 'closePrice', 'totalVolume', 'quoteTimeInLong',
                  'netChange', 'volatility', 'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue',
                  'theoreticalVolatility', 'strikePrice', 'expirationDate', 'daysToExpiration',  'percentChange']

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
                      'toDate': '2021-2-28'})

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


#
def add_rows(clean_data, table_name):
    engine = create_engine('sqlite:///Options.db', echo=False)
    clean_data.to_sql(table_name, con=engine, if_exists='append', index_label='index')

    return 0


def delete_db_table(table):
    conn = sqlite3.connect('options.db')
    con = conn.cursor()
    con.execute(f'DROP TABLE {table}')
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
        except ServerError:
            error = True
            failed_pulls = failed_pulls + 1
            print('A server error occurred')

        if not error:
            try:
                add_rows(clean_chain(raw_chain(chain, 'call')), 'calls')
                pulls = pulls + 1

            except (ValueError, ServerError):
                print(f'{x}: Calls for {stock} did not have values for this iteration')
                failed_pulls = failed_pulls + 1

            try:
                add_rows(clean_chain(raw_chain(chain, 'put')), 'puts')
                pulls = pulls + 1

            except (ValueError, ServerError):
                print(f'{x}: Puts for {stock} did not have values for this iteration')
                failed_pulls = failed_pulls + 1

        print(f'{x}: {stock}')
        x = x + 1
        time.sleep(2)

    return 0


def start():
    pull_count = 0
    end_t = 1600

    while get_time_now():
        get_next_chains()
        pull_count = pull_count + 1
        print(pull_count)

    print('option market closed')

    print(f'failed_pulls: {failed_pulls}')
    print(f'pulls: {pulls}')

    return 0


# |SQLite management| #
#
#make_sqlite_table('puts')  # inputs: puts|calls
# add_rows(clean_chain(raw_chain(get_chain('SPY'), 'put')), 'puts')  # raw_chain(,'put|call')), 'puts|calls')
# delete_db_table('calls')
# delete_db_table('puts')
show_db_table('puts')
show_db_table('calls')


def main():
    start()
    return 0

#main()
