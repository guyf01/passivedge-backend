"""MonthDate dataclass for handling month/year."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MonthDate:
    """
    Represents a specific month and year.
    
    Base class without validation. Use ValidatedMonthDate for input validation.
    
    :param year: The year
    :param month: The month (1-12)
    """
    year: int
    month: int


    def __lt__(self, other: MonthDate) -> bool:
        """
        Less than comparison.
        
        :param other: Another MonthDate to compare against
        :return: True if self is before other
        """
        return (self.year, self.month) < (other.year, other.month)


    def __le__(self, other: MonthDate) -> bool:
        """
        Less than or equal comparison.
        
        :param other: Another MonthDate to compare against
        :return: True if self is before or equal to other
        """
        return (self.year, self.month) <= (other.year, other.month)


    def __gt__(self, other: MonthDate) -> bool:
        """
        Greater than comparison.
        
        :param other: Another MonthDate to compare against
        :return: True if self is after other
        """
        return (self.year, self.month) > (other.year, other.month)


    def __ge__(self, other: MonthDate) -> bool:
        """
        Greater than or equal comparison.
        
        :param other: Another MonthDate to compare against
        :return: True if self is after or equal to other
        """
        return (self.year, self.month) >= (other.year, other.month)


    def __str__(self) -> str:
        """
        Format as 'YYYY-MM'.
        
        :return: String representation in YYYY-MM format
        """
        return f"{self.year}-{self.month:02d}"
