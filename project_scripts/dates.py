# Standard library imports.
from datetime import datetime
from sys import exit

# Local imports.
from exceptions import Date_Exception

def get_start(date_obj: datetime) -> str:
    """
    Returns a string representation of a datetime day and month.
    """
    if date_obj is None:
        return ""
    else:
        return " -s {:02d}{:02d}".format(
            date_obj.month,
            date_obj.day,
            )

def get_end(date_obj: datetime) -> str:
    """
    Returns a string representation of a datetime day and month.
    """
    if date_obj is None:
        return ""
    else:
        return " -e {:02d}{:02d}".format(
            date_obj.month,
            date_obj.day
            )
    
def validate_dates(
        date_1: datetime = None, 
        date_2: datetime = None
        ) -> None:
    """
    Raise a value error if an end date precedes a start date.
    """
    
    if (date_1 and date_2) and date_1 > date_2:
        raise Date_Exception(
            f"Start must be less than end."
            )

def get_date_str(
        year: int,
        start:datetime=None, 
        end:datetime=None,
        ) -> str:
    """
    Returns a string representation of a date query.
    """
    try:
        validate_dates(start,end)
        year_str = f"-y {year}"
        return "".join([year_str,get_start(start),get_end(end)])
    except Date_Exception as err:
        print(err)
        exit(0)