# Module Description:  columns.py<br/>

## Overview<br/>

The columns.py module defines the four functions outlined in the below<br/>
code block.  The two "validate" functions parse the list of integers<br/>
passed to the bevent and bgame "columns" parameters, raising a<br/>
Column_Exception if the list is not formatted properly.  The two "get"<br/>
functions return a string that helps compose a query against the<br/>
retrosheet executables.<br/>

Two variables of note are defined in this module - bevent_dict and<br/>
bgame_dict.  They  are dictionaries that store column index and column<br/>
title information.  The retro_object class uses these dictionaries to<br/>
define default column input for bevent and bgame.<br/>

## Function Signatures<br/>

```python
 def validate_bevent(columns: list[int]):
    """
    Raises a Column_Exception error if the columns argument passed to
    bevent is out of bounds or empty.
    """

def get_bevent_cols(columns: list[int]):
    """
    Returns a string representation of columns for 
    Retrosheet's bevent application.
    """

def validate_bgame(columns: list[int]):
    """
    Raises a Column_Exception error if the columns argument passed to
    bgame is out of bounds or empty.
    """

def get_bgame_cols(columns: list[int]):
    """
    Returns a string representation of columns for Retrosheet's bgame
    application.
    """
```
