# from datetime import time
import asyncio
from time import sleep, time

from src.ethtracker.exch_rates import BybitExchangeRates
from config.config import FIRST_CRYPTO_SYMBOL, SECOND_CRYPTO_SYMBOL, INTERVAL, NUMBER_OF_SAMPLES
from config.config import ALARM_THRESHOLD, TIME_THRESHOLD, BAD_CORRELATION_THRESHOLD, VERBOSE_MODE, POSSIBLE_TIMINGS
import statsmodels.api as statmodel
from statsmodels.iolib.summary2 import Summary
from src.ethtracker.myexeption import ConnectionLostError

from src.ethtracker.functions import detect_best_timing


class Prediction:

    def __init__(self):
        self.requester_btc = BybitExchangeRates(FIRST_CRYPTO_SYMBOL)
        self.requester_eth = BybitExchangeRates(SECOND_CRYPTO_SYMBOL)
        self.history_btc = []
        self.history_eth = []
        self.btc_influence: float = 0
        self.last_btc_price = 0
        self.last_eth_price = 0
        self.eth_cumulative_change = 0
        self.begin_time = time()
        self.floating_tail: list[dict] = []  # list of measurements of own prices (for last hour)

    def __repr__(self):
        return "Prediction()"

    def get_data(self):
        try:
            history_btc = self.requester_btc.get_historical_rates(INTERVAL, NUMBER_OF_SAMPLES)
            history_eth = self.requester_eth.get_historical_rates(INTERVAL, NUMBER_OF_SAMPLES)
            self.history_btc = history_btc
            self.history_eth = history_eth
            self.btc_influence: float = self.calculate_influence()
            self.last_btc_price = self.history_btc[0]
            self.last_eth_price = self.history_eth[0]
        except ConnectionLostError:
            pass

    def calculate_influence(self):
        # if correlation < BAD_CORRELATION_THRESHOLD needed to recalculate
        model_sq = statmodel.OLS(self.history_eth, statmodel.add_constant(self.history_btc)).fit()
        btc_influence = model_sq.params[1]
        print("Change influence coef:", btc_influence)
        return btc_influence

    async def rebuild_models(self):
        """
        Recalculate all models and choose the best model
        Push me only in a case of emergency - I need much time for calculating"""
        interval, samples, coef = detect_best_timing(self.requester_btc, self.requester_eth, POSSIBLE_TIMINGS)
        if coef > BAD_CORRELATION_THRESHOLD:
            try:
                history_btc = self.requester_btc.get_historical_rates(interval, samples)
                history_eth = self.requester_eth.get_historical_rates(interval, samples)
                self.history_btc = history_btc
                self.history_eth = history_eth
                self.btc_influence = self.calculate_influence()
            except ConnectionLostError:
                 # very strange situation
                 print("""We have done samples but cannot recalculate influence. 
                       We have to try again. Wait 10 sec....""")
                 await asyncio.sleep(10)
                 await self.rebuild_models()
        else:
            print("We have to wait for a better time. Wait 15 sec....")
            await asyncio.sleep(15)
            await self.rebuild_models()

    @property
    def status(self):
        return {"ETH price": self.last_eth_price,
                "cumulative changes": self.eth_cumulative_change,
                "BTC influence": self.btc_influence}

    def set_zero_parameters(self):
        self.eth_cumulative_change = 0
        self.begin_time = time()

    def send_message(self, current, eth_percent_change):
        print("=================================")
        print("Attention! Current own ETH price is over threshold!")
        print("Current price", current)
        print(f"Comulative: {self.eth_cumulative_change:10.6f}  {eth_percent_change:4.6f}% ")
        print(self.floating_tail)
        print("================================")

    def add_to_floating_tail(self, cur_time, cur_value):
        correction = 0
        del_counter = 0
        self.floating_tail.append({"time": cur_time, "value": cur_value})
        for point in self.floating_tail:
            if point["time"] <= cur_time - TIME_THRESHOLD:
                correction += point["value"]
                del_counter += 1
            else:
                break
        if del_counter > 0:
            self.floating_tail = self.floating_tail[del_counter:]
            # for point in self.floating_tail:
            #     point["value"] -= correction
        return cur_value - correction

    def current_handler(self):
        try:
            # One way
            # current_btc = self.requester_btc.get_last_rates()
            # current_eth = self.requester_eth.get_last_rates()

            # Alternative way - not crossing with get_historical_data for better async working
            current_btc = self.requester_btc.get_current_rates_ccxt()
            current_eth = self.requester_eth.get_current_rates_ccxt()
        except ConnectionLostError as e:
            if VERBOSE_MODE:
                print(f"{time():10.2f} Error {e}. Seу you on the next step")
            return
        btc_delta = (current_btc - self.last_btc_price)
        eth_delta = (current_eth - self.last_eth_price)
        eth_own_delta = eth_delta - btc_delta * self.btc_influence  # Own ETH changes

        # pay attention - if we have been working more TIME_THRESHOLD
        # self.eth_cumulative_change will increment taking into account correction
        eth_own_delta_plus = self.add_to_floating_tail(time(), eth_own_delta)
        self.eth_cumulative_change += eth_own_delta_plus

        eth_percent_change = self.eth_cumulative_change / current_eth
        if VERBOSE_MODE:
            print(
                f"{time():10.2f}   Current ETH: {current_eth:12.6f},   Delta BTC:, {btc_delta:10.4f}"
                f",    Delta ETH: {eth_delta:10.4f}"
                f",    Own ETH changes:, {eth_own_delta:10.6f}"
                f",    Comulative: {self.eth_cumulative_change:10.6f}, {eth_own_delta_plus:10.6f}  {100 * eth_percent_change:4.6f}% ")
            # print([x['value'] for x in self.floating_tail]) # for debug decrease TIME_THRESHOLD to 60 or less sec
        if abs(eth_percent_change) >= ALARM_THRESHOLD:
            self.send_message(current_eth, eth_percent_change)
            self.set_zero_parameters()
            # we are in fire - we need to reincarnate
            self.rebuild_models()

        # work_time = time() - self.begin_time
        # if work_time > TIME_THRESHOLD:
        #     self.set_zero_parameters()
            # Actually this is not entirely fair, we have to remember the data from an hour ago
            # But for version w/o database let it be as is
            # Maximum what we might lose less 1 percent, but we wait for a huge moving

        self.last_eth_price = current_eth
        self.last_btc_price = current_btc


def main_process():
    prediction = Prediction()
    while True:
        sleep(1)
        prediction.current_handler()


if __name__ == '__main__':
    main_process()
