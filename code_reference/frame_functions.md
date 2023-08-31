# Module Description:  frame_functions.py<br/>

## Overview

The frame_functions module converts the string returned by the<br/>
retrosheet executables into a formatted Pandas DataFrame.  Two<br/>
functions, construct_bevent_frame and construct_bgame_frame, create<br/>
unformatted DataFrames with a call to to_frame.  After the initial<br/>
frame is created, they call their associated formatting functions -<br/>
to_float_bevent, to_float_bgame, and to_datetime_bgame - and return a<br/>
fully formatted DataFrame.  Two lists of integers, bevent_ints and<br/>
bgame_ints,  signify the index position of numeric columns in the<br/>
bevent and bgame output.  The to_float functions use these lists in<br/>
their conversions.<br/>

In addition to DataFrame creation, this module provides functions that<br/>
further modify bevent and bgame output.  The DataFrame returned by<br/>
bevent does not contain any datetime information.  It does, however,<br/>
return an alphanumeric string from which a date can be extracted.  Two<br/>
functions, id_to_date and get_bevent_dates, work in concert to return a<br/>
Series of datetime objects.<br/>

The insert_names function converts a player’s retrosheet id - a<br/>
unique, alphanumeric string - to a first and last name.  It takes two<br/>
arguments :  a DataFrame, which the function will change in place, and<br/>
a list of column titles containing retrosheet ids.  The function<br/>
inserts Last and First name columns immediately after the retrosheet id<br/>
columns.<br/>

## Function Signatures

```python
def to_float_bevent(frame: pd.DataFrame) -> None:
    """
    Converts strings to ints, as appropriate.
    """

def to_float_bgame(frame: pd.DataFrame) -> None:
    """
    Converts strings to ints, as appropriate.
    """

def to_datetime_bgame(frame: pd.DataFrame) -> None:
    """
    Converts strings to datetimes, as appropriate.
    """

def to_frame(
        event_output: str, 
        columns: list[int]) -> pd.DataFrame:
    """
    Converts bevent and bgame string output into a pandas dataframe.
    """

def construct_bevent_frame(
        event_output: str,columns: list[int]) -> pd.DataFrame:

def construct_bgame_frame(
        event_output: str, columns: list[int],) -> pd.DataFrame:
    """
    Takes bgame output as an argument and returns
    a formatted DataFrame.
    """

def id_to_date(game_id: str) -> datetime:
    """
    Uses regular expressions to return a datetime object from a game 
    id.  Is called by get_bevent_dates.
    """

def get_bevent_dates(frame: pd.DataFrame) -> None:
    """
    Applies the id_to_date function to a bevent frame, adding a date
    series to the frame.  This change is made in-place.
    """

def get_first(retro_id: pd.Series) -> pd.Series:
    """
    Returns a Series with player first names.  Is called by get_names.
    """

def get_last(retro_id: pd.Series) -> pd.Series:
    """
    Returns a Series with player last names.  Is called by get_names.
    """

def get_names(retro_id: pd.Series) -> pd.DataFrame:
    """
    Takes a Series of retrosheet player ids and returns a DataFrame
    containing Last name and First name Series.  Is called by
    insert_names.
    """

def insert_names(frame: pd.DataFrame, columns: list[str]) -> None:
    """
    Retrieves a player's last and first names from a retrosheet player
    id.  Adds last and first columns.  Changes are made in place.
    """
```