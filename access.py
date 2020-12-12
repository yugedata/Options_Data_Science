from sqlalchemy import create_engine
import _sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

conn = _sqlite3.connect('Options.db')
c = conn.cursor()


def test():
    c.execute('SELECT * FROM puts WHERE rowid = 1')
    one = c.fetchone()

    for j in one:
        print(j)

    return 0


# test()

check, count = [], 0
y_yes = []

for row in c.execute(f'SELECT quoteTimeInLong FROM puts WHERE symbol = \'AAPL_121120P123\''):
    for t in row:
        temp = int(t) // 100000
        # print(temp)
        check.append(temp)

go = check[0]
end = check[-1]

x_time = np.arange(start=go, stop=end)

for n in x_time:
    if n == check[count]:
        count = count + 1
        y_yes.append(1)
    else:
        y_yes.append(.5)


def equa_distanced():
    n_bins = [go]
    next_bin = go
    diff = (end - go) // 20
    count_2 = 0
    while count_2 < 20:
        n_bins.append(next_bin)
        next_bin = next_bin + diff
        print(next_bin)
        print(diff)
        count_2 = count_2 + 1

    return 0


columns_wanted = ['time']


def make_sqlite_table(table_name):
    engine = create_engine('sqlite:///temp.db', echo=False)
    table_columns = pd.DataFrame(columns=columns_wanted)
    table_columns.to_sql(table_name, con=engine)

    return 0


def add_rows(clean_data, table_name):
    engine = create_engine('sqlite:///temp.db', echo=False)
    clean_data.to_sql(table_name, con=engine, if_exists='append', index_label='index')

    return 0


# make_sqlite_table('Time')
# add_rows(check, 'Time')
plt.hist(x=check, bins=173, density=False)
plt.title('Minutes Captured')
plt.show()
conn.close()
