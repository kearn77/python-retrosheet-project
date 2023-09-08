# Project Overview<br/>

Some time ago, as a first attempt at a programming project, I cobbled<br/>
together a database file containing MLB results and statistics over the<br/>
last twenty seasons.  I accomplished this by scraping<br/>
sportsreference.com, which has a generous web-scraping policy that<br/>
accommodates most get requests.  Given the massive amount of<br/>
information I needed to scrape, however, even sportsreference’s<br/>
web-scraping policy presented difficulties I struggled to overcome.<br/>
Trust me, it is difficult to capture data in a timely manner capped at<br/>
a request per second!   Fortunately, I found a more complete,<br/>
open-source set of resources - [retrosheet.org](https://www.retrosheet.org/ "Links to retrosheet.").<br/>

Founded in 1989, retrosheet is a record keeping project that<br/>
computerizes play-by-play accounts of Major League baseball games.<br/>
Information on the site is free to use, under the condition that any<br/>
project developed with the site's information [properly cites the site](/IMPORTANT_RETROSHEET_NOTICE.md).<br/>

Although retrosheet makes staggering amounts of information available<br/>
free of charge, I quickly encountered a problem - the information<br/>
largely exists in specialty files that can only be queried by the<br/>
site's software applications. Further complicating matters, the<br/>
applications are meant to run on a windows command line, with output<br/>
redirected to text files that can be imported into database and<br/>
spreadsheet software.<br/>

My solution to this problem -  a python module that emulates the command<br/>
line and wraps around the retrosheet applications - allows python<br/>
enthusiasts to start with the fun stuff - creating descriptive<br/>
statistics and exploring the actual contents of the data sets.<br/>

After a robust refactoring, the project's main module, retro_object.py,<br/>
calls retrosheet's bevent and bgame applications and returns a<br/>
formatted Pandas DataFrame.<br/>

A second module, frame_functions.py, provides a number of functions<br/>
for formatting the bevent and bgame DataFrames.  This module is<br/>
designed for people who are not familiar with the Pandas library and<br/>
would benefit from a helping hand.<br/>

## Table of Contents<br/>

### [Project Summary](/project_summary/)<br/>

The project summary directory contains a markdown file titled<br/>
synopsis.md.  It provides a broad overview of the project and a test<br/>
case for the modules.<br/>

### [Code Reference](/code_reference/)<br/>
This directory contains numerous markdown files corresponding to the<br/>
python modules stored within "Project Scripts."  These files provide an<br/>
overview of a module’s role within the context of the broader<br/>
project.  While it is not an exhaustive, line-by-line accounting of the<br/>
project’s code, it should provide an in-depth description of the<br/>
project’s mechanics.<br/>


### [Project Scripts](/project_scripts/)<br/>

The scripts directory contains the project's eight python files:<br/>
columns.py, dates.py, dirs.py exceptions.py, formatting.py,<br/>
frame_functions.py, retro_object.py, and teams.py  Anyone reviewing<br/>
this directory would benefit from having the Code Reference available<br/>
in a split view.<br/>

### [Example Notebooks](/example_notebooks/)<br/>

The notebooks directory provides a test case for module usage.  As<br/>
outlined in the project’s synopsis, the test case examines strikeouts<br/>
at Fenway park from 2010 through 2020.  For the following reasons, the<br/>
code contained within this directory utilizes Jupyter Notebooks as an<br/>
environment.<br/>

-  It is the tool of choice among data scientists and data enthusiasts.<br/>
Consequently, it seemed a logical choice for visualizing the data<br/>
contained within retrosheet’s event files.<br/>

-  Moreover, because it provides an interactive environment, it reduces<br/>
the growing pains associated with some of python’s most popular<br/>
third-party libraries, such as matplotlib and seaborn.<br/>

### [Project Exports](/project_exports/)<br/>

The exports directory contains the .csv files created by the example<br/>
notebooks.<br/>

### [JSON Files](/json_files/)<br/>

The JSON directory contains four files - bevent_fields, bgame_fields,<br/>
team_extensions, and bio_information - which accomplish the following:<br/>

#### bevent_fields.json<br/>

Stores the column information associated with bevent.exe.  Can be used<br/>
to create a python dictionary that populates a pandas DataFrame with<br/>
appropriate column titles.  The key-value relationship is of the form<br/>
int -> str, where int is a number zero to ninety-six and str is a<br/>
column title.<br/>

#### bgame_fileds.json<br/>

Stores the column information associated with bgame.exe.  Can be used to<br/>
create a python dictionary that populates a pandas DataFrame with<br/>
appropriate column titles.  The key-value relationship is of the form<br/>
int -> str, where int is a number zero to eighty-four and str is a<br/>
column title.<br/>

#### team_extensions.json<br/>

Stores team abbreviations for every major league baseball team.<br/>
Abbreviations are used when calling bevent, bgame, and box from the<br/>
command line.  Similarly, a RetroObject is instantiated when passed a<br/>
valid team abbreviation.  The key-value relationship is of the form str<br/>
-> list\list\, where str is a team abbreviation that returns a team’s<br/>
historical information.<br/>

#### bio_information.json<br/>

Contains player biographical data.  This data is stored in relation to a<br/>
retrosheet player id, an alphanumeric representation of a player’s<br/>
name.  The key-value relationship is of the form str -> dict, where str<br/>
is a player id that returns a dictionary of biographical information.<br/>

### [Event Files](/event_files/)<br/>

Normally, the event_files folder would contain the following:<br/>

- [bevent.exe](https://www.retrosheet.org/resources/resources1.html "Links to retrosheet.");<br/>

- [bgame.exe](https://www.retrosheet.org/resources/resources1.html "Links to retrosheet.");<br/>

- [Event files](https://www.retrosheet.org/game.htm "Links to retrosheet.") ending in .EVN or .EVA;<br/>

- [Roster files](https://www.retrosheet.org/game.htm "Links to retrosheet.") ending in .ROS;<br/>

- [Team files](https://www.retrosheet.org/game.htm "Links to retrosheet.") of the form TEAM2000, TEAM2001, ...<br/>

To avoid cluttering the repository, I have included links to these<br/>
resources rather than the resources themselves.  They are required to<br/>
successfully run the test cases outlined in the example notebooks.<br/>

### Requirements<br/>

The contents contained within the [Project Scripts](/project_scripts/), [JSON Files](/json_files/), and<br/>
[Event Files](/event_files/) directories are required to run the project.<br/>

I used python’s standard library for the majority of the project’s<br/>
scripts. Two files - retro_object.py and frame_functions.py - use<br/>
Pandas, a popular data science library, to create and manipulate<br/>
DataFrames.<br/>

The example notebooks rely on two third-party libraries:<br/>
Pandas, the aforementioned data science library, and notebooks,<br/>
Jupyter’s environment for interactive computing.<br/>

For more information about the project’s development environment,<br/>
please reference [requirements.txt](/requirements.txt).<br/>

### Status<br/>

The project's first refactoring has been pushed to the main branch!<br/>
A clear separation of concerns has been emphasized, with dedicated<br/>
modules for parsing column information, date information, and team<br/>
specifics.  Moreover, the retro_object.py module has been rewritten<br/>
with a singular purpose - running the bevent and bgame executables and<br/>
returning a Pandas DataFrame.  Calls to the box executable have been<br/>
deprecated.  The following goals remain:<br/>

- Develop more robust use cases.<br/>

- Incorporate more of retrosheet’s peripherals into the project.  As<br/>
it is currently composed, the project includes only what is necessary<br/>
to parse the event files for player statistics and biographical<br/>
information.<br/>