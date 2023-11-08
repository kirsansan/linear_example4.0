from src.ethtracker.exch_rates import BybitExchangeRates
import pytest
from unittest.mock import patch


class TestBybitExchangeRates:

    def test_get_current_rates_ccxt(self):
        obj = BybitExchangeRates()
        result = obj.get_current_rates_ccxt()
        assert result is not None

    def test_get_last_rates(self):
        obj = BybitExchangeRates()
        result = obj.get_last_rates()
        assert result is not None

    def test_get_history(self):
        obj = BybitExchangeRates()
        result1 = obj.get_historical_rates(1, 5, False)
        result2 = obj.get_historical_rates(1, 10, True)
        assert result1.all() is not None
        assert len(result1) == 5
        assert result2.all() is not None
