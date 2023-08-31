# Module Description:  exceptions.py<br/>

## Overview
The exceptions module creates four exceptions, which all inherit from<br/>
python’s base Exception class.<br/>

## Column_Exception
Column_Exception signifies a formatting error with the list of integers<br/>
passed to the bevent and bgame columns parameter.  It is raised by the<br/>
"validate" functions found within the columns module - validate_bevent<br/>
and validate_bgame.  The module’s "get" functions - get_bevent and<br/>
get_bgame - call the validate functions and print the associated error<br/>
message if the raise condition is triggered.<br/>

### Associated Functions

```python
def validate_bevent(columns: list[int]):
    """
    Raises a Column_Exception error if the columns argument passed to
    bevent is out of bounds or empty.
    """
    if not columns:
        raise Column_Exception(
            f"An empty list cannot be passed to the columns parameter."
        )
    if max(columns) > 96 or len(columns) > 97:
        raise Column_Exception(
            f"Bevent has 97 columns, numbered 0 - 96."
        )

def get_bevent_cols(columns: list[int]):
    """
    Returns a string representation of columns for 
    Retrosheet's bevent application.
    """
    try:
        validate_bevent(columns)
    except Column_Exception as err:
        print(err)
        exit(0)
        
    if columns == list(range(97)):
        return ' '.join(["-f","0-96"])
    else:
        return "-f " + ','.join([str(i) for i in columns])
```

## Date_Exception
Date_Exception signifies a problem with the arguments passed to the<br/>
start and end parameters in a call to bevent or bgame.  The exception<br/>
is raised by the function validate_dates, which is located in the dates<br/>
module.  The get_date_str function calls validate_dates and prints an<br/>
error message if a raise condition is triggered.<br/>

### Associated Functions

```python
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
```

## Event_File_Exception
Event_File_Exception signifies a problem with the event file passed to<br/>
a retrosheet query.  Typically, this encompasses two scenarios.  Either<br/>
there is no output associated with the query’s dates, or the event<br/>
file itself is not present in the event_files directory.  This<br/>
exception is raised in the validate_output function, which is located<br/>
in the formatting module.  The to_frame function, which is located in<br/>
the frame_functions module, calls validate_output, printing an error<br/>
message if the raise condition is triggered.<br/>

### Associated Functions

```python
def validate_output(event_output: str) -> None:
    """
    Raises an Event_File_Exception if output is equal to the empty string.
    Signifies a proper query with no associated dates.
    """
    try:
        if not event_output:
            raise Event_File_Exception(
                f"No games associated with date_str argument."
            )
    except Event_File_Exception as err:
        print(err)
        exit(0)

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
```

## Team_Exception
Team_Exception indicates that the string passed to retro_object is not<br/>
a valid team abbreviation.  It is raised by the team module’s<br/>
validate_team function.  validate_team is called when a retro_object is<br/>
instantiated.<br/>

### Associated Functions

```python
def validate_team(team: str) -> None:
    """
    Raises a Team_Exception error.
    """
    try:
        if team not in valid_teams:
            raise Team_Exception(
                f"{team} is not a valid team abbreviation."
            )
    except Team_Exception as err:
        print(err)
        exit(0)

def __init__(self, team: str) -> None:
        """
        Instantiate a Retro_Object, which has the following properties:
        team, history, and valid_years.
        """
        is_valid(team.upper())
        self.team = team.upper()
        self.history: list[list] = teams_dict[self.team]
        self.valid_years: list[range] = (
            [range(i[0],i[1]) for i in self.history]
            )
```