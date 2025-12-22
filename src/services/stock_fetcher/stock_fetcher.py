"""Stock data fetcher service using Yahoo Finance."""

import logging

import yfinance as yf

from src.models.date import MonthDate, MonthPeriod
from src.models.analysis import DayScore, StockAnalysis
from src.services.stock_fetcher.exceptions import NoDataForMonthError


logger = logging.getLogger('fetcher')


class MonthStockFetcher:
    """
    Fetches stock data from Yahoo Finance for a single month.
    
    Calculates avg_price_diff = ((day_close - month_avg) / month_avg) * 100
    """

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
            start=month.as_date(),
            end=month.next_month().as_date()
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
