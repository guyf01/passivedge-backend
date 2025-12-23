"""Stock aggregator service for multi-month analysis."""

import logging
from collections import defaultdict
from typing import Callable

from src.models.date import MonthDate, MonthPeriod
from src.models.analysis import DayScore, StockAnalysis


logger = logging.getLogger('aggregator')


class StockAggregator:
    """
    Aggregates stock data across multiple months.
    
    Fetches data for each month in a period using a provided fetcher,
    then combines the results using DayScore.combine().
    """

    def __init__(self, fetcher: Callable[[str, MonthDate], StockAnalysis]):
        """
        Initialize aggregator with a fetcher function.
        
        :param fetcher: Function to fetch data (symbol, month) -> StockAnalysis
        """
        self._fetcher = fetcher


    def aggregate(self, symbol: str, period: MonthPeriod) -> StockAnalysis:
        """
        Aggregate stock data across a period.
        
        :param symbol: Stock ticker symbol
        :param period: The period to aggregate
        :return: StockAnalysis with averaged daily scores
        """
        # Collect all scores by day
        day_scores: dict[str, list[DayScore]] = defaultdict(list)

        for month in period.generate_months():
            analysis = self._fetcher(symbol, month)
            
            for day, score in analysis.days.items():
                day_scores[day].append(score)

        # Combine scores for each day
        combined_days = {
            day: DayScore.combine(scores)
            for day, scores in day_scores.items()
        }

        logger.info(f"Aggregated for '{symbol}' over {period}")

        return StockAnalysis(
            symbol=symbol,
            period=period,
            days=combined_days
        )
