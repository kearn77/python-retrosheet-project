# Module Description: dates.py<br/>

## Overview<br/>

The dates.py module provides four functions that help compose the date<br/>
component of a bgame or bevent query.  The get_start and get_end<br/>
functions take datetime objects as input and return a string<br/>
representation of the date.  Python’s format method is used to<br/>
generate padded zeros where appropriate.<br/>

The validate_dates function takes two datetime objects as input and<br/>
raises a Date_Exception if the first date is greater than the second<br/>
date.<br/>

All three functions are called within get_date_str, which takes an int<br/>
and two datetime objects as arguments and returns the date component of<br/>
a bgame or bevent query.  Moreover, it prints a Date_Exception to<br/>
standard output if the raise condition in validate_dates is triggered.<br/>
It uses python’s join method to compose the date string.<br/>

## Function Signatures

```python
def get_start(date_obj: datetime) -> str:
    """
    Returns a string representation of a datetime day and month.
    """

def get_end(date_obj: datetime) -> str:
    """
    Returns a string representation of a datetime day and month.
    """

def validate_dates(
        date_1: datetime = None, 
        date_2: datetime = None
        ) -> None:
    """
    Raise a value error if an end date precedes a start date.
    """

def get_date_str(
        year: int,
        start:datetime=None, 
        end:datetime=None,
        ) -> str:
    """
    Returns a string representation of a date query.
    """
```