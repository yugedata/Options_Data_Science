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
