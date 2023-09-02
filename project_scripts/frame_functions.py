# Standard library imports.
from datetime import datetime
from json import loads
from re import compile, sub

# Third party imports.
import pandas as pd

# Local imports.
from columns import bevent_dict, bgame_dict
from dirs import json_dir
from formatting import format_output, validate_output

bevent_ints = [
    2,3,4,5,6,8,9,32,33,34,37,40,43,46,51,52,54,56,58,59,60,61,87,88,
    89,90,91,92,93,94,95,96
    ]

bgame_ints = [
    2,18,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,47,49,
    51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81
    ]

bio_json = json_dir / "bio_information.json"
bio_dict: dict[str,dict[str,str]] = loads(open(str(bio_json),'r').read())

def to_float_bevent(frame: pd.DataFrame) -> None:
    """
    Converts strings to ints, as appropriate.
    """
    for column in frame.columns:
        if column in bevent_ints:
            frame[column] = pd.to_numeric(arg=frame[column])
        else:
            continue

def to_float_bgame(frame: pd.DataFrame) -> None:
    """
    Converts strings to ints, as appropriate.
    """
    for column in frame.columns:
        if column in bgame_ints:
            frame[column] = pd.to_numeric(arg=frame[column])
        else:
            continue

def to_datetime_bgame(frame: pd.DataFrame) -> None:
    """
    Converts strings to datetimes, as appropriate.
    """
    for column in frame.columns:
        if column == 1:
            frame[column] = pd.to_datetime(frame[column],format="%m/%d/%Y")
            frame[column] = frame[column].dt.date
        else:
            continue

def to_frame(
        event_output: str, 
        columns: list[int]) -> pd.DataFrame:
    """
    Converts bevent and bgame string output into a pandas dataframe.
    """
    validate_output(event_output)
    frame = pd.DataFrame(
        data = format_output(event_output),
        columns = columns
        )
    return frame

def construct_bevent_frame(
        event_output: str,columns: list[int]) -> pd.DataFrame:
    """
    Takes bevent output as an argument and returns
    a formatted DataFrame.
    """
    frame = to_frame(event_output,columns)
    to_float_bevent(frame)
    frame = frame.rename(columns=bevent_dict)
    return frame

def construct_bgame_frame(
        event_output: str, columns: list[int],) -> pd.DataFrame:
    """
    Takes bgame output as an argument and returns
    a formatted DataFrame.
    """
    frame = to_frame(event_output,columns)
    to_datetime_bgame(frame)
    to_float_bgame(frame)
    frame = frame.rename(columns=bgame_dict)
    return frame

def id_to_date(game_id: str) -> datetime:
    """
    Uses regular expressions to return a datetime object from a game 
    id.  Is called by get_bevent_dates.
    """
    pattern = compile("[A-Z]{3}(\d{4})(\d{2})(\d{2})\d")
    nums = sub(pattern, r"\1,\2,\3", game_id)
    nums = [int(val) for val in nums.split(sep = ",")]
    return datetime(
        year = nums[0], 
        month = nums[1], 
        day = nums[2]
        ).date()

def get_bevent_dates(frame: pd.DataFrame) -> None:
    """
    Applies the id_to_date function to a bevent frame, adding a date
    series to the frame.  This change is made in-place.
    """
    if "game id*" in frame.columns:
        idx = frame.columns.get_loc("game id*")
        date = pd.Series(frame["game id*"]).apply(id_to_date)
        frame.insert(idx+1,"date",date)

def get_first(retro_id: pd.Series) -> pd.Series:
    """
    Returns a Series with player first names.  Is called by get_names.
    """
    first = retro_id.apply(lambda first: bio_dict[first]["FIRST"])
    return first

def get_last(retro_id: pd.Series) -> pd.Series:
    """
    Returns a Series with player last names.  Is called by get_names.
    """
    last = retro_id.apply(lambda last: bio_dict[last]["LAST"])
    return last

def get_names(retro_id: pd.Series) -> pd.DataFrame:
    """
    Takes a Series of retrosheet player ids and returns a DataFrame
    containing Last name and First name Series.  Is called by
    insert_names.
    """
    names = pd.concat(
        objs = [get_last(retro_id),get_first(retro_id)],
        axis = 1
        )
    names.columns = ["Last", "First"]
    return names

def insert_names(frame: pd.DataFrame, columns: list[str]) -> None:
    """
    Retrieves a player's last and first names from a retrosheet player
    id.  Adds last and first columns.  Changes are made in place.
    """
    for title in columns:
        idx = frame.columns.get_loc(title)
        names = get_names(frame[title])
        frame.insert(idx+1,f"{title} Last",names["Last"])
        frame.insert(idx+2,f"{title} First",names["First"])