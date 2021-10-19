from pandas import DataFrame, Timestamp, Timedelta
import numpy as np
from stocks import StockManager
from utils.singleton import Singleton
from utils.exception import TradeException, TradeManagerException


class Trade(dict):
    """
    Trade Class
    """
    __sm = StockManager()

    BUY = True
    SELL = False

    def __init__(self, stock_symbol, timestamp, quantity, buy_or_sell, trade_price):
        """
        Class Constructor
        :param stock_symbol: Symbol of the given stock
        :param timestamp: Storing the time of the trade
        :param quantity: Quantity of the stock
        :param buy_or_sell: The stocks are bought or sold
        :param trade_price: The price of the stocks
        """
        if quantity < 0 or trade_price < 0:
            raise TradeException("Invalid Input")

        self["stock"] = self.__sm[str(stock_symbol)]
        self["timestamp"] = Timestamp(timestamp)
        self["quantity"] = int(quantity)
        self["buy_or_sell"] = bool(buy_or_sell)
        self["trade_price"] = int(trade_price)

    @classmethod
    def create_trade(cls, stock_symbol, quantity, buy_or_sell, trade_price):
        """
        Create Trades using Trade time
        :param stock_symbol: Symbol of the given stock
        :param quantity: Quantity of the stock
        :param buy_or_sell: The stocks are bought or sold
        :param trade_price:The price of the stocks
        :return: Trade Class Object
        """
        return cls(stock_symbol, Timestamp.now(), quantity, buy_or_sell, trade_price)


class GlobalBeverageCorporationExchangeTradeManager(metaclass=Singleton):
    """
    Singleton GBCE Trade Manager class.
    """

    def __init__(self):
        """
        Constructor for initialisation
        """

        super(GlobalBeverageCorporationExchangeTradeManager, self).__init__()
        self.__storage = []

        self.__df_storage = None
        self.__df_time = None
        self.__append_time = None

    def add(self, trade):
        """
        Add new Trade
        :param trade: Trade Class Instance
        """
        if isinstance(trade, Trade):
            self.__storage.append(trade)
            self.__append_time = Timestamp.now()
        else:
            raise TradeManagerException('Invalid trade')

    def __len__(self):
        return len(self.__storage)

    def _create_df_storage(self):
        """
        Create Panda Date Frame for analyzing data.
        Data Frame is created only when no df is available or is not updated.
        This is checked based on the append time of trade and df create time
        """
        if self.__df_time is None or self.__append_time > self.__df_time:
            self.__df_storage = DataFrame(self.__storage)
            self.__df_storage.set_index('timestamp')
            self.__df_time = Timestamp.now()

    def volume_weighted_stock_price(self, interval):
        """
        Find Volume Weighted Stock Price based on last interval in seconds
        :param interval: Interval in seconds
        """
        try:
            self._create_df_storage()
            current_df = self.__df_storage[
                self.__df_storage.timestamp >= Timestamp.now() - Timedelta(seconds=int(interval))]
            return sum(current_df.quantity * current_df.trade_price) / sum(current_df.quantity)
        except TypeError as te:
            raise TradeManagerException('Invalid time interval: {0}'.format(te))

    def all_share_index(self):
        """
        Geometric mean of Volume Weighted Stock Price of all Shares
        """
        try:
            self._create_df_storage()
            return np.exp(np.sum(self.__df_storage.quantity * np.log(self.__df_storage.trade_price)) / np.sum(
                self.__df_storage.quantity))
        except ZeroDivisionError:
            return 0.0
