class TradeManagerException(Exception):
    """
    TradeManager Exception class
    """
    def __init__(self, message_):
        super(TradeManagerException, self).__init__(message_)


class TradeException(Exception):
    """
    Trade Exception Class
    """
    def __init__(self, message_):
        super(TradeException, self).__init__(message_)


class StockException(Exception):
    """
    Stock Exception Class
    """
    def __init__(self, message_):
        super(StockException, self).__init__(message_)


class StockManagerException(Exception):
    """
    StockManager Exception Class
    """
    def __init__(self, message_):
        super(StockManagerException, self).__init__(message_)
