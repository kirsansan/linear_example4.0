from src.ethtracker.exch_rates import BybitExchangeRates
from config.config import FIRST_CRYPTO_SYMBOL, SECOND_CRYPTO_SYMBOL, POSSIBLE_TIMINGS, BAD_CORRELATION_THRESHOLD
import matplotlib.pyplot as plt
import statsmodels.api as statmodel

from src.ethtracker.functions import detect_best_timing
from src.ethtracker.hand_made_correlation import calculate_correlation
from statsmodels.iolib.summary2 import Summary
from sklearn import linear_model
import numpy as np
from src.ethtracker.decorators import light_print_time_to_work


@light_print_time_to_work
def get_np_correlation(interval, number_of_samples):
    btc = data_btc.get_historical_rates(interval, number_of_samples, True)
    eth = data_eth.get_historical_rates(interval, number_of_samples, True)
    correlation = eth[['Close']].corrwith(btc['Close'], axis=0, numeric_only=True)
    # print('Pandas Correlation: ', correlation)
    return correlation


@light_print_time_to_work
def get_my_correlation(interval, number_of_samples):
    clear_btc = data_btc.get_historical_rates(interval, number_of_samples, False)
    clear_eth = data_eth.get_historical_rates(interval, number_of_samples, False)
    my_correlation = calculate_correlation(clear_eth, clear_btc)
    # print('My Linear Correlation: ', my_correlation)
    return my_correlation


if __name__ == '__main__':
    is_you_want_to_draw = True
    data_btc = BybitExchangeRates(FIRST_CRYPTO_SYMBOL)
    data_eth = BybitExchangeRates(SECOND_CRYPTO_SYMBOL)

    # make sure that both methods give the same result
    print(get_np_correlation(15, 1000)['Close'])
    print(get_my_correlation(15, 1000))
    # but speed of the second method is better

    # visual testing for different lenght on samples and intervals
    test_timing = POSSIBLE_TIMINGS
    correlations = []
    if is_you_want_to_draw:
        for params in test_timing:
            clear_btc = data_btc.get_historical_rates(params['interval'], params['num_of_samples'], False)
            clear_eth = data_eth.get_historical_rates(params['interval'], params['num_of_samples'], False)
            correlations.append(calculate_correlation(clear_eth, clear_btc))

            plt.figure(figsize=(10, 6))
            plt.scatter(clear_btc, clear_eth, alpha=0.5)
            plt.title(f"Correlation ETHUSDT vs. BTCUSDT {params['interval']} with {params['num_of_samples']}")
            plt.xlabel('Price BTCUSDT')
            plt.ylabel('Price ETHUSDT')
            plt.plot([min(clear_btc), max(clear_btc)], [min(clear_eth), max(clear_eth)], color="red", linewidth=2)
            plt.grid()
            plt.show()
        # now we can see that the best correlation we have found with params 15, 1000
        print("the best result gives", max(correlations))
        # but we need max correlation at the tail of loads for better prediction
        print("the worse result gives", min(correlations))
        # therefore we have to adjust the worst result as a border (threshold) for stop making prediction
        # if linear correlation coefficient gets worse 0.72 (not strong correlation)

    new_interval, new_samples_num, new_coef = detect_best_timing(data_btc, data_eth, POSSIBLE_TIMINGS)
    print("the best timing detected with interval:", new_interval, " and number of samples:", new_samples_num)
    if new_coef < BAD_CORRELATION_THRESHOLD:
        print("It's not possible, bit I'm seeing it right now!!!!!!!")
        print(f"We lost strong correlation. Coef = {new_coef} only")
        print("We cannot work in this situation")

    # well, reload data for final display
    btc = data_btc.get_historical_rates(new_interval, new_samples_num, True)
    eth = data_eth.get_historical_rates(new_interval, new_samples_num, True)
    # one more test
    # Build regression model
    model_sq = statmodel.OLS(eth['Close'], statmodel.add_constant(btc['Close'])).fit()
    result_for_print: Summary = model_sq.summary()
    print("Pay attention for the parameters:\n", result_for_print)
    btc_influence = model_sq.params['Close']
    print("params =", model_sq.params)
    print('Coefficient of influence of BTC on price ETH: ', btc_influence)

    # So we can calculate the value of influence of BTC on price ETH
    model_tmp = statmodel.OLS(eth['Close'], statmodel.add_constant(btc['Close'] * btc_influence)).fit()
    btc_influence_price = model_tmp.predict(statmodel.add_constant(btc['Close'] * btc_influence))
    eth['PredictedOS'] = btc_influence_price

    # Let's predict price with LinearRegression Model (similarly the same model)
    foundation = np.array(btc['Close']).reshape(-1, 1)
    model_ln = linear_model.LinearRegression()
    model_ln.fit(foundation, eth['Close'])
    eth['PredictedLN'] = model_ln.predict(foundation)

    # Finally, display the results of prediction
    fig, ax = plt.subplots()
    eth.Close.plot()
    eth.PredictedLN.plot()
    eth.PredictedOS.plot()
    # btc.Close.plot()
    plt.title('Prices of ETH')
    ax.legend(['Real close price', 'LN Predicted price', 'OS Predicted price'])
    plt.grid()
    plt.show()
