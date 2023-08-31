class Column_Exception(Exception):
    """
    Raises an exception if the columns passed
    to bevent or bgame are not valid.
    """
    def __init__(self,message):
        super().__init__(message)

class Date_Exception(Exception):
    """
    An exception for date formatting.
    """
    def __init__(self,message):
        super().__init__(message)

class Event_File_Exception(Exception):
    """
    Raises an error if an event file does not 
    exist for a league year, or if no games exist
    for a specified time period.
    """
    def __init__(self,message):
        super().__init__(message)


class Team_Exception(Exception):
    """
    Creates the Team_Exception error.
    """
    def __init__(self,message):
        super().__init__(message)