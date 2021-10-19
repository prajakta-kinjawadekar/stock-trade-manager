from pandas import Timestamp, Timedelta, date_range
from stocks import StockManager
from trades import Trade, GlobalBeverageCorporationExchangeTradeManager

# stock's header
HEADER = ['symbol', 'type', 'last_dividend', 'fixed_dividend', 'par_value']

# stocks
STOCKS = [['TEA', 'Common', 0, None, 100], ['POP', 'Common', 8, None, 100],
          ['ALE', 'Common', 23, None, 60], ['GIN', 'Preferred', 8, 0.02, 100],
          ['JOE', 'Common', 13, None, 250]]

_stock_manager = StockManager()
_stock_manager.create_stocks(HEADER, STOCKS)

BEGINNING_OF_TRADES = Timestamp.now() - Timedelta(seconds=60)
list_of_timestamps = date_range(BEGINNING_OF_TRADES, periods=9, freq='200L')

TRADES = [['TEA', 1000, Trade.BUY, 1000],
          ['ALE', 100, Trade.SELL, 2000],
          ['GIN', 200, Trade.BUY, 900],
          ['JOE', 500, Trade.SELL, 300],
          ['ALE', 600, Trade.SELL, 200],
          ['POP', 400, Trade.BUY, 700],
          ['TEA', 100, Trade.SELL, 800],
          ['POP', 700, Trade.BUY, 900],
          ['JOE', 900, Trade.BUY, 1000]]

for i in range(9):
    TRADES[i].insert(1, list_of_timestamps[i])


def main():
    """
    It shows
     - at each trade - DIVIDEND YIELD, P/E RATIO values
     - Valume Weighted Stock Price of Trades in last 300 seconds
     - ALL Share Index
    """
    gbce = GlobalBeverageCorporationExchangeTradeManager()

    for trade in TRADES:
        print('TRADE: {0}'.format(trade))
        stock = _stock_manager[trade[0]]
        print('STOCKS -- SYMBOL: {0}, MARKET PRICE: {1}, DIVIDEND YIELD: {2}, P/E RATIO: {3}'.format(
            trade[0], trade[4], stock.dividend_yield(trade[4]), stock.pe_ratio(trade[4])))
        gbce.add(Trade(*trade))

    print('Volume Weighted Stock Price in the last 300 seconds: {0}'.format(
        gbce.volume_weighted_stock_price(300)))
    print('All Share Index: {0}'.format(gbce.all_share_index()))


if __name__ == "__main__":
    main()
