# Module Description:  retro_object.py<br/>

## Overview<br/>

The retro_object module serves as the entry point to the project.  It<br/>
creates the Retro_Object class, which provides the bevent and bgame<br/>
methods.  bevent and bgame use python’s run function to call the<br/>
retrosheet executables of the same name.  Executable output is stored<br/>
as a string and passed to the construct_frame functions described in<br/>
the [frame_functions](/frame_functions.md) module.  A formatted DataFrame is returned to the<br/>
caller.<br/>

A third method, build_query, creates the query that is passed to the<br/>
retrosheet executable.  This query is passed to run’s args parameter.<br/>
As explained in the project summary, a retrosheet query contains the<br/>
following:  the year to be queried, optional start and end dates,<br/>
requested columns, and an event file.  build_query calls the functions<br/>
outlined in [columns.md](/columns.md) and [dates.md](/dates.md) to construct this query.<br/>

The validate_team function is called when a Retro_Object is<br/>
instantiated.  It ensures that only valid team ids are used to create a<br/>
Retro_Object instance.  Retro_Object properties include the following:<br/>
team, an upper case representation of the team id; history, a list that<br/>
outlines the years a team has played, a team’s name, and the file<br/>
extension associated with the team; and valid_years, a list of range<br/>
objects that can be called to confirm if a team played in a given time<br/>
frame.<br/>

\_\_str\_\_, an overloaded method, describes a Retro_Object instance.  When<br/>
a Retro_Object is passed to the print function, the f-string returned<br/>
by \_\_str\_\_ is printed.<br/>

## Function Signatures<br/>

```python
class Retro_Object:
    """
    Create a Retro_Object capable of calling retrosheet's bevent and
    bgame applications.
    """

    def __init__(self, team: str) -> None:
        """
        Instantiate a Retro_Object, which has the following properties:
        team, history, and valid_years.
        """

    def bevent(
            self,
            year: int,
            columns: list[int] = [idx for idx,_ in bevent_defaults],
            start: datetime = None,
            end: datetime = None
            ) -> DataFrame:
        """
        Call retrosheet's bevent.exe, returning the output in the form
        of a Pandas dataframe.
        """

    def bgame(
            self,
            year: int,
            columns: list[int] = [idx for idx,_ in bgame_all],
            start: datetime = None,
            end: datetime = None
            ) -> DataFrame:
        """
        Call retrosheet's bevent.exe, returning the output in the form
        of a Pandas dataframe.
        """

    def build_query(
            self,
            year: int,
            columns: list[int],
            app: str,
            start: datetime = None,
            end: datetime = None) -> str:
        """
        Returns an event file query that is passed to python's run
        method.
        """

    def __str__(self) -> str:
        """
        Prints a string representation of a Retro_Object.
        """
```
