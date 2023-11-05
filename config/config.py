import os
# install as python-dotenv
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# if you are seeing this config after March 2024
# you should probably configure next param as BTCUSDI24 oк BTCUSTJ24 ect
FIRST_CRYPTO_SYMBOL = 'BTCUSDH24'
SECOND_CRYPTO_SYMBOL = 'ETHUSDH24'
# for binance use symbols like BTCUSD_240329 ... and etc

INTERVAL = 15
NUMBER_OF_SAMPLES = 1000

ALLARM_THRESHOLD = 0.01  # one percent
BAD_CORRELATION_THRESHOLD = 0.72  # see in research.py
TIME_THRESHOLD = 3600  # 60*60 seconds = 1 hour

VERBOSE_MODE = True

POSSIBLE_TIMINGS = [{'interval': 5, 'num_of_samples': 200},
                    {'interval': 15, 'num_of_samples': 200},
                    {'interval': 360, 'num_of_samples': 200},
                    {'interval': 5, 'num_of_samples': 500},
                    {'interval': 15, 'num_of_samples': 500},
                    {'interval': 360, 'num_of_samples': 500},
                    {'interval': 5, 'num_of_samples': 1000},
                    {'interval': 15, 'num_of_samples': 1000},
                    {'interval': 360, 'num_of_samples': 1000}]
