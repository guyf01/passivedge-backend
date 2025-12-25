"""Stock data fetcher service using Yahoo Finance."""

import yfinance as yf

from src.models.date import MonthDate, MonthPeriod
from src.models.analysis import DayScore, StockAnalysis
from src.services.stock_fetcher.exceptions import NoDataForMonthError
from src import get_logger


logger = get_logger('fetcher')


class MonthStockFetcher:
    """
    Fetches stock data from Yahoo Finance for a single month.
    
    Calculates avg_price_diff = ((day_close - month_avg) / month_avg) * 100
    """
    @staticmethod
    def exists(symbol: str) -> bool:
        """
        Check if a stock symbol exists.
        
        :param symbol: Stock ticker symbol (e.g., 'AAPL')
        :return: True if stock exists, False otherwise
        """
        ticker = yf.Ticker(symbol)
        # Check if ticker has valid info (fast check)
        return ticker.info.get('regularMarketPrice') is not None


    def fetch(self, symbol: str, month: MonthDate) -> StockAnalysis:
        """
        Fetch data for a single month and calculate avg_price_diff.
        
        :param symbol: Stock ticker symbol (e.g., 'AAPL')
        :param month: The month to fetch
        :return: StockAnalysis with daily scores
        :raises NoDataForMonthError: If no data available for the month
        """
        logger.info(f"Fetching data for '{symbol}' '{month}'")
        
        df = yf.Ticker(symbol).history(
            start=month.to_datetime(),
            end=month.next_month().to_datetime()
        )

        if df.empty:
            logger.warning(f"No data found for '{symbol}' '{month}'")
            raise NoDataForMonthError(f"No data found for {symbol} in {month}")
        
        month_avg = df['Close'].mean()
        df['avg_price_diff'] = (df['Close'] / month_avg - 1) * 100
        
        logger.info(f"Fetched {len(df)} trading days for '{symbol}' '{month}'")
        
        return StockAnalysis(
            symbol=symbol,
            period=MonthPeriod.single(month),
            days={
                str(date.day): DayScore(avg_price_diff=round(apd, 2)) 
                for date, apd in df['avg_price_diff'].items()
            }
        )
