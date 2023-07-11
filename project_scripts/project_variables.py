# Standard library imports.
from json import loads

# local imports.
from project_directories import jsonDir


# Project level dictionaries imported by the retro_object module, 
# mainly for object instantiation.
beventFieldsDict = loads(open(jsonDir / "bevent_fields.json", "r").read())
beventFieldsDict = {
    int(columnNumber): columnName 
    for columnNumber, columnName in beventFieldsDict.items()
    }

bgameFieldsDict = loads(open(jsonDir / "bgame_fields.json", "r").read())
bgameFieldsDict = {
    int(columnNumber): columnName 
    for columnNumber, columnName in bgameFieldsDict.items()
    }

teamDict = loads(open(jsonDir / "team_extensions.json", "r").read())

# Project level dictionaries that contain retrosheet's key-value pairs.
# These are not necessary for object instantiation, but will aid in 
# understanding a retro_object's underlying data.
bioDict = loads(open(jsonDir / "bio_information.json", "r").read())

precipDict = loads(open(jsonDir / "precipitation.json", "r").read())
precipDict = {
    int(columnNumber): columnName
    for columnNumber, columnName in precipDict.items()
    }

skyDict = loads(open(jsonDir / "sky.json", "r").read())
skyDict = {
    int(columnNumber): columnName
    for columnNumber, columnName in skyDict.items()
    }

windDir = loads(open(jsonDir / "wind_direction.json", "r").read())
windDir = {
    int(columnNumber): columnName
    for columnNumber, columnName in windDir.items()
    }
