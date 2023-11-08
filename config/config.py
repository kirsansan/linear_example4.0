import os
# install as python-dotenv
from dotenv import load_dotenv

load_dotenv()

# Bybit support keys (need for getting historical data)
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# if you are seeing this config after March 2024
# you should probably configure next param as BTCUSDI24 oк BTCUSDJ24 ect
FIRST_CRYPTO_SYMBOL = 'BTCUSDH24'
SECOND_CRYPTO_SYMBOL = 'ETHUSDH24'
# FIRST_CRYPTO_SYMBOL = 'BTCUSDT'  # open it for more dynamic changes
# SECOND_CRYPTO_SYMBOL = 'ETHUSDT'
# for binance use symbols like BTCUSD_240329 ... and etc

INTERVAL = 15  # interval between samples. default is 15
NUMBER_OF_SAMPLES = 1000  # number of samples. default is 1000

ALARM_THRESHOLD = 0.01  # 0.01 = one percent
BAD_CORRELATION_THRESHOLD = 0.72  # see explanation in research.py
TIME_THRESHOLD = 3600  # 3600  # default 60*60 seconds = 1 hour

VERBOSE_MODE = True  # to print or not to print - that is the question
REBUILD_MODELS_TIME = 60  # seconds. default = 60*60; if you don't want rebuilding - set 0

# This list may contain extended intervals and numbers of samples
POSSIBLE_TIMINGS = [{'interval': 5, 'num_of_samples': 200},
                    {'interval': 15, 'num_of_samples': 200},
                    {'interval': 360, 'num_of_samples': 200},
                    {'interval': 5, 'num_of_samples': 500},
                    {'interval': 15, 'num_of_samples': 500},
                    {'interval': 360, 'num_of_samples': 500},
                    {'interval': 5, 'num_of_samples': 1000},
                    {'interval': 15, 'num_of_samples': 1000},
                    {'interval': 360, 'num_of_samples': 1000}]

ENV_TYPE = os.getenv('ENV_TYPE')  # local as default

if ENV_TYPE == 'local':
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PORT = os.getenv('POSTGRES_PORT')
    DB_BASE_NAME = os.getenv('POSTGRES_BASE')
    DB_HOST = 'localhost'
elif ENV_TYPE == 'external-with-servers-postgres':
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_USER = 'postgres'
    DB_PORT = '5432'
    DB_BASE_NAME = os.getenv('POSTGRES_BASE')
    DB_HOST = 'localhost'
else:
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PORT = int(os.getenv('POSTGRES_PORT'))
    DB_BASE_NAME = os.getenv('POSTGRES_BASE')
    DB_HOST = os.getenv('POSTGRES_HOST')
