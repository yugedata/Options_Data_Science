from sqlalchemy import create_engine
from td.client import TDClient
from datetime import datetime
from td.exceptions import ServerError
import datetime
import pandas as pd
import sqlite3
import time

TDSession = TDClient(
    client_id='AYGTNN1VCCC3GV7SBFAGT3SZC8AXEPBE',
    redirect_uri='https://172.0.0.1',
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


test_quote_time_epoch = test_quotes_2D['AMD']['regularMarketTradeTimeInLong']
human_time(test_quote_time_epoch)


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

print(len(opt_column_names))
print(len(columns_unwanted))
print(len(columns_wanted))
print(len(stocks))


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


for i in opt_column_names:
    for j in columns_wanted:
        if i == j:
            outs.append(i)

print(outs)
print(len(outs))
unique_list(outs)

# \/


def get_chain(s):
    opt_lookup = TDSession.get_options_chain(
        option_chain={'symbol': s, 'strikeCount': 50,
                      'toDate': '2021-2-28'})

    return opt_lookup


def narrow_print():
    opt_lookup = get_chain('SPY')
    narrow = opt_lookup['putExpDateMap']['2020-11-27:1']['363.0'][0]
    for m in narrow.keys():
        print(m, narrow[m])
    return 0


