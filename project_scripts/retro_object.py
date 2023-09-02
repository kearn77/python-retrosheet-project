# Standard library imports.
from datetime import datetime
from os import chdir
from subprocess import run

# Third party imports.
from pandas import DataFrame

# Local imports.
from columns import (
    bevent_dict,
    bgame_dict,
    get_bevent_cols,
    get_bgame_cols
)
from dates import get_date_str
from dirs import (
    local_dir, 
    events_dir
)
from frame_functions import (
    construct_bevent_frame,
    construct_bgame_frame,
)
from teams import (
    get_ext, 
    teams_dict, 
    validate_team
)


class Retro_Object:
    """
    Create a Retro_Object capable of calling retrosheet's bevent and
    bgame applications.
    """

    # Default bevent and bgame column information.
    bevent_defaults = [(idx,col) for idx, col in bevent_dict.items()
                        if col.endswith("*")]
    bevent_all = [(idx,col) for idx, col in bevent_dict.items()]
    bgame_all = [(idx,col) for idx, col in bgame_dict.items()]

    def __init__(self, team: str) -> None:
        """
        Instantiate a Retro_Object, which has the following properties:
        team, history, and valid_years.
        """
        validate_team(team.upper())
        self.team = team.upper()
        self.history: list[list] = teams_dict[self.team]
        self.valid_years: list[range] = (
            [range(i[0],i[1]) for i in self.history]
            )

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
    
        query = self.build_query(year,columns,"bevent",start,end)
        chdir(events_dir)
        
        # String output from bevent.exe.
        bevent_str = run(
            args = query,
            shell = False,
            capture_output = True,
            encoding = "UTF-8"
            ).stdout
        
        chdir(local_dir)
        return construct_bevent_frame(bevent_str,columns)

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
        query = self.build_query(year,columns,"bgame",start,end)
        chdir(events_dir) 

        # String output from bgame.exe.
        bgame_str = run(
            args = query,
            shell = False,
            capture_output = True,
            encoding = "UTF-8"
            ).stdout
        
        chdir(local_dir)
        return construct_bgame_frame(bgame_str,columns)
    
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
        if app == "bevent":
            column_string = get_bevent_cols(columns)
            date_string = get_date_str(year,start,end)
        else:
            column_string = get_bgame_cols(columns)
            date_string = f"{get_date_str(year,start,end)} -dsf"

        team_extension = get_ext(year,self.team)

        return " ".join([
                    app,
                    date_string,
                    column_string,
                    team_extension
                    ]
                )

    def __str__(self) -> str:
        """
        Prints a string representation of a Retro_Object.
        """
        if len(self.history) < 2:
            return (
                f"{self.history[0][3]} Retro_Object."
                f"  Valid years are: {self.valid_years}"
                )
        else:
            return (
                f"{self.history[1][3]} Retro_Object."
                f"  Valid years are: {self.valid_years}"
                )