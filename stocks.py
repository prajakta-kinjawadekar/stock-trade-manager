from abc import ABC, ABCMeta, abstractmethod
from collections import MutableMapping
from utils.singleton import Singleton
from utils.exception import StockException, StockManagerException


class Stock(ABC):
    """
    Abstract class for stocks
    """

    def __init__(self, symbol, last_dividend, par_value):
        """
        Constructor
        :param symbol: The symbol of the given stock
        :param last_dividend: The last dividend value of the given stock
        :param par_value: Par value of the given stock
        """

        self.symbol = str(symbol)
        self.last_dividend = int(last_dividend)
        self.par_value = int(par_value)

    def pe_ratio(self, market_price):
        """
        Method to find PE Ratio
        :param market_price: The current value of the given stock
        :return: Share PE Ratio
        """
        return int(market_price) / self.last_dividend if self.last_dividend != 0 else 0

    @abstractmethod
    def dividend_yield(self, market_price):
        """
        Abstract Method as there are two different Shares -
        Preferred and Common
        :param market_price: The current value of the given stock
        """

        raise StockException('Abstract function of Stock Abstract class')


class PreferredStock(Stock):
    """
    Preferred Stock Class
    """

    def __init__(self, symbol, last_dividend, fixed_dividend, par_value):
        """
        Constructor
        :param symbol: The symbol of the given stock
        :param last_dividend: The last dividend value of the given stock
        :param fixed_dividend: The fixed divedent value of the stock
        :param par_value: Par value of the given stock
        """
        super(PreferredStock, self).__init__(symbol, last_dividend, par_value)
        self.fixed_dividend = float(fixed_dividend)

    def dividend_yield(self, market_price):
        """
        Method to calculate divident yied of Preferred Share
        :param market_price: The current value of the given stock
        """
        return self.fixed_dividend * self.par_value / market_price if market_price != 0 else 0


class CommonStock(Stock):
    """
    Common Stock Class
    """

    def __init__(self, symbol, last_dividend, par_value):
        """
        Constructor
        :param symbol: The symbol of the given stock
        :param last_dividend: The last dividend value of the given stock
        :param par_value: Par value of the given stock
        """
        super(CommonStock, self).__init__(symbol, last_dividend, par_value)

    def dividend_yield(self, market_price):
        """
        Method to calculate dividend yield of Common Share
        :param market_price: The current value of the given stock
        """
        return (self.last_dividend / market_price) if market_price != 0 else 0


class _CombinedSingletonABCMetaStockManager(ABCMeta, Singleton):
    """
    Because Stock Manager is a subclass of MutableMapping Abstract Class and MutableMapping's meta class
    is ABCMeta, we have to combine our meta classes.
    """
    pass


class StockManager(MutableMapping, metaclass=_CombinedSingletonABCMetaStockManager):
    """
    Stock Manager class.
    1) Subclass of MutableMapping
    2) Meta classes: ABCMeta and Singleton
    """

    def __init__(self):
        """
        Constructor for initialisation
        """
        self.__stocks = {}
        self.__type = {'Common': CommonStock,
                       'Preferred': PreferredStock,
                       }

    def __iter__(self):
        """
        Inherited abstract function - iterator

        @return - Iterator on the stocks symbols!!!!
        """
        return iter(self.__stocks)

    def __len__(self):
        """
        Inherited abstract function - length

        @return - Number of stored stocks
        """
        return len(self.__stocks)

    def __getitem__(self, key):
        """
        Inherited abstract function - getter

        @return - give back the corresponding value of a key
        """
        return self.__stocks[key]

    def __setitem__(self, key, value):
        """
        Inherited abstract function - setter
        """
        if isinstance(value, Stock):
            self.__stocks[key] = value
        else:
            raise StockManagerException('Invalid Value')

    def __delitem__(self, key):
        """
        Inherited abstract function - delete
        """
        del self.__stocks[key]

    def create_stocks(self, header, stocks):
        """
        Generate stocks
        :param header: Stock Header (list)
        :param stocks: Attributes/details of stocks (list)

        """
        for stock in stocks:
            stock_details = dict(filter(lambda x: x[1] is not None, zip(header, stock)))
            stock_type = stock_details.pop('type')
            self.__stocks[stock_details['symbol']] = self.__type[stock_type](**stock_details)

