# Standard library imports.
import os
import re 

# Local import.
from project_directories import eventsDir


# Regex pattern that matches with the year component of an event file.
findYear = re.compile(r'\d{4}')

# Walk through the event_files directory.  Append all event_file years to fileYears.
directory = os.fsencode(str(eventsDir))
fileYears = []
for file in os.listdir(directory):
    fileName = os.fsdecode(file)
    if fileName.endswith('.EVA') or fileName.endswith('.EVN'):
        currentYear = [int(i) for i in re.findall(pattern=findYear, string=fileName)][0]
        fileYears.append(currentYear)
    else:
        continue

# Create default year start and year end variables based on the max and 
# min years found within the event_files directory.
defaultYearStart = min(fileYears)
defaultYearEnd = max(fileYears)






