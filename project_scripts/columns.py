# Standard library imports.
from json import loads
from pathlib import Path
from sys import exit

# Local imports.
from dirs import json_dir
from exceptions import Column_Exception

# Paths to bevent and bgame column information.
# Stored as in JSON format.
bevent_fields: Path = json_dir / "bevent_fields.json"
bgame_fields: Path = json_dir / "bgame_fields.json"

# bevent and bgame fields in dictionary form.
bevent_json: dict = loads(open(str(bevent_fields),'r').read())
bevent_dict: dict[int,str] = {
    int(column_number): column_name
    for column_number, column_name in bevent_json.items()
    }

bgame_json: dict = loads(open(str(bgame_fields),'r').read())
bgame_dict: dict[int,str] = {
    int(column_number): column_name
    for column_number, column_name in bgame_json.items()
    }

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

def validate_bgame(columns: list[int]):
    """
    Raises a Column_Exception error if the columns argument passed to
    bgame is out of bounds or empty.
    """
    if not columns:
        raise Column_Exception(
            f"An empty list cannot be passed to the columns parameter."
            )
    elif max(columns) > 84 or len(columns) > 85:
        raise Column_Exception(
            f"Bgame has 85 columns, numbered 0-84."
            )
    
def get_bgame_cols(columns: list[int]):
    """
    Returns a string representation of columns for Retrosheet's bgame
    application.
    """
    try:
        validate_bgame(columns)
    except Column_Exception as err:
        print(err)
        exit(0)

    if columns == list(range(85)):
        return ' '.join(["-f","0-84"])
    else:
        return "-f " + ','.join([str(i) for i in columns])