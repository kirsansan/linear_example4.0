from src.ethtracker.hand_made_correlation import calculate_correlation


def detect_best_timing(handle_btc, handle_eth, test_timing: list[dict]) -> (int, int):
    for enum, params in enumerate(test_timing):
        clear_btc = handle_btc.get_historical_rates(params['interval'], params['num_of_samples'], False)
        clear_eth = handle_eth.get_historical_rates(params['interval'], params['num_of_samples'], False)
        test_timing[enum]['coef']: float = calculate_correlation(clear_eth, clear_btc)
    test_timing.sort(key=lambda x: x['coef'], reverse=True)
    return test_timing[0]['interval'], test_timing[0]['num_of_samples'], test_timing[0]['coef']
