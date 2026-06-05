"""Stock aggregator service for multi-month analysis."""

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from src.models.date import MonthPeriod
from src.models.analysis import DayScore, StockAnalysis
from src.services.stock_fetcher.base_fetcher import StockFetcher
from src import get_logger


logger = get_logger('aggregator')


class StockAggregator:
    """
    Aggregates stock data across multiple months.

    Fetches data for each month in a period using a provided fetcher,
    then combines the results using DayScore.combine().
    """

    def __init__(self, fetcher: StockFetcher, max_workers: int):
        self._fetcher = fetcher
        self._max_workers = max_workers


    def aggregate(self, symbol: str, period: MonthPeriod) -> StockAnalysis:
        """
        Aggregate stock data across all months in a period.

        Fetches each month concurrently, then merges the day scores across months
        into a single averaged result.

        :param symbol: Stock ticker symbol (e.g. AAPL)
        :param period: The period to aggregate
        :return: StockAnalysis with averaged daily scores across the period
        :raises NoDataForMonthError: If any month in the period has no data
        """
        analyses = self._fetch_all_months(symbol, period)
        days = self._merge_day_scores(analyses)
        logger.info(f"Aggregated for '{symbol}' over {period}")
        return StockAnalysis(symbol=symbol, period=period, days=days)


    def _fetch_all_months(self, symbol: str, period: MonthPeriod) -> list[StockAnalysis]:
        """Fetch all months in the period concurrently, returning results in period order."""
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            return list(executor.map(lambda month: self._fetcher.fetch(symbol, month), period.generate_months()))


    def _merge_day_scores(self, analyses: list[StockAnalysis]) -> dict[str, DayScore]:
        """Collect day scores across all analyses and combine each day into a single averaged score."""
        day_scores: dict[str, list[DayScore]] = defaultdict(list)
        for analysis in analyses:
            for day, score in analysis.days.items():
                day_scores[day].append(score)
        return {day: DayScore.combine(scores) for day, scores in day_scores.items()}
