from abc import ABC, abstractmethod
from datetime import datetime

from ccxt import bybit as bybit
from pandas import DataFrame
from pybit.unified_trading import HTTP, WebSocket
from config.config import API_KEY, SECRET_KEY
import numpy as np
import pandas as pd
from src.ethtracker.myexeption import ConnectionLostError


class ExchangeRates(ABC):

    def __init__(self, symbol: str = "BTCUSDT"):
        self.master_symbol = symbol

    @abstractmethod
    def get_last_rates(self) -> float | None:
        pass

    @abstractmethod
    def get_historical_rates(self, interval: int, number_of_samples: int, pandas_format_flag: bool = False):
        pass


class BybitExchangeRates(ExchangeRates):

    def __init__(self, symbol: str = "BTCUSDT"):
        super(BybitExchangeRates, self).__init__(symbol)
        self.session = None
        self.exchange = None

    def get_session(self):
        if not self.session:
            self.session = HTTP(
                testnet=False,
                api_key=API_KEY,
                api_secret=SECRET_KEY,
            )

    def get_exchange(self):
        if not self.exchange:
            self.exchange = bybit()

    def get_current_rates_ccxt(self) -> float:
        """Returns current rates as average between ask and bid """
        self.get_exchange()
        # exchange.fetch_future_markets(params)
        # self.exchange.fetchMarkets()
        try:
            order_book = self.exchange.fetchOrderBook(self.master_symbol)
        except Exception:
            raise ConnectionLostError("Last rates - Connection was lost")
        # print(order_book)
        # print(exchange)
        best_bid = order_book['bids'][0][0]
        best_ask = order_book['asks'][0][0]
        return float((best_ask + best_bid) / 2)

    def get_last_rates(self) -> float | None:
        """Returns the last rates in 'Close'"""
        self.get_session()
        try:
            temp_price_m = self.session.get_kline(category="linear",
                                                  symbol=self.master_symbol,
                                                  interval=1,
                                                  limit=1
                                                  )["result"]['list'][0][4]
        except:
            # print("Last rates - Connection was lost")
            raise ConnectionLostError("Last rates - Connection was lost")
        return float(temp_price_m)

    def get_historical_rates(self, interval: int, number_of_samples: int,
                             pandas_format_flag: bool = False):
        """
        interval	true	string	Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W"""
        self.get_session()
        try:
            temp_price_m = self.session.get_kline(category="linear",
                                                  symbol=self.master_symbol,
                                                  interval=interval,
                                                  limit=number_of_samples
                                                  )["result"]
        except Exception:
            # print("Historical rates - Connection was lost")
            raise ConnectionLostError("Historical rates - Connection was lost")
        array = np.array(temp_price_m['list'])
        if pandas_format_flag:
            pandy = pd.DataFrame(array[:, [0, 1, 2, 3, 4, 5, 6]],
                                 columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover'])
            pandy.set_index('Time', inplace=True)

            # Transrofm values to numeric
            for col in ('Open', 'High', 'Low', 'Close', 'Volume', 'Turnover'):
                pandy[col] = pandy[col].astype(float)
            return pandy  # it's need for data visual control while we researched the models
        else:
            return array[:, 4].astype(float)


