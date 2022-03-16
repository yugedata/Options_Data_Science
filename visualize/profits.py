
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def graph_profits(excel_file):
    df = pd.read_excel(excel_file)
    u_dates = np.unique(df["bot_date"])
    # df = df[df['Days_left'] != 0]
    # df = df[~df.C.str.split("_")[1].contains("P")]

    x = [x/10 for x in range(1, 200, 1)]
    y = []
    yy = []
    for i in x:
        tf = df[(df['bot_price'] < i)]
        #tf = tf[(tf['bot_price'] <= 2)]
        tf = tf[(tf['bot_date'] >= 20220305)]
        tf = tf[(tf['Days_left'] > 25)]
        # print(tf['Contract'])

        cost = round(np.sum(np.array(tf['bot_price'])) * 100, 3)
        y.append(cost)
        pl = round(np.sum(np.array(tf['TotalChange'])) * 100, 3)
        yy.append(pl)

    fig, axs = plt.subplots(2)

    axs[0].plot(x, y)
    axs[1].plot(x, yy)
    plt.show()

    return True


graph_profits("portfolio_20220310.xlsx")


# df = pd.read_csv("optionable.csv")
# opt = np.array(df['Symbol'])
# for i in opt:
#     if '\\xa0' in i:
#         print(i[4:])
#     else:
#         print(i)
