## Project Inception<br/>

Some time ago, as a first attempt at a programming project, I cobbled<br/>
together a database file containing MLB results and statistics over the<br/>
last twenty seasons.  I accomplished this by scraping<br/>
sportsreference.com, which has a generous web-scraping policy that<br/>
accommodates most get requests.  Given the massive amount of<br/>
information I needed to scrape, however, even sportsreference’s<br/>
web-scraping policy presented difficulties I struggled to overcome.<br/>
Trust me, it is difficult to capture data in a timely manner capped at<br/>
a request per second!   Fortunately, I found a more complete,<br/>
open-source set of resources - [retrosheet.org](https://www.retrosheet.org "Links to retrosheet.").<br/>

Founded in 1989, retrosheet is a record keeping project that<br/>
computerizes play-by-play accounts of Major League baseball games.<br/>
Information on the site is free to use, under the condition that any<br/>
project developed with the site's information [properly cites the site](../IMPORTANT_RETROSHEET_NOTICE.md).<br/>

Although retrosheet makes staggering amounts of information available<br/>
free of charge, I quickly encountered a problem - the information<br/>
largely exists in specialty files that can only be queried by the<br/>
site's software applications. Further complicating matters, the<br/>
applications are meant to run on a windows command line, with output<br/>
redirected to text files that can be imported into database and<br/>
spreadsheet software.<br/>

## What the Heck is a Command Line?<br/>

I suspect that, after reading the last sentence, the typical windows<br/>
user has a basic question: what the heck is a command line?<br/>
Informally, the command line is that vaguely intimidating, minimalist<br/>
screen that the IT specialist at work uses to conduct magic rituals.<br/>
More formally, it is one of two command line shells for the windows<br/>
operating system that provides an interface between a user and the OS.<br/>
A windows user can find and open the command line by entering "Command<br/>
Prompt" in the windows search bar.<br/>

As stated above, retrosheet’s software applications - "bevent" and<br/>
"bgame" - are designed to run on the windows command line.<br/>
Ultimately, this approach is cumbersome, requiring a fair amount of<br/>
setup that potentially discourages the use of the applications.  My<br/>
solution to this problem, a python module that circumvents the command<br/>
line, allows python enthusiasts to start with the fun stuff - creating<br/>
descriptive statistics and exploring the actual contents of the data<br/>
sets.  Since my project obviates the manipulation of the command line,<br/>
it is worth exploring how the command line tools function.<br/>

## Legacy Implementation<br/>

We are getting ahead of ourselves.  Before we can explore how the<br/>
retrosheet applications work, we must complete some basic setup.  To<br/>
access the site’s information, we have to create a directory<br/>
comprising the retrosheet event files we want to query, in addition to<br/>
the two aforementioned applications - bevent and bgame.  Event files<br/>
may be downloaded from https://www.retrosheet.org/game.htm, while the<br/>
applications may be downloaded from https://www.retrosheet.org/tools.htm.<br/>
Note that event files end with either the ".EVA" or ".EVN" suffix.<br/>
Let's store these files in a directory named "event_files."<br/>

Now for some bad news: Linux and Unix users are out of luck.  Developed<br/>
before apple products skyrocketed in popularity, the retrosheet<br/>
applications are designed to run on windows OS.  Although the command<br/>
line can be emulated on Linux and Unix operating systems, I have<br/>
written and tested this project on windows, reserving cross platform<br/>
functionality for a future date.  I cannot guarantee that the project<br/>
will work on a non-windows operating system. My apologies to any mac<br/>
users.<br/>

Once the event files and applications are in the same directory, we can<br/>
begin testing the tools.  First, we call the command line, which should<br/>
open a screen similar to figure 1.  Note that right clicking on the<br/>
command prompt’s header will give us access to properties, allowing<br/>
us to customize the command line to our liking.<br/>

```
C:\Users\{your_user_name}>
```
Figure 1 - Command line entry point.<br/>

Next, using the cd command - an abbreviation for change directory -<br/>
navigate to the folder where the retrosheet event files and<br/>
applications are stored. Typing a retrosheet application’s name<br/>
followed by the -h switch will provide a broad overview of the<br/>
application.<br/>

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
Figure 2 - bgame help screen.<br/>

Figure 2 shows the bgame help screen.  It provides a brief description<br/>
of the application, followed by an enumeration of the various switches<br/>
that can be utilized in a query.  The switches allow a user to<br/>
manipulate the dates queried and the formatting of any results, and<br/>
they may be combined in a variety of ways.  A quick aside:  is your<br/>
command line too cluttered?  No problem!  A quick "cls" command will<br/>
clear your screen.<br/>

Now that our screen is cleared, let us attempt our first query.  Say we<br/>
want all of the bgame fields associated with the Boston Red Sox for<br/>
July 2021.  As outlined by the help screen, our query will need the<br/>
following information: the string "bgame"; the year to be processed,<br/>
2021; the start date, July first; the end date, July thirty-first; and<br/>
the relevant event file, 2021BOS.eva.  Combining these components into<br/>
a single query, we get the following:<br/>

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
Figure 3 - Example bgame query and truncated output.<br/>

Notice that the dates in our query, July first and July thirty-first,<br/>
are padded with zeros.  Failure to pad single digit days or months with<br/>
zeros will result in an empty return value from standard output.<br/>
Moreover, as alluded to above, the suffix of the queried file carries<br/>
meaning - event files for American League teams end with the suffix<br/>
".EVA," while files for National League teams end with the suffix<br/>
".EVN."  Failure to provide the correct suffix will result in an empty<br/>
return value, as will an incorrect team abbreviation.<br/>

The information as currently displayed is not particularly helpful.<br/>
Indeed, it may induce a low-grade migraine in the unsuspecting<br/>
newcomer.  How can we transfer this information to a more digestible<br/>
form?<br/>

Retrosheet recommends redirecting the command line’s output to a text<br/>
or csv file.  While this method may have its shortcomings, it is<br/>
certainly preferable to a blob of text superimposed against a bare<br/>
screen.  To redirect standard output, we simply have to place the ">"<br/>
symbol after our query, along with the name and location of the file we<br/>
want to write.  Our Boston query could be rewritten in the following<br/>
manner:<br/>

```
bgame -y 2021 -s 0701 -e 0731 2021BOS.eva > {your_file_path}\Boston_July_21.csv
```
Figure 4 - Bgame query redirected to csv file.<br/>

A csv file has been created and placed in our target directory.  Note<br/>
that csv stands for comma separated values, a format that is commonly<br/>
used to import data to, and export data from, relational databases.<br/>

Most queries will mirror our first example.  If we wanted to extract<br/>
all bgame fields up to a certain date, then we would simply drop the -s<br/>
switch.  For example, "bgame -y 2021 -e 0701..." will return a result<br/>
set up to and including July first.  Conversely, "bgame -y 2021 -s<br/>
0701..."  will return a result set from July first through the end of<br/>
the regular season.  If no column information is specified in either a<br/>
bgame or bevent query, then column defaults are provided.<br/>

## Application Shortcomings<br/>

This workflow has a number of limitations.  Event files are organized in<br/>
accordance with a team’s home games.  This means that any given event<br/>
file only covers half of a season.  Retrieving the other eighty-one<br/>
games is no trivial matter, and doing so via the command line is<br/>
tedious and error prone. An algorithmic approach to this problem would<br/>
seem preferable to command line mastery.<br/>

Moreover, the breadth of major league history is vast, presenting a<br/>
host of problems for users.  Teams change cities and even leagues,<br/>
which result in new team abbreviations and file extensions for query<br/>
construction.  Not so long ago, the Brewers played in the American<br/>
League, the Astros the National League.<br/>

Although application output can be redirected to text files, this is<br/>
not a viable solution for long term data storage, nor did the<br/>
application creators intend it as such.  As stated earlier, the text<br/>
files are meant to be imported into database software.  An ordinary<br/>
user, however, may have no interest in creating a MySQL or SQLite<br/>
database, or even know where to begin learning SQL.<br/>

Creating an entire database of results is a substantial roadblock for<br/>
casual users who may only need limited access to the data.  Requesting<br/>
specific fields to answer pointed questions will probably be the most<br/>
efficient approach for the curious fan or fantasy league enthusiast.<br/>
There is also the matter of managing the considerable amount of<br/>
required supplemental information, such as roster files, field names,<br/>
and field descriptions.<br/>

## Project Implementation<br/>

I did not find the prospect of maintaining a directory of text files<br/>
appealing.  Accordingly, this project came into being.  This project<br/>
treats retrosheet's applications as a black box, using python's run<br/>
method to capture output as a Pandas DataFrame rather than a text file.<br/>
In turn, these DataFrames can be used with the Pandas data analysis<br/>
library to create descriptive statistics, bypassing the setup required<br/>
in the legacy implementation.<br/>

The bevent method returns information about every individual play in a<br/>
baseball game, including pitch type, runners on base, batter and hitter<br/>
handedness, etc.   Bgame returns general information about a game, such<br/>
as weather, starting lineups, and stadium attendance.<br/>

## Why Use this Project?<br/>

Retro_object.py eliminates the query and storage steps inherent in the<br/>
legacy application implementation, allowing users to immediately begin<br/>
the process of creating descriptive statistics.  Importantly, python<br/>
and its associated libraries are open source.  They are one-hundred<br/>
percent, all caps FREE. While Microsoft Excel is excellent spreadsheet<br/>
software, it does carry a hefty price-tag, with Microsoft incentivizing<br/>
subscriptions over direct software ownership.  Additionally, working<br/>
entirely in Excel carries limitations, especially with larger data<br/>
sets.  As a general-purpose programming language, python and its<br/>
associated libraries provide functionality that simply does not exist<br/>
within excel.  There is nothing that can be done in excel that cannot<br/>
be done more effectively in python.<br/>

But that is enough praise for python and open-source projects - for now,<br/>
anyway.  Some examples are in order.<br/>


To demonstrate the module’s capabilities, we will obtain information<br/>
about every July strikeout at Fenway during the 2021 season.  We will<br/>
use the python standard library and a third-party extension, "Pandas,"<br/>
to conduct our research. The source code for this example can be found<br/>
in the following .ipynb files, which are located in the<br/>
[example_notebooks](../example_notebooks/) directory: [first_notebook](../example_notebooks/first_notebook.ipynb), [second_notebook](../example_notebooks/second_notebook.ipynb), and<br/>
[third_notebook](../example_notebooks/third_notebook.ipynb).  The products of these exports, three similarly named<br/>
"july_strikeouts" csv files, can be found in the [project_exports](../project_exports/)<br/>
directory.<br/>

As a matter of convention, import statements - statements that provide<br/>
access to code written in another module - are written at the top level<br/>
of a python file.  We begin first_notebook by importing the following:<br/>
the datetime class from the datetime library, which provides a number<br/>
of built in methods for structuring and parsing dates; the Path module<br/>
from the pathlib library, which provides methods for navigating file<br/>
paths; and the sys module, which provides access to variables<br/>
maintained by the python interpreter.<br/>

Two bevent and bgame parameters - year and start - take datetime<br/>
objects as their arguments.  Path is used to export the notebook's<br/>
result to the project_exports directory.  Sys amends the system path to<br/>
include the python modules found within the [project_scripts](../project_scripts/) directory.<br/>

Now for the fun part.  We have to consider which Retro_Object method to<br/>
call. Since we want information about events within a game, a call to<br/>
bevent is in order.<br/>

Bevent's parameters are straightforward.  We pass an int, 2021, to<br/>
the year parameter.  Additionally, we pass two datetime objects to year<br/>
and start, which compose the time frame we are researching.  The final<br/>
parameter, columns, takes a list of ints as an argument.  The argument<br/>
passed to the columns parameter - a list comprehension - merits<br/>
explanation.<br/>

All Retro_Objects can access three attributes: bevent_defaults,<br/>
bevent_all, and bgame_all.  They detail the column information<br/>
associated with the two applications.  Each variable is a list of<br/>
two-tuples, with a tuple's first element representing a column's index<br/>
and the second element representing a column's title.  As is implied by<br/>
the variable name, bevent_defaults mirrors the default fields<br/>
associated with the retrosheet application.  Bgame has no defaults.<br/>
The list comprehension passed to columns unpacks the index - an int -<br/>
associated with every tuple entry in bevent_all.<br/>

This comprehension is actually the default argument passed to the<br/>
columns parameter in bevent.  We could have omitted it entirely and<br/>
returned the same result.  Notebooks one and two do not include the<br/>
comprehension.<br/>

```python
# Create a pandas DataFrame for Boston's July 2021 results using
# bevent.
boston_july_events = boston.bevent(
    year=2021,
    start=datetime(2021,7,1),
    end=datetime(2021,7,30),
    columns=[idx for idx,_ in boston.bevent_defaults]
    )
```
Figure 5 - Bevent call from [first_notebook.ipynb](../example_notebooks/first_notebook.ipynb)<br/>

Voila!  Using a Boston Retro_Object, we have successfully created a<br/>
Pandas DataFrame.  This DataFrame contains the default bevent fields<br/>
for Boston’s July 2021 results.  A cursory review of the DataFrame<br/>
raises an important question, however.  How are we going to filter this<br/>
information?  Printing the DataFrame reveals that it is<br/>
nine-hundred-thirty rows by thirty-six columns.<br/>

As it turns out, we will retrieve our desired information with ease.<br/>
The Pandas method query - not to be confused with the colloquial use of<br/>
the term deployed throughout this synopsis - is a Pandas method that<br/>
allows us to filter a DataFrame’s records on the basis of a Boolean<br/>
expression.  We can express a simple yet powerful request with query:<br/>
if the event text column contains a "K," then include the record in our<br/>
result set.  Although we can execute this query against the original<br/>
DataFrame by setting "in place" to True, we will create a new DataFrame<br/>
with our query results, titled "strike_three."<br/>

```python
# Strikeouts at Boston home games, July 2021. 
strike_three = (
    boston_july_events
    .query(""" `event text*` == 'K' """)
    .filter([
        "game id*", "balls*", "strikes*",
        "visiting team*","batting team*",
        "res batter*", "res batter hand*",
        "res pitcher*", "res pitcher hand*"
        ])
    )
```
Figure 6 - Pandas query from [first_notebook.ipynb](../example_notebooks/first_notebook.ipynb).<br/>

After executing this query, we filter for the columns we would like to<br/>
view, exporting the results to a csv file titled<br/>
[july_strikeouts_first_export](/project_exports/july_strikeouts_first_export.csv) Let’s open this file with excel<br/>
and view the results.<br/>

A nice result for minimal effort, but we can do better.  Examining our<br/>
spreadsheet, we realize that our data must be refined.  There are no<br/>
dates associated with these records.  Rather, we have received a game<br/>
id, a difficult to decipher, alphanumeric representation of the date<br/>
and venue. Then there is the matter of the "res batter" and "res<br/>
pitcher" columns, which have returned a primary key representation of<br/>
the players’ names.  This normalization of the data is actually an<br/>
incredible feat on retrosheet’s part, but it can bemuse those hoping<br/>
to glean a quick insight from the tools.<br/>

As alluded to above, this project assumes that a user does not have a<br/>
mastery of the Pandas library.  Consequently, the frame_functions<br/>
module provides a number of built in methods for formatting the<br/>
DataFrames returned by bevent and bgame.<br/>

Two function calls - one to get_bevent_dates, one to insert_names -<br/>
provides our desired formatting.  We conclude our adjustments by<br/>
reversing the normalization in the batting team column, replacing zero<br/>
with "away" and one with "home." [july_strikeouts_second_export](../project_exports/july_strikeouts_second_export.csv) captures<br/>
the results of our revised DataFrame.  Much better, wouldn’t you say?<br/>

```python
# Extract dates from game id* column.  Add batter and pitcher names to
# dataframe.
ff.get_bevent_dates(strike_three)
ff.insert_names(
    frame = strike_three,
    columns = ["res batter*","res pitcher*"]
    )
```
Figure 7 - Get dates and insert names.  From [second_notebook.ipynb](../example_notebooks/second_notebook.ipynb).<br/>

Let’s up the ante one last time.  Instead of retrieving strikeout<br/>
information for July 2021, we will obtain strikeout information for an<br/>
entire decade, July 2010 through July 2020.  Surely this will require a<br/>
massive effort on our part...?<br/>

The cost of this additional information?  A simple for loop.  We create<br/>
an empty list, my_frames, which will store bevent DataFrames.  Next, we<br/>
iterate over the range 2010 through 2021, calling bevent and appending<br/>
its result to my_frames for every iteration through the loop.  Once we<br/>
have exited the loop, we concatenate my_frame's elements into a single<br/>
DataFrame. The final product of our efforts,<br/>
[july_strikeouts_third_export](../project_exports/july_strikeouts_third_export.csv), details all<br/>
two-thousand-one-hundred-eight Fenway strikeouts from July 2010 through<br/>
July 2020.<br/>

```python
# Create a list of frames for the 2010 through 2020 seasons.
my_frames: list[pd.DataFrame] = []
for year in range(2010,2021):
    frame = boston.bevent(
        year = year,
        start = datetime(year,7,1),
        end = datetime(year,7,31)
        )
    my_frames.append(frame)

# Concatenate all of the DataFrames in my_frames.
boston_july_events = pd.concat(objs=my_frames)

# Strikeouts at Boston July home games, 2010 through 2020. 
strike_three = (
    boston_july_events
    .query(""" `event text*` == "K" """)
    .filter([
        "game id*", "date", "balls*", "strikes*",
        "visiting team*","batting team*",
        "res batter*", "res batter hand*",
        "res pitcher*", "res pitcher hand*"
        ])
    )

# Extract dates from game id* column.  Add batter and pitcher names to
# dataframe.
ff.get_bevent_dates(strike_three)
ff.insert_names(
    frame = strike_three,
    columns = ["res batter*","res pitcher*"]
    )
```
Figure 8 - Revised bevent call from [third_notebook.ipynb](../example_notebooks/third_notebook.ipynb).<br/>

## The Sky is the Limit<br/>

How should users utilize this module?  Our test case demonstrates that<br/>
it can seamlessly interact with python's data science stack, namely<br/>
pandas.  To that end, I envision a future where a user can pair<br/>
retro_object.py with pandas and seaborn to produce high quality data<br/>
visualizations.  The module's utility is not limited to data analysis,<br/>
however.  Paired with an object relational mapper like sqlAlchemy, this<br/>
module could drastically reduce the effort required to build a robust<br/>
database of MLB statistics, games, and players.  A populated database<br/>
could serve as the springboard to any number of interesting projects,<br/>
such as expected value calculators and Monte Carlo simulations.<br/>
Whatever purpose it serves, at the very least, I hope it saves you,<br/>
dear reader, a little bit of that most precious resource - time.<br/>

I would like to conclude this synopsis with a heartfelt thank you to<br/>
retrosheet.  I pursued this project to increase my productivity with<br/>
their tools, which remain invaluable resources for baseball<br/>
enthusiasts.  That they make such a vast collection of historical<br/>
information available, free of charge and free of advertisements, is<br/>
almost anachronistic.  I cannot thank them enough for maintaining this<br/>
beacon of the web.<br/>