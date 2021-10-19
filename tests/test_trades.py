import pytest
from stocks import StockManager, Stock
from trades import Trade, GlobalBeverageCorporationExchangeTradeManager
from utils.exception import TradeException

HEADER = ['symbol', 'type', 'last_dividend', 'fixed_dividend', 'par_value']
STOCKS = [['TEA', 'Common', 0, None, 100], ['POP', 'Common', 8, None, 100],
          ['ALE', 'Common', 23, None, 60], ['GIN', 'Preferred', 8, 0.02, 100],
          ['JOE', 'Common', 13, None, 250]]


class TestTrades:

    @classmethod
    def setup(cls):
        cls._sm = StockManager()
        cls._sm.create_stocks(HEADER, STOCKS)

    @pytest.mark.parametrize("stock_symbol, timestamp, quantity, buy_or_sell, trade_price",
                             [('TEA', '2015-JAN-21 00:12:11', 1000, Trade.BUY, 1000),
                              ('ALE', '2015-JAN-21 00:12:11', 1000, Trade.SELL, 1000)])
    def test_create_trade_with_constructor(self, stock_symbol, timestamp,
                                           quantity, buy_or_sell, trade_price):
        t = Trade(stock_symbol, timestamp, quantity, buy_or_sell, trade_price)
        assert isinstance(t, Trade)

    @pytest.mark.parametrize("stock_symbol, timestamp, quantity, buy_or_sell, trade_price",
                             [('TEA', '2015-JAN-21 00:12:11', 1000, Trade.BUY, -1000),
                              ('ALE', '2015-JAN-21 00:12:11', -1000, Trade.SELL, 1000)])
    def test_invalid_trade(self, stock_symbol, timestamp,
                           quantity, buy_or_sell, trade_price):
        with pytest.raises(TradeException):
            Trade(stock_symbol, timestamp, quantity, buy_or_sell, trade_price)

    @pytest.mark.parametrize("stock_symbol, quantity, buy_or_sell, trade_price",
                             [('TEA', 1000, Trade.BUY, 1000),
                              ('ALE', 1000, Trade.SELL, 1000)])
    def test_create_trade_with_method(self, stock_symbol,
                                      quantity, buy_or_sell, trade_price):
        t = Trade.create_trade(stock_symbol,
                               quantity, buy_or_sell, trade_price)
        assert isinstance(t, Trade)

    @classmethod
    def teardown(cls):
        del cls._sm


class TestGlobalBeverageCorporationExchangeTradeManager:
    @classmethod
    def setup_class(cls):
        cls._sm = StockManager()
        cls._sm.create_stocks(HEADER, STOCKS)

    @classmethod
    def teardown_class(cls):
        del cls._sm

    def test_singleton(self):
        tm1 = GlobalBeverageCorporationExchangeTradeManager()
        tm2 = GlobalBeverageCorporationExchangeTradeManager()
        assert tm1 is tm2
        del tm1
        del tm2

    @pytest.mark.parametrize("stock_symbol, timestamp, quantity, buy_or_sell, trade_price",
                             [('TEA', '2015-JAN-21 00:12:11', 1000, Trade.BUY, 1000),
                              ('ALE', '2015-JAN-21 00:12:11', 1000, Trade.SELL, 1000)])
    def test_add_trade(self, stock_symbol, timestamp,
                       quantity, buy_or_sell, trade_price):
        t1 = Trade(stock_symbol, timestamp, quantity, buy_or_sell, trade_price)
        gbce = GlobalBeverageCorporationExchangeTradeManager()
        gbce.add(t1)
        assert (len(gbce), 1)



