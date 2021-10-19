import pytest
from stocks import StockManager, CommonStock, PreferredStock

COMMON_STOCK_DATA = [('TEA', 0, 100),
                     ('POP', 8, 100),
                     ('ALE', 23, 60),
                     ('JOE', 13, 250)]
PREFERRED_STOCK_DATA = [('GIN', 8, 0.02, 100)]


class TestStocks:
    @pytest.mark.parametrize("symbol, last_dividend, par_value",
                             COMMON_STOCK_DATA)
    def test_create_common_stock(self, symbol, last_dividend, par_value):
        """
        Function to test Creating Common Stock
        :param symbol: Stock Symbol
        :param last_dividend: Last Dividend
        :param par_value: Par Value
        """
        c = CommonStock(symbol, last_dividend, par_value)
        assert isinstance(c, CommonStock)

    @pytest.mark.parametrize("symbol, last_dividend, fixed_dividend, par_value",
                             PREFERRED_STOCK_DATA)
    def test_create_preferred_stock(self, symbol, last_dividend,
                                    fixed_dividend, par_value):
        """
        Function to test Creating Preferred Stock
        :param symbol: Stock symbol
        :param last_dividend: Last Dividend
        :param fixed_dividend: Fixed Dividend
        :param par_value: Par Value
        """
        p = PreferredStock(symbol, last_dividend, fixed_dividend, par_value)
        assert isinstance(p, PreferredStock)

    @pytest.mark.parametrize("symbol, last_dividend, par_value, price, expected_value",
                             [('TEA', 0, 100, 100, 0),
                              ('POP', 8, 100, 100, 0.08),
                              ('ALE', 23, 60, 100, 0.23),
                              ('JOE', 13, 250, 100, 0.13)])
    def test_dividend_yield_common(self, symbol, last_dividend, par_value, price, expected_value):
        """
        Test Common Stock Dividend Yield
        :param symbol: Stock Symbol
        :param last_dividend: Last Dividend
        :param par_value: Par Value
        :param price: Price
        :param expected_value: Expected Value
        """
        c = CommonStock(symbol, last_dividend, par_value)
        assert c.dividend_yield(price) == expected_value

    @pytest.mark.parametrize("symbol, last_dividend, fixed_dividend, par_value, price, expected_value",
                             [('GIN', 8, 0.02, 100, 100, 0.02)])
    def test_dividend_yield_preferred(self, symbol, last_dividend,
                                      fixed_dividend, par_value,
                                      price, expected_value):
        """
        Test Preferred Stock Dividend Yield
        :param symbol: Stock Symbol
        :param last_dividend: Last Dividend
        :param fixed_dividend: Fixed Dividend
        :param par_value: Par Value
        :param price: Price
        :param expected_value: Expected Value
        """
        p = PreferredStock(symbol, last_dividend, fixed_dividend, par_value)
        assert p.dividend_yield(price) == expected_value

    def test_stock_manager_singleton(self):
        sm1 = StockManager()
        sm2 = StockManager()
        assert sm1 is sm2
        del sm1
        del sm2

    @pytest.mark.parametrize("symbol, last_dividend, par_value",
                             COMMON_STOCK_DATA)
    def test_adding_common_stocks(self, symbol, last_dividend, par_value):
        """
        Test Adding Common Stock
        :param symbol: Symbol
        :param last_dividend: Last Dividend
        :param par_value: Par Value
        """
        c = CommonStock(symbol, last_dividend, par_value)
        sm = StockManager()
        current_length = len(sm)
        sm[symbol] = c
        assert len(sm) == current_length + 1

    @pytest.mark.parametrize("symbol, last_dividend, fixed_dividend, par_value",
                             PREFERRED_STOCK_DATA)
    def test_adding_preferred_stocks(self, symbol, last_dividend,
                                     fixed_dividend, par_value):
        """
        Test Adding Preferred Stock
        :param symbol:
        :param last_dividend:
        :param fixed_dividend:
        :param par_value:
        """
        p = PreferredStock(symbol, last_dividend, fixed_dividend, par_value)
        sm = StockManager()
        current_length = len(sm)
        sm[symbol] = p
        assert len(sm) == current_length + 1


if __name__ == "__main__":
    pytest.main([__file__])