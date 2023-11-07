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

    def get_session(self):
        if not self.session:
            self.session = HTTP(
                testnet=False,
                api_key=API_KEY,
                api_secret=SECRET_KEY,
            )

    # def get_current_rates(self):
    #     """Returns current rates for the """
    #     exchange = bybit()
    #     params = {
    #         'symbol': self.master_symbol,
    #     }
    #     # exchange.fetch_future_markets(params)
    #     exchange.fetchMarkets()
    #     order_book = exchange.fetchOrderBook(self.master_symbol)
    #     print(order_book)
    #     print(exchange)
    #     return exchange

    def get_last_rates(self) -> float | None:
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
        """interval	true	string	Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W"""
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
            return pandy
        else:
            return array[:, 4].astype(float)


if __name__ == '__main__':
    bybitBTC = BybitExchangeRates("BTCUSDH24")
    bybitETH = BybitExchangeRates("ETHUSDH24")

    print(bybitBTC.get_last_rates(), bybitETH.get_last_rates())
    btc = bybitBTC.get_historical_rates(15, 1000, pandas_format_flag=False)
    eth = bybitETH.get_historical_rates(15, 1000, pandas_format_flag=True)
    print(btc, "\n", eth)
