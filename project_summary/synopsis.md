## Project Inception

Some time ago, as a first attempt at a programming project, I cobbled<br/>
together a database file containing MLB results and statistics over the last<br/>
twenty seasons.  I accomplished this by scraping sportsreference.com, which<br/>
has a generous web-scraping policy that accommodates most get requests.  Given<br/>
the massive amount of information I needed to scrape, however, even<br/>
sportsreference’s web-scraping policy presented difficulties I struggled to<br/>
overcome.  Trust me, it is difficult to capture data in a timely manner capped<br/>
at a request per second!   Fortunately, I found a more complete, open-source<br/>
set of resources - [retrosheet.org.](https://www.retrosheet.org/).

Founded in 1989, retrosheet is a record keeping project that computerizes<br/>
play-by-play accounts of Major League baseball games.  Information on the site<br/>
is free to use, under the condition that any project developed with the site's<br/>
information [properly cites the site](/IMPORTANT_RETROSHEET_NOTICE.md).

Although retrosheet makes staggering amounts of information available free of<br/>
charge, I quickly encountered a problem - the information largely exists in<br/>
specialty files that can only be queried by the site's software applications.<br/>
Further complicating matters, the applications are meant to run on a windows<br/>
command line, with output redirected to text files that can be imported into<br/>
database and spreadsheet software.

## What the Heck is a Command Line?

I suspect that, after reading the last sentence, the typical windows user has<br/>
a basic question: what the heck is a command line?  Informally, the command<br/>
line is that vaguely intimidating, minimalist screen that the IT specialist at<br/>
work uses to conduct magic rituals.  More formally, it is one of two command<br/>
line shells for the windows operating system that provides an interface<br/>
between a user and the OS.  A windows user can find and open the command line<br/>
by entering "Command Prompt" in the windows search bar.

As stated above, retrosheet’s software applications - "bevent," "bgame," and<br/>
"box" - are designed to run on the windows command line.  Ultimately, this<br/>
approach is cumbersome, requiring a fair amount of setup that potentially<br/>
discourages the use of the applications.  My solution to this problem, a<br/>
python module that circumvents the command line, allows python enthusiasts to<br/>
start with the fun stuff - creating descriptive statistics and exploring the<br/>
actual contents of the data sets.  Since my project obviates the manipulation<br/>
of the command line, it is worth exploring how the command line tools function.

## Legacy Implementation

We are getting ahead of ourselves.  Before we can explore how the retrosheet<br/>
applications work, we must complete some basic setup.  To access the site’s<br/>
information, we have to create a directory comprising the retrosheet event<br/>
files we want to query, in addition to the three aforementioned applications -<br/>
bevent, bgame, and box.  Event files may be downloaded from<br/>
https://www.retrosheet.org/game.htm, while the applications may be downloaded<br/>
from https://www.retrosheet.org/tools.htm.  Note that event files end with<br/>
either the ".EVA" or ".EVN" suffix.  Let's store these files in a directory<br/>
named "event_files."

Now for some bad news: Linux and Unix users are out of luck.  Developed before<br/>
apple products skyrocketed in popularity, the retrosheet applications are<br/>
designed to run on windows OS.  Although the command line can be emulated on<br/>
Linux and Unix operating systems, I have written and tested this project on<br/>
windows, reserving cross platform functionality for a future date.  I cannot<br/>
guarantee that the project module will work on a non-windows operating system.<br/>
My apologies to any mac users.

Once the event files and applications are in the same directory, we can begin<br/>
testing the tools.  First, we call the command line, which should open a<br/>
screen similar to figure 1.  Note that right clicking on the command<br/>
prompt’s header will give us access to properties, allowing us to customize<br/>
the command line to our liking.

```
C:\Users\{your_user_name}>
```
Figure 1 - Command line entry point.

Next, using the cd command - an abbreviation for change directory - navigate<br/>
to the folder where the retrosheet event files and applications are stored.<br/>
Typing a retrosheet application’s name followed by the -h switch will provide<br/>
a broad overview of the application.

```
Expanded game descriptor, version 110(188) of 07/19/2020.
  Type 'bgame -h' for help.
Copyright (c) 2001 by DiamondWare.

bgame generates files suitable for use by dBase or Lotus-like programs.
Each record describes one game.
Usage: bgame [options] eventfile...
options:
  -h        print this help
  -i id     only process game given by id
  -q        ask whether to process each game
  -y year   Year to process (for teamyyyy and aaayyyy.ros).
  -s start  Earliest date to process (mmdd).
  -e end    Last date to process (mmdd).
  -a        generate Ascii-delimited format files (default)
  -ft       generate Fortran format files
  -m        use master player file instead of local roster files
  -f flist  give list of fields to output
              Default is 0-84
  -d        print list of field numbers and descriptions
  The -dxx switches choose a date format for the gamedate field.
  -dsf      slashes, full year: mm/dd/yyyy
  -dsp      slashes, partial year: mm/dd/yy
  -dnf      no slashes, full year: yyyymmdd
  -dnp      no slashes, partial year: yymmdd (the default)
```
Figure 2 - bgame help screen.

Figure 2 shows the bgame help screen.  It provides a brief description of<br/>
the application, followed by an enumeration of the various switches that can<br/>
be utilized in a query.  The switches allow a user to manipulate the dates<br/>
queried and the formatting of any results, and they may be combined in a<br/>
variety of ways.  A quick aside:  is your command line too cluttered?  No<br/>
problem!  A quick "cls" command will clear your screen.

Now that our screen is cleared, let us attempt our first query.  Say we want<br/>
all of the bgame fields associated with the Boston Red Sox for July 2021.  As<br/>
outlined by the help screen, our query will need the following information:<br/>
the string "bgame"; the year to be processed, 2021; the start date, July<br/>
first; the end date, July thirty-first; and the relevant event file,<br/>
2021BOS.eva.  Combining these components into a single query, we get the<br/>
following:

```
{your_file_path}\event_files>bgame -y 2021 -s 0701 -e 0731 2021BOS.eva

 Type 'bgame -h' for help.
Copyright (c) 2001 by DiamondWare.
[Processing file 2021BOS.eva.]
"BOS202107010","210701",0,"Thursday",110,"T","D","KCA","BOS","BOS07",
"bubik001","eovan001","randt901","ticht901","reynj901","lives901","(none)",
"(none)",27913,"","","","2021/07/02 07:19:50","",0,1,82,3,10,0,1,2,188,9,1,15,
...
```
Figure 3 - Example bgame query and truncated output.

Notice that the dates in our query, July first and July thirty-first, are<br/>
padded with zeros.  Failure to pad single digit days or months with zeros will<br/>
result in an empty return value from standard output.  Moreover, as alluded to<br/>
above, the suffix of the queried file carries meaning - event files for<br/>
American League teams end with the suffix ".EVA," while files for National<br/>
League teams end with the suffix ".EVN."  Failure to provide the correct<br/>
suffix will result in an empty return value, as will an incorrect team<br/>
abbreviation. 
 
The information as currently displayed is not particularly helpful.  Indeed,<br/>
it may induce a low-grade migraine in the unsuspecting newcomer.  How can we<br/>
transfer this information to a more digestible form?

Retrosheet recommends redirecting the command line’s standard output to a text<br/>
or csv file.  While this method may have its shortcomings, it is certainly<br/>
preferable to a blob of text superimposed against a bare screen.  To redirect<br/>
standard output, we simply have to place the ">" symbol after our query, along<br/>
with the name and location of the file we want to write.  Our Boston query<br/>
could be rewritten in the following manner: 

```
bgame -y 2021 -s 0701 -e 0731 2021BOS.eva > {your_file_path}\Boston_July_21.csv
```
Figure 4 - Bgame query redirected to csv file.

A csv file has been created and placed in our target directory.  Note that csv<br/>
stands for comma separated values, a format that is commonly used to import<br/>
data to, and export data from, relational databases.

Most queries will mirror our first example.  If we wanted to extract all bgame<br/>
fields up to a certain date, then we would simply drop the -s switch.  For<br/>
example, "bgame -y 2021 -e 0701..." will return a result set up to and<br/>
including July first.  Conversely, "bgame -y 2021 -s 0701..."  will return a<br/>
result set from July first through the end of the regular season.  If no<br/>
column information is specified in either a bgame or bevent query, then column<br/>
defaults are provided.

## Application Shortcomings

This workflow has a number of limitations.  Event files are organized in<br/>
accordance with a team’s home games.  This means that any given event file<br/>
only covers half of a season.  Retrieving the other eighty-one games is no<br/>
trivial matter, and doing so via the command line is tedious and error prone.<br/>
An algorithmic approach to this problem would seem preferable to command line<br/>
mastery.

Moreover, the breadth of major league history is vast, presenting a host of<br/>
problems for users.  Teams change cities and even leagues, which result in new<br/>
team abbreviations and file extensions for query construction.  Not so long<br/>
ago, the Brewers played in the American League, the Astros the National<br/>
League.

Although application output can be redirected to text files, this is not a<br/>
viable solution for long term data storage, nor did the application creators<br/>
intend it as such.  As stated earlier, the text files are meant to be imported<br/>
into database software.  An ordinary user, however, may have no interest in<br/>
creating a MySQL or SQLite database, or even know where to begin learning SQL.

Creating an entire database of results is a substantial roadblock for casual<br/>
users who may only need limited access to the data.  Requesting specific<br/>
fields to answer pointed questions will probably be the most efficient<br/>
approach for the curious fan or fantasy league enthusiast.  There is also the<br/>
matter of managing the considerable amount of required supplemental<br/>
information, such as roster files, field names, and field descriptions.

## Project Implementation

I did not find the prospect of maintaining a directory of text files<br/>
appealing.  Accordingly, this module file came into being.  This module treats<br/>
retrosheet's applications as a black box, using python's run method to capture<br/>
output in python objects rather than text files.  In turn, these objects can<br/>
be used with the Pandas data analysis library to create descriptive<br/>
statistics, bypassing the setup required in the legacy implementation.

"retro_object.py" creates a python class titled "RetroObject," which contains<br/>
two types of methods: formatting methods and emulation methods.  The former<br/>
formats user input into an appropriate query string, while the latter uses the<br/>
query string to call the executables for retrosheet's software applications.
  
The bevent method returns information about every individual play in a<br/>
baseball game, including pitch type, runners on base, batter and hitter<br/>
handedness, etc.   Bgame returns general information about a game, such as<br/>
weather, starting lineups, and stadium attendance.  Both methods return a list<br/>
of lists that can be passed into the Pandas DataFrame method.  Box returns a<br/>
string of box scores that can either be displayed with python's print function<br/>
or stored in a text file.  

All captured output is in the form of a string.  As a result, RetroObject's<br/>
methods are fairly involved, with a considerable amount of conditional logic.<br/>
To the extent that I have deviated from python's PEP8 style guide, it is to<br/>
accommodate the reader in processing these conditional code blocks.

I have attempted to keep in-file comments to a minimum.  In lieu of in-file<br/>
comments, I have used docstrings to convey class and method functionality to<br/>
the reader.  For more descriptive comments about code structure and syntax,<br/>
please read the "code reference" companion file, which elucidates these<br/>
matters.

## Why Use this Project?

Retro_object.py eliminates the query and storage steps inherent in the legacy<br/>
application implementation, allowing users to immediately begin the process of<br/>
creating descriptive statistics.  Importantly, python and its associated<br/>
libraries are open source.  They are one-hundred percent, all caps FREE.<br/>
While Microsoft Excel is excellent spreadsheet software, it does carry a hefty<br/>
price-tag, with Microsoft incentivizing subscriptions over direct software<br/>
ownership.  Additionally, working entirely in Excel carries limitations,<br/>
especially with larger data sets.  As a general-purpose programming language,<br/>
python and its associated libraries provide functionality that simply does not<br/>
exist within excel.  There is nothing that can be done in excel that cannot be<br/>
done more effectively in python.

But that is enough praise for python and open-source projects - for now,<br/>
anyway.  Some examples are in order.

## July Strikeouts at Boston Home Games:  A Test Case

To demonstrate the module’s capabilities, we will obtain information about<br/>
every July strikeout at Fenway during the 2021 season.  We will use the python<br/>
standard library and a third-party extension, "Pandas," to conduct our<br/>
research.  The source code for this example can be found in the following<br/>
.ipynb files, which are located in the "example_notebooks" directory:<br/>
"first_notebook," "second_notebook," and "third_notebook."  The products of<br/>
these exports, three similarly named "july_strikeouts" csv files, can be found<br/>
in the "project_exports" directory.

As a matter of convention, import statements - statements that provide access<br/>
to code written in another module - are written at the top level of a python<br/>
file.  We begin first_notebook with two imports: "import pandas as pd" and<br/>
"import retro_object as ro."  The former imports the Pandas data analysis<br/>
library, providing us access to an impressive set of numeric and data<br/>
manipulation methods.  The latter provides us access to the retro_object.py<br/>
module, which contains the RetroObject class and retrosheet peripherals.<br/>
Methods and attributes associated with imports may be called through dot<br/>
notation.  For example, pd.DataFrame() or ro.bgame().

Now for the fun part.  We have to consider which RetroObject method to call.<br/>
Since we want information about events within a game, a call to bevent is in<br/>
order.   Our ultimate goal is to construct a Pandas DataFrame, the predominant<br/>
Pandas data structure that enables the bulk of the library’s functionality.<br/>
Since bevent returns a list of lists, constructing our desired DataFrame is as<br/>
simple as passing a call to bevent into DataFrame’s data parameter, as<br/>
captured by figure 5.  Note that the call to bevent does not use padded<br/>
zeros, and it accommodates both string and numeric input.  After passing<br/>
bevent as an argument into the data parameter, we pass a list comprehension as<br/>
an argument into the columns parameter.  This merits an explanation.

```python
# Create a pandas DataFrame for Boston's 
# July 2021 results using bevent.
bostonJulyEvents = pd.DataFrame(
    data = boston.bevent(
        yearStart = 2021,
        start = 71,
        end = 731 
    ),
    columns = [ro.beventFieldsDict[col] for col in boston.columns]
)
```
Figure 5 - Bevent call from [first_notebook.ipynb](../example_notebooks/first_notebook.ipynb)

Our Boston RetroObject retains state, allowing us to access the columns<br/>
attribute we passed into bevent.  Simply put, the list comprehension iterates<br/>
over the column numbers that compose the columns attribute, passing each<br/>
number into "ro.beventFieldsDict," a dictionary.  A dictionary is a collection<br/>
of key-value pairs.  By passing a key - column number into beventFieldsDict,<br/>
we receive a value - column name in return. 
 
Voila!  Using a Boston RetroObject, we have successfully created a Pandas<br/>
DataFrame.  This DataFrame contains the default bevent fields for Boston’s<br/>
July 2021 results.  A cursory review of the DataFrame raises an important<br/>
question, however.  How are we going to filter this information?  Printing the<br/>
DataFrame reveals that it is nine-hundred-thirty rows by thirty-six columns.

As it turns out, we will retrieve our desired information with ease.  The<br/>
Pandas method query - not to be confused with the colloquial use of the term<br/>
deployed throughout this synopsis - is a Pandas method that allows us to filter<br/>
a DataFrame’s records on the basis of a Boolean expression.  We can express a<br/>
simple yet powerful request with query:  if the event text column contains a<br/>
"K," then include the record in our result set.  Although we can execute this<br/>
query against the original DataFrame by setting "in place" to True, we will<br/>
create a new DataFrame with our query results, titled "strikeThree."

```python
# Strikeouts at Boston home games, July 2021. 
strikeThree = (
    bostonJulyEvents
    .query(""" `event text*` == 'K' """)
    .filter([
        "game id*", "balls*", "strikes*",
        "visiting team*","batting team*",
        "res batter*", "res batter hand*",
        "res pitcher*", "res pitcher hand*"
    ])
)
```
Figure 6 - Pandas query from [first_notebook.ipynb](../example_notebooks/first_notebook.ipynb)

After executing this query, we filter for the columns we would like to view,<br/>
exporting the results to a csv file titled "july_strikeouts_first_export.csv."<br/>
Let’s [open this file](../project_exports/july_strikeouts_first_export.csv) with excel and view the results.

A nice result for minimal effort, but we can do better.  Examining our<br/>
spreadsheet, we realize that our data must be refined.  There are no dates<br/>
associated with these records.  Rather, we have received a game id, a<br/>
difficult to decipher, alphanumeric representation of the date and venue.<br/>
Then there is the matter of the "res batter" and "res pitcher" columns, which<br/>
have returned a primary key representation of the players’ names.  This<br/>
normalization of the data is actually an incredible feat on retrosheet’s part,<br/>
but it can bemuse those hoping to glean a quick insight from the tools.

Python’s standard library provides us with all of the tools we need to extract<br/>
the date from a game id.  As outlined in figure 7, we write four additional<br/>
import statements at the top of the file.  Collectively, they import the<br/>
datetime class, in addition to a trio of methods from the regex library.<br/>
Subsequently, we define a function titled "idToDate."  The function uses the<br/>
regex methods compile, findall, and sub to parse a game id for its year,<br/>
month, and day components.  Once we have retrieved these components, we pass<br/>
them into datetime and return a date to the caller.

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

# Create a Boston RetroObject.
boston = ro.RetroObject("bos")

# Define a function to extract the date from a game id.
def idToDate(gameId: str) -> datetime:
    pattern = compile("[A-Z]{3}(\d{4})(\d{2})(\d{2})\d")
    nums = sub(pattern, r"\1,\2,\3", gameId)
    nums = [
        int(sub("^0", "", val)) if findall("^0", val) else int(val) 
        for val in nums.split(sep = ",")
    ]
    return datetime(year = nums[0], month = nums[1], day = nums[2]).date()
```
Figure 7 - idToDate function from [second_notebook.ipynb](../example_notebooks/second_notebook.ipynb)

After defining idToDate and writing our additional import statements, we chain<br/>
an additional method to strikeThree - assign, which allows us to add new<br/>
series to the DataFrame.  We add five additional series to the DataFrame: date,<br/>
batter last name, batter first name, pitcher last name, and pitcher first<br/>
name.  We create the date series by applying the idToDate function to the game<br/>
id series.  Similarly, players’ names are assigned to the DataFrame by<br/>
applying dictionary calls to the res batter and res pitcher series.  We<br/>
conclude our adjustments by reversing the normalization in the batting team<br/>
column, replacing zero with "away" and one with "home."<br/>
[july_strikeouts_second_export](../project_exports/july_strikeouts_second_export.csv) captures the results of our revised dataframe.  Much better,<br/>
wouldn’t you say?

```python
# Strikeouts at Boston home games, July 2021. 
strikeThree = (
    bostonJulyEvents
    .query(""" `event text*` == "K" """)
    .assign(
        date = (
            bostonJulyEvents["game id*"]
            .apply(lambda x: idToDate(x))
        ),
        batter_last_name = (
            bostonJulyEvents["res batter*"]
            .apply(lambda x: bioDict[x]["LAST"])
        ), 
        batter_first_name = (
            bostonJulyEvents["res batter*"]
            .apply(lambda x: bioDict[x]["FIRST"])
        ), 
        pitcher_last_name = (
            bostonJulyEvents["res pitcher*"]
            .apply(lambda x: bioDict[x]["LAST"])
        ),
        pitcher_first_name = (
            bostonJulyEvents["res pitcher*"]
            .apply(lambda x: bioDict[x]["FIRST"])
        )
    )
    .filter([
        "game id*", "date", "balls*", "strikes*",
        "visiting team*","batting team*",
        "batter_last_name", "batter_first_name",
        "res batter*", "res batter hand*",
        "pitcher_last_name", "pitcher_first_name",
        "res pitcher*", "res pitcher hand*"
    ])
)
```
Figure 8 - DataFrame with call to idToDate.  From [second_notebook.ipynb](../example_notebooks/second_notebook.ipynb)

Let’s up the ante one last time.  Instead of retrieving strikeout information<br/>
for July 2021, we will obtain strikeout information for an entire decade, July<br/>
2010 through July 2020.  Surely this will require a massive effort on our<br/>
part...?

The cost of this additional information?  A single line.  Passing arguments<br/>
into bevent’s year start and year end parameters executes the desired query<br/>
for all years in the range, inclusive of the bounds.  The final product of our<br/>
efforts, ["july_strikeouts_third_export](../project_exports/july_strikeouts_third_export.csv)," details all<br/>
two-thousand-one-hundred-eight Fenway strikeouts from July 2010 through July<br/>
2020.

```python
# Create a pandas DataFrame for Boston's 
# July results, 2010 through 2020.
bostonJulyEvents = pd.DataFrame(
    data = boston.bevent(
        yearStart = 2010,
        yearEnd = 2020,
        start = 71,
        end = 731 
    ),
    columns = [ro.beventFieldsDict[col] for col in boston.columns]
)
```
Figure 9 - Revised bevent call from [third_notebook.ipynb](../example_notebooks/third_notebook.ipynb)

## The Sky is the Limit

How should users utilize this module?  Our test case demonstrates that it can<br/>
seamlessly interact with python's data science stack, namely pandas.  To that<br/>
end, I envision a future where a user can package retro_object.py with pandas<br/>
and seaborn to produce high quality data visualizations.  The module's utility<br/>
is not limited to data analysis, however.  Paired with an object relational<br/>
mapper like sqlAlchemy, this module could drastically reduce the effort<br/>
required to build a robust database of MLB statistics, games, and players.  A<br/>
populated database could serve as the springboard to any number of interesting<br/>
projects, such as expected value calculators and Monte Carlo simulations.<br/>
Whatever purpose it serves, at the very least, I hope it saves you, dear<br/>
reader, a little bit of that most precious resource - time. 

I would like to conclude this synopsis with a heartfelt thank you to<br/>
retrosheet.  I pursued this project to increase my productivity with their<br/>
tools, which remain invaluable resources for baseball enthusiasts.  That they<br/>
make such a vast collection of historical information available, free of<br/>
charge and free of advertisements, is almost anachronistic.  I cannot thank<br/>
them enough for maintaining this beacon of the web.