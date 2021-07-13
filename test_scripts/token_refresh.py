from sqlalchemy import create_engine
from td.client import TDClient
from datetime import datetime
from td import exceptions
import datetime
import pandas as pd
import sqlite3
import time

TDSession = TDClient(
    client_id='insert client id key',
    redirect_uri='https://127.0.0.1',
    credentials_path='path to working directory'
)

TDSession.login()
