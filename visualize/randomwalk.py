# Trade options based off randomly generated stock movement with BSM

from math import log, sqrt, exp
from scipy.stats import norm
import matplotlib.pyplot as plt
import random
import sqlite3

start = 115
price = start
cash = 1000
cash = int(cash)
yesterday_cash = 0
yesterday_price = start
yesterday_IV = 0
days = 0
mood = 0

net_liquid = 0
commission = 0
loot = 0

calls_strikes = []
puts_strikes = []
calls = []
puts = []
strangles = []
option_ladder = [100, 101, 102.5, 104, 105, 106, 107.5, 108.75,
                 110, 111.25, 112.50, 113.75, 115, 116.25, 117.50,
                 118.75, 120, 121.25, 122.50, 123.75, 125, 126.25,
                 127.5, 128.75, 130]
temp_c = 0
temp_p = 0
temp_total = 0
tick_count = 0
minutes_per_day = 390
total_ticks = minutes_per_day
total_dollar_movements = []

ticks = []
for i in range(total_ticks):
    ticks.append(i)


# Call and Put classes using 2 different BSM implementations to value premium()
class Call:

    def __init__(self, stock, strike, ttl, risk, sigma):
        self.stock = float(stock)
        self.strike = strike
        self.ttl = ttl
        self.risk = risk
        self.sigma = sigma
        self.d1num = (log(self.stock / self.strike) + (self.risk + .5 * self.sigma ** 2) * self.ttl)
        self.d1 = self.d1num / (self.sigma * sqrt(self.ttl))
        self.d2 = self.d1 - self.sigma * sqrt(self.ttl)

    def premium(self):
        d1 = ((log(self.stock / self.strike) +
               (self.risk + 0.5 * self.sigma ** 2) * self.ttl) /
              (self.sigma * sqrt(self.ttl)))
        d2 = ((log(self.stock / self.strike) +
               (self.risk - 0.5 * self.sigma ** 2) * self.ttl) /
              (self.sigma * sqrt(self.ttl)))
        value = (self.stock * norm.cdf(d1, 0.0, 1.0) -
                 self.strike * exp(-self.risk * self.ttl) * norm.cdf(d2, 0.0, 1.0))
        return value

    def delta(self):
        delta = (norm.cdf(self.d1))
        return delta

    def gamma(self):
        gamma = norm.pdf(self.d1) / (self.stock * self.sigma * sqrt(self.ttl))
        return gamma

    def theta(self):
        theta = -(self.stock * norm.pdf(self.d1) * self.sigma / (2 * sqrt(self.ttl))) + (self.risk * self.strike)
        (self.risk * self.strike * exp(-self.risk * self.ttl) * norm.cdf(-self.d2))
        return theta

    def vega(self):
        vega = (self.stock * norm.pdf(self.d1) * sqrt(self.ttl))
        return vega


class Put:

    def __init__(self, stock, strike, ttl, risk, sigma):
        self.stock = float(stock)
        self.strike = strike
        self.ttl = ttl
        self.risk = risk
        self.sigma = sigma
        self.d1num = (log(self.stock / self.strike) + (self.risk + .5 * self.sigma ** 2) * self.ttl)
        self.d1 = self.d1num / (self.sigma * sqrt(self.ttl))
        self.d2 = self.d1 - self.sigma * sqrt(self.ttl)

    def premium(self):
        value = -self.stock * norm.cdf(-self.d1) + self.strike * exp(-self.risk * self.ttl) * norm.cdf(-self.d2)
        return value

    def delta(self):
        delta = -(norm.cdf(-self.d1))
        return delta

    def gamma(self):
        gamma = norm.pdf(self.d1) / (self.stock * self.sigma * sqrt(self.ttl))
        return gamma

    def theta(self):
        theta = -(self.stock * norm.pdf(self.d1) * self.sigma / (2 * sqrt(self.ttl))) + (self.risk * self.strike)
        (self.risk * self.strike * exp(-self.risk * self.ttl) * norm.cdf(-self.d2))
        return theta

    def vega(self):
        vega = (self.stock * norm.pdf(self.d1) * sqrt(self.ttl))
        return vega


def lookup_call(p, cp):
    global temp_c, temp_total, net_liquid
    temp_call = Call(p, cp, 2 / 365, .08, .40)
    temp_c = float(format(temp_call.premium(), '.2f')) * 1000
    temp_total = temp_total + temp_c

    return temp_c


def lookup_put(p, pp):
    global temp_p, temp_total, net_liquid
    temp_put = Put(p, pp, 2 / 365, .08, .40)
    # print(temp_put.delta())
    temp_p = float(format(temp_put.premium(), '.2f')) * 1000
    temp_total = temp_total + temp_p

    return temp_p


def buy_call():
    plt.axvline(linewidth=1, color='g')

    global calls, cash, net_liquid, commission

    return 0


def sell_call():
    plt.axvline(linewidth=1, color='r')

    global cash, calls, net_liquid, commission

    return 0


def buy_put():
    plt.axvline(linewidth=1, color='b')

    global puts, cash, net_liquid, commission

    return 0


def sell_put():
    plt.axvline(linewidth=1, color='p')

    global puts, cash, net_liquid, commission

    return 0


def buy_strangle(t, sp):
    plt.axvline(x=t, linewidth=1, color='orange')

    global calls, puts, cash, \
        commission, strangles, option_ladder, \
        temp_total, temp_c, temp_p, net_liquid, \
        calls_strikes, puts_strikes

    call_strike = 0
    put_strike = 0
    k = 0

    while put_strike == 0:
        if option_ladder[k] > sp:
            call_strike = option_ladder[k + 1]
            calls_strikes.append(call_strike)
            put_strike = option_ladder[k - 1]
            puts_strikes.append(put_strike)
        k = k + 1

    temp_c = lookup_call(sp, call_strike)
    temp_p = lookup_put(sp, put_strike)
    temp_total = temp_c + temp_p
    net_liquid = net_liquid + temp_total

    calls.append(temp_c)
    puts.append(temp_p)
    strangles.append(temp_total)
    cash = cash - temp_c - temp_p - 1.30

    return 0


# pull 25 puts and calls in a graph, numpy


def sell_strangle(t, sp, pair, color):
    plt.axvline(x=t, linewidth=1, color=color)

    global calls, puts, cash, \
        net_liquid, commission, \
        temp_total, temp_c, temp_p, \
        strangles, calls_strikes, puts_strikes

    temp_c = lookup_call(sp, calls_strikes[pair])
    temp_p = lookup_put(sp, puts_strikes[pair])
    temp_total = temp_c + temp_p

    cash = cash + temp_c + temp_p - 1.30
    net_liquid = net_liquid - calls[pair] - puts[pair]

    del calls[pair]
    del puts[pair]
    del strangles[pair]
    del calls_strikes[pair]
    del puts_strikes[pair]

    return 0


def alert(a):
    global net_liquid, cash, strangles, \
        temp_c, temp_p, temp_total, \
        calls_strikes, puts_strikes

    if a == 0:
        print('Trade - Loss')

    elif a == 1:
        print('Trade - Win')

    elif a == 2:
        print('Trade - Scratch')

    elif a == 3:
        print('Trade - Buy')

    else:
        print('Check')

    print(f'|Time: {i} |#: {len(strangles)}|')
    print(f'|Call: {int(temp_c)} + Put: {int(temp_p)}| \n|Total: {int(temp_total)}|')
    if a == 3:
        print(f'|C strike:    {calls_strikes[0]}| \n|P Strike:    {puts_strikes[0]}|')

    print(f'|Net Liquidity:  {int(net_liquid)}|')
    print(f'|Buying Power: {int(cash)}| \n')

    return 0


def volatility(m):
    if m == 0:
        return random.uniform(-.00075, .0007)
    elif m == 1:
        return random.uniform(-.0007, .00075)
    else:
        return random.uniform(-.00075, .00075)


d = 2  # change int for how many days to simulate
while days < d:
    print('______________________________________________________')
    print(f'Day:  {days + 1} \n')

    conn = sqlite3.connect('walk_training.db')
    con = conn.cursor()
    con.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='stocks' ''')

    # if the count is 1, then table exists
    if con.fetchone()[0] != 1:
        con.execute('CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)')

    yesterday_cash = cash
    yesterday_price = price

    prices = []
    averages = []
    total_dollar_movement = 0

    moods = [0] * 45 + [1] * 45 + [2] * 5
    moods = random.choice(moods)

    if moods == 0:
        plt.title('a random walk: Bear Day')

    elif moods == 1:
        plt.title('a random walk: Bull Day')

    else:
        plt.title('a random walk: Choppy Day')

    # con.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    conn.commit()

    for i in range(total_ticks):
        change = volatility(moods)
        price = price + (price * change)
        prices.append(price)
        total_dollar_movement = total_dollar_movement + abs(change)
        temp_avg_total = 0


        denominator = min(len(prices), 50)


        averages.append(sum(prices[-denominator:]) / denominator)

        # if tick_count % 1 == 0 or tick_count == total_ticks - 1:

        if tick_count == 0:
            buy_strangle(0, price)
            alert(3)

        if len(strangles) > 0:
            temp_total = 0
            temp_c = lookup_call(price, calls_strikes[0])
            temp_p = lookup_put(price, puts_strikes[0])

            if temp_total < (strangles[0] - (strangles[0] * .15)):
                sell_strangle(tick_count, price, 0, 'r')
                alert(0)
            elif temp_total > (strangles[0] + (strangles[0] * .10)):
                sell_strangle(tick_count, price, 0, 'g')
                alert(1)
            elif tick_count == (total_ticks - 1):
                sell_strangle(total_ticks, price, 0, 'orange')
                alert(2)
            else:
                if tick_count != tick_count:
                    alert(4)

            temp_total = 0

        tick_count = tick_count + 1

    total_dollar_movements.append(int(total_dollar_movement))

    loot = loot + (cash - yesterday_cash)
    days = days + 1
    tick_count = 0
    print(f'Days left: {d - days} Total loot: {int(loot)} Total Moves: {int(total_dollar_movement)}')
    print('______________________________________________________')

    plt.plot(ticks, prices, label='AAPL')
    plt.plot(ticks, averages, label='movingAvg')
    plt.legend()
    plt.show()
    conn.close()

'''
conn = sqlite3.connect('walk_training.db')
con = conn.cursor()
for row in con.execute('SELECT * FROM stocks ORDER BY price'):
    print(row)
conn.close()
'''
