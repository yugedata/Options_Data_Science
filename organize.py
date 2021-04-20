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
