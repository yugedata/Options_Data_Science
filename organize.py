"""
[1] This script needs to take the raw data in all options
files and separate tem into stock tables because now its only
2 massive tables for calls and puts

[2] When this is done a version 2 needs to be make so that
the OG miner will put the options data into stock tables

[a] for i in call/put table patition sym to find equity
[b] put i in {equity} call/put table in new date file
[c]
[d]
"""
import sqlite3
import os
import pandas as pd

# file_date = ""

read_directory = '/Users/Sato/Documents/PycharmProjects/open_interest/Data/'
write_directory = '/Users/Sato/Documents/PycharmProjects/open_interest/Data_Library/'
substring = '_'

columns = ('putCall', 'symbol', 'exchangeName', 'bid', 'ask', 'last',
            'highPrice', 'lowPrice', 'openPrice', 'closePrice', 'totalVolume', 'quoteTimeInLong', 'netChange',
            'volatility', 'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue',
            'theoreticalVolatility', 'strikePrice', 'expirationDate', 'daysToExpiration', 'percentChange')

# sorting tickers is working but writing to new file is not
for filename in os.listdir(read_directory):
    if filename.endswith(".db"):
        print(filename)
        con = sqlite3.connect(f'{read_directory}{filename}')
        conn = sqlite3.connect(f'{write_directory}{filename}')
        c = con.cursor()
        c.execute("SELECT * FROM calls")
        cu = con.cursor()
        # res = c.execute("SELECT name FROM sqlite_master WHERE type='table';")

        for row in c:
            temp_contract = row[2]
            equity = temp_contract.partition(substring)[0]
            sqlite_insert = f'''INSERT INTO c{equity} ('putCall', 'symbol', 'exchangeName', 'bid', 'ask', 'last', 
            'highPrice', 'lowPrice', 'openPrice', 'closePrice', 'totalVolume', 'quoteTimeInLong', 'netChange', 
            'volatility', 'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue', 
            'theoreticalVolatility', 'strikePrice', 'expirationDate', 'daysToExpiration', 'percentChange') 
            values {row[1:]} '''

            try:
                cu.execute(sqlite_insert)
            except sqlite3.OperationalError:
                cu.execute(f'''CREATE TABLE IF NOT EXISTS c{equity} {columns}''')
            finally:
                cu.execute(sqlite_insert)
            conn.commit()
        c.close()
        cu.close()

# possible fix: use sqlachemy from mining script
for filename in os.listdir(read_directory):
    if filename.endswith(".db"):
        print(filename)
        con = sqlite3.connect(f'{read_directory}{filename}')
        conn = sqlite3.connect(f'{write_directory}{filename}')
        c = con.cursor()
        c.execute("SELECT * FROM puts")
        cu = con.cursor()
        # res = c.execute("SELECT name FROM sqlite_master WHERE type='table';")

        for row in c:
            temp_contract = row[2]
            equity = temp_contract.partition(substring)[0]
            sqlite_insert = f'''INSERT INTO p{equity} ('putCall', 'symbol', 'exchangeName', 'bid', 'ask', 'last', 
            'highPrice', 'lowPrice', 'openPrice', 'closePrice', 'totalVolume', 'quoteTimeInLong', 'netChange', 
            'volatility', 'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue', 
            'theoreticalVolatility', 'strikePrice', 'expirationDate', 'daysToExpiration', 'percentChange') 
            values {row[1:]} '''

            try:
                cu.execute(sqlite_insert)
            except sqlite3.OperationalError:
                cu.execute(f'''CREATE TABLE IF NOT EXISTS p{equity} {columns}''')
                cu.execute(sqlite_insert)
            conn.commit()
        c.close()
        cu.close()


