# Module Description:  formatting.py<br/>

## Overview
The formatting module defines three functions – do_replacements,<br/>
format_output, and validate_output.  do_replacements edits the string<br/>
returned by a retrosheet executable, while format_output splits the<br/>
edited string to create a list.  Ultimately, the to_frame function,<br/>
which is located in the frame_functions module, passes this list to the<br/>
Pandas DataFrame method, returning the result to the caller.  The<br/>
validate_output function raises an Event_File_Exception, which is<br/>
elucidated [here](/exceptions.md).<br/>

## Function Signatures

```python
def do_replacements(event_output: str) -> list[str]:
    """
    Replace quotation marks and strings with the value None.
    """

def format_output(event_output: str) -> list[list]:
    """
    Return event_output as a list of lists.
    """

def validate_output(event_output: str) -> None:
    """
    Raises an Event_File_Exception if output is equal to the empty string.
    Signifies a proper query with no associated dates.
    """
```