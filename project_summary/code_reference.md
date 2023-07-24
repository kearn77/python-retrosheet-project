## Naming Conventions

In keeping with python convention, I have written project level file names in<br/>
snake-case, with a single underscore separating distinct, lower-case words.<br/>
Module level variable names are written in camel-case style: lowercase letters<br/>
compose the first word in a variable, and the first letter of any subsequent<br/>
word is capitalized.  In accordance with the PEP8 style guide, classes are an<br/>
exception to this rule, beginning with a capital rather than lowercase letter.   
	
As highlighted in the project synopsis, the majority of RetroObject's methods<br/>
format user input into a valid query string.  These strings are then passed to<br/>
“bevent,” “bgame,” and “box.”  Since users are not meant to call formatting<br/>
methods directly, they begin with double underscores, e.g.,<br/>
__createColumnString.  Note that the first method in the RetroObject class,<br/>
the double underscore enclosed __init__, is a common method shared by all<br/>
python classes.  Roughly equivalent to a constructor, __init__ is responsible<br/>
for creating instances of a class.

## Line Length, Indentation, and Blank Spaces

PEP8 recommends limiting most lines to a maximum of seventy-nine characters,<br/>
with docstrings and long blocks of text limited to seventy-two characters.<br/>
These restrictions allow readers to split their screens while maintaining code<br/>
readability, enabling the cross referencing of source code and library<br/>
documentation.  With this goal in mind, continuation lines have been written<br/>
in accordance with PEP8's indenting recommendations, though there are several<br/>
recurring patterns that may seem awkward to programmers.  For example, longer<br/>
list comprehensions have been split across multiple lines, resulting<br/>
in the following pattern:

```python
self.dateRange = [
            year for year in 
            range(int(yearStart), int(yearEnd) + 1, 1)
            ]
```
Figure 1 - PEP8 formatted list comprehension.

While my natural inclination is to write the above comprehension on a single<br/>
line, I have opted for the current form as a matter of consistency with PEP8.<br/>
My apologies for any vertigo that may ensue.
	
With the exception of multi-line expressions, whitespace has been omitted<br/>
immediately insides parentheses and before commas.  However, a single space<br/>
has been inserted after a comma that separates one value from another.  For<br/>
example, when unpacking a tuple, the code favors the following convention: <br/>
x,y = 5, 10.  Similarly, values passed into method parameters are separated by<br/>
a single space.

## Code Notes

The program begins by importing a number of standard library modules, third<br/>
party modules, and local modules.  Standard library modules are imported<br/>
first, third party modules second, local modules third.  As a secondary<br/>
sorting convention, modules are ordered alphabetically ascending.

retro_object imports  event_parser, project_directories, and<br/>
project_variables.  event_parser uses regular expressions to determine the<br/>
bounds of the event files on record.  This will determine default year start<br/>
and year end arguments for bevent, bgame, and box.  project_directories<br/>
provides file paths called throughout retro_object, while project_variables<br/>
contains a number of dictionaries that are used throughout retro_object to<br/>
determine relevant team information and default column input.
	
There are several dictionaries located within project_variables that are not<br/>
imported by retro_object.  The dictionary of player, manager, and umpire<br/>
biographical information - titled bioDict - is especially useful to end users.<br/>
Figure 2 demonstrates how these local modules can be imported by a scripts<br/>
running in a different directory.

```python
# Standard library imports.
from datetime import datetime
from pathlib import Path
from re import compile, findall, sub
import sys

# Third party library imports.
import pandas as pd

# Local imports.
sys.path.insert(0,str(Path.cwd().parent/"project_scripts"))
from project_variables import bioDict
import retro_object as ro
```
Figure 2 - Import statements.

Next, the module defines the RetroObject class, which contains our program's<br/>
core logic.  Class level attributes are defined before methods, and they may<br/>
be called by any instance of the class through dot notation.  A class object<br/>
is created by passing a valid "retroString" to a RetroObject call, e.g.,<br/>
RetroObject('WAS').  Please note that ro.validTeams will return a list of<br/>
acceptable retroStrings.  Moreover, capitalization does not matter; the<br/>
constructor automatically converts user input to upper case.

Like all python classes, the first defined method is __init__, which creates<br/>
class instances and assigns them the following attributes: "lowerBound,"<br/>
"upperBound," "league," "fullName," and "fileExtension."  Generally speaking,<br/>
the bounds are used to determine if a user requested season is valid, while<br/>
fileExtension ensures that the proper file is queried - i.e., a query about an<br/>
American League team is made against a .EVA file, a National League team a<br/>
.EVN file.  fullName and league exist for informational purposes, since team<br/>
abbreviations are not necessarily intuitive.  These attributes are sourced<br/>
from the json file "team_extensions.json," which is loaded into the program<br/>
and stored as the dictionary "teamDict."   A sixth attribute, titled "entry,"<br/>
will return the dictionary value associated with a retroString, which serves<br/>
as a dictionary key.

Please note that two teams - the Houston Astros and Milwaukee Brewers - have<br/>
played in both the American League and the National League.  Consequently,<br/>
they have two entries for every attribute, each ending in a one or two, e.g.,<br/>
lowerBoundOne versus lowerBoundTwo.

```python
import retro_object as ro

boston = ro.RetroObject('BOS')
```
Figure 3 - RetroObject instantiation.

The first method encountered after __init__ is bevent, which returns<br/>
play-by-play records as a list of lists.  Bevent begins by changing the<br/>
current working directory to the application directory, and it concludes by<br/>
returning to the module level directory.  This pattern is repeated for bgame<br/>
and box.

Six arguments may be passed to bevent, dictating the column numbers to be<br/>
queried, the desired date range from which to pull information, and the<br/>
seasons requested by the caller.  After assigning these variables to self, the<br/>
method runs a conditional statement to determine whether the caller passed<br/>
both a game id and start/end parameters to the method.  If the caller passed<br/>
both types of arguments, then the program warns that game id takes precedence<br/>
over start and end, and only one record - that associated with the game id -<br/>
will be returned.

Subsequently, three variables are created - dateRange, output, and<br/>
columnValidation.  Bevent iterates over the years in dateRange with a for<br/>
loop, running its executable for every year in the range and concatenating the<br/>
results to output.  __columnValidation, assigned to __columnPipe's output,<br/>
helps construct the query string passed into the run method.

Once the loop has concluded, bevent uses the string method, "split," to<br/>
convert rawOutput into a list, with newline characters serving as the<br/>
demarcation separating entries.  Formatting changes are made to entries within<br/>
output using a list comprehension and the string method "replace," and the<br/>
program splits the list by comma, creating a list of lists.  Finally, bevent<br/>
loops over every list in output, calling the __convertToInt method to change<br/>
strings to integers, where appropriate.  Output is returned to the caller.

```python
def bevent(
        self, columns = defaultColsBevent, 
        yearStart = defaultYearStart, yearEnd = defaultYearEnd,
        start = None, end = None, id = None) -> list[list]:
    """
    Bevent uses the run method from python's subprocess module to 
    call Retrosheet's bevent application as a child process of the 
    program.  The functions __createDateString, __columnPipe, and 
    __produceFileExtension are called to properly format the query 
    that is passed into the run method. Generally, bevent returns 
    more granular information about a game, e.g. number/type of 
    pitches during an at bat.  Output is passed through the 
    __typeConversions function and returned as a list of lists.
    """
```
Figure 4 - bevent call signature and docstring.

The two methods after bevent - bgame and box - mirror bevent's structure.<br/>
There is only one meaningful difference between the type of data returned by<br/>
bevent and bgame - the latter contains three columns that return date<br/>
information.  To accommodate these columns, bgame calls __typeConversions<br/>
rather than __convertToInt, changing string values to datetime objects where<br/>
appropriate.  Note that __typeConversions calls __mergeDateTime to properly<br/>
format the time component in any datetime object.

```python
def bgame(
        self, columns = defaultColsBgame, 
        yearStart = defaultYearStart, yearEnd = defaultYearEnd,
        start = None, end = None, id = None) -> list[list]:
    """
    Bgame uses the run method from python's subprocess module to 
    call Retrosheet's bgame application as a child process of the 
    program.  The functions __createDateString, __columnPipe, and 
    __produceFileExtension are called to properly format the query 
    that is passed into the run method.  Output is passed through 
    __typeConversions and __converToInt and returned as a list of 
    lists.  Bgame returns general information about a game, e.g. 
    start time, temperature, starting lineups, etc.  
    """
```
Figure 5 - bgame call signature and docstring.

Box is simply a truncated version of bevent and bgame.  The method returns<br/>
output once it has exited the for loop, with no additional formatting.  Box's<br/>
functionality is largely identical to its concomitant command line<br/>
application, allowing the user to return box scores from multiple seasons with<br/>
a single call.

```python
def box(
        self, yearStart = defaultYearStart, 
        yearEnd = defaultYearEnd, start = None, 
        end = None, id = None) -> str:
    """
    Box uses the run method from python's subprocess module 
    to call Retrosheet's box application as a child process 
    of the program.  The functions __createDateString and 
    __produceFileExtension are called to properly format the 
    query that is passed into the run method.  Box returns 
    a boxscore string suitable for import into a text file 
    or printing on the command line.
    """
```
Figure 6 - box call signature and docstring.

The remaining methods in RetroObject serve a singular purpose - format the<br/>
input passed into, and the output returned by, the emulation methods bevent,<br/>
bgame, and box.  They accomplish this in a nested manner.  Relatively simple<br/>
formatting methods are passed into more complex ones, which are in turn called<br/>
by the emulation methods.
	
__columnPipe, called by bevent and bgame prior to executing their for loops,<br/>
converts the user's requested columns into a valid string.  While this may<br/>
seem like a simple task, quirks in the command line applications complicate<br/>
its execution. 

Internally, bevent and bgame columns begin with zero and run through<br/>
eighty-four and ninety-six, respectively.  However, if a user were to pass<br/>
every column number to an executable, then an error message is returned,<br/>
indicating that the requested columns exceed the number of columns.  This is a<br/>
semantic error, with the retrosheet application conflating column maximums<br/>
with the length of the column array requested.  To prevent this error,<br/>
__columnPipe returns a column string in the following form: 0-84.  This<br/>
convention is applied to all consecutive column numbers, such that a request<br/>
for columns "1, 2, 3, 4, 5, 20, 21, 22" would return "1-5, 20-22."  Although<br/>
__columnPipe returns a column string, it cedes the logic to another method,<br/>
titled "__createColumnString."  __columnPipe also returns a sorted array of<br/>
the columns selected, and in the case of bgame, the difference between the<br/>
index positions of columns one and four in the sorted column array.

```python
def __columnPipe(
        self, 
        columns = defaultColsBgame, 
        desiredFunction = 'bgame') -> tuple:
    """
    __columnPipe returns the column information bevent and bgame 
    require to execute successfully.  If the desired function is 
    set to bgame, then three objects are returned - a column 
    string, a sorted column list, and the difference between 
    the indexes for columns four and one, if applicable.  If 
    the desired function is set to bevent, then only the column 
    string and column list are returned.
    """
```
Figure 7 - __columnPipe call signature and docstring.

```python
return (
    self.columnString,
    self.columns,
    )
```
Figure 8 - __columnPipe return value.

__createColumnString is straightforward in its approach.  An array of column<br/>
numbers is passed to the method.  A for loop iterates over the array,<br/>
attempting to assign the next element to the variable nextValue.  If this<br/>
assignment does not succeed, then iteration has concluded, and columnString is<br/>
returned.  Otherwise, the method determines whether the next value is one<br/>
greater than the current value.  If it is, then the loop continues to the next<br/>
value.  If it is not, then a string of the following form, minValue-value, is<br/>
concatenated to columnString, and minValue is assigned to nextValue.

```python
def __createColumnString(self, columns) -> list:
    """
    __createColumnString creates a valid column string that bevent
    and bgame can use to query event files.  It is called 
    by  "__columnPipe,' which provides the column information 
    bevent and bgame need to query event files.
    """
```
Figure 9 - __createColumnString call signature and docstring.

When bgame calls __columnPipe, __columnPipe calls the method<br/>
__linkDateColumns.  If a user requests bgame's fourth column without its first<br/>
column, then __linkDateColumns appends the first column to the list of<br/>
requested columns.  Because bgame's fourth column is a time string, it is<br/>
devoid of meaning without an associated date.  In recognition of this<br/>
deficiency, __linkDateColumns prevents the fourth column from being returned<br/>
without a date component.

```python
def __linkDateColumns(self, columns) -> tuple:
    """
    This function, which is called by __columnPipe if the 
    parameter 'desiredFunction' is set to 'bgame,' ensures 
    that column one is present in the column list when four 
    is selected without it.  It returns the new sorted column 
    list, in addition to the difference between the indexes 
    for columns four and one.
    """
```
Figure 10 - __linkDateColumns call signature and docstring.

The other formatting method directly called by bevent, bgame, and box is<br/>
__createDateString.  It returns the date components used in a valid query<br/>
string, accomplishing this feat by incorporating two additional methods:<br/>
__convertToDatetime and __evalGameId.

```python
def __createDateString(
        self, year = 2021, 
        start = None, end = None, 
        id = None) -> list:
    """
    __createDateString returns the proper date 
    formatting for bevent, bgame, and box queries.  
    The start and end parameters, which take both integer
    and string input, denote the start and end dates a 
    user is querying.  If either start or end is selected 
    with the other parameter set to None, then results 
    will start from or terminate with the selected date, 
    respectively.  Id queries a specific game using a 
    concatenated string format - teamid | four-digit year 
    | zero-padded month | zero-padded day | an integer 0-3.  
    Please note that id and start/end are mutually 
    exclusive; id has precendence over start and end.
    """
```
Figure 11 - __createDateString call signature and docstring.

__createDateString begins via tuple assignment, with year, start, and end<br/>
referencing __convertToDatetime's output.  __convertToDatetime uses another<br/>
method, __convertDatetimeComponents, to ensure that year, start, and end are<br/>
either datetime or NoneType objects.

Once year, start, and end have been properly assigned, __createDateString runs<br/>
a gauntlet of conditional tests and returns the properly formatted date<br/>
string.  If a game id is passed to the method, then the id is passed to<br/>
__evalGameId, which determines whether the id is properly constructed.  If the<br/>
formatting is correct, then the game id is returned.

```python
def __convertToDatetime(
        self, yearComponent = 2021, 
        startComponent = None, endComponent = None) -> tuple:
    """
    __convertToDatetime is called by __createDateString
    to compose proper date queries. It takes three arguments - 
    yearComponent, startComponent, and endComponent -and returns 
    objects suitable for __createDateString.  Returned values are 
    either datetime or NoneType objects.
    """

```
Figure 12 - __convertToDatetime call signature and docstring.

```python
def __convertDatetimeComponents(self, component):
    """
    __convertDatetimeComponents is called by the 
    __convertToDatetime function to ensure that 
    self.year,self.start, and self.end are one of 
    the following object types: datetime, integer, 
    or NoneType.  Ultimately, arguments passed into 
    this function are returned to convert_ to_datetime, 
    which are then passed to create_date_string.
    """
```
Figure 13 - __convertDatetimeComponents call signature and docstring.

```python
def __evalGameId(self, id):
    """
    This function uses the compile and match methods 
    from the regular expressions library to raise 
    value errors for any game id that is not properly 
    formatted.  It is called by __createDateString 
    when an argument is passed to the id parameter.
    """
```
Figure 14 - __evalGameId call signature and docstring.

As described, the program's control flow is fairly basic.  Emulation functions<br/>
call __columnPipe and __createDateString to form valid queries.  In turn,<br/>
__columnPipe and __createDateString call methods to accomplish this task.  The<br/>
output returned by python's run method is passed through __convertToInt and<br/>
__typeConversions and returned to the caller.  For more information regarding<br/>
a method, please reference that method's docstring.

```python
def __convertToInt(self, target):
    """
    This function attempts to convert a target object to an int.  
    If this is successful, then the new int object is returned.  
    If the target object is None, then the nan type from python's 
    math module is returned.  Finally, if the target object cannot 
    be converted to an integer and is not None, then the unaltered 
    target object is returned.
    """
```
Figure 15 - __convertToInt call signature and docstring.

```python
def __typeConversions(self, retro_output, columns) -> list:
    """
    __typeConversions converts string objects to integers, nan,
    or datetime objects, where appropriate.  It accomplishes 
    this by looping over the entries in bgame and bevent output 
    and calling the function __convertToInt.  
    
    If retro_application is set to bgame and the index linked 
    to column four is reached, then a proper datetime object is 
    created by calling __mergeDateTime.  If the index linked to 
    column one or twenty-two is reached, then a proper datetime 
    is created with datetime's strptime method.
    """
```
Figure 16 - __typeConversions call signature and docstring.