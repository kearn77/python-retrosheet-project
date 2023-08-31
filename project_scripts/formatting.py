from exceptions import Event_File_Exception

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

def do_replacements(event_output: str) -> list[str]:
    """
    Replace quotation marks and strings with the value None.
    """
    return (
            event_output
            .replace('"','')
            .replace("(None)",'')
            .split("\n")
            [:-1]
        )

def format_output(event_output: str) -> list[list]:
    """
    Return event_output as a list of lists.
    """
    
    return [row.split(",") for row in do_replacements(event_output)]