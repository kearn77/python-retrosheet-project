## Project Overview

Some time ago, as a first attempt at a programming project, I cobbled<br/>
together a database file containing MLB results and statistics over the last<br/>
twenty seasons.  I accomplished this by scraping sportsreference.com, which<br/>
has a generous web-scraping policy that accommodates most get requests.  Given<br/>
the massive amount of information I needed to scrape, however, even<br/>
sportsreference’s web-scraping policy presented difficulties I struggled to<br/>
overcome.  Trust me, it is difficult to capture data in a timely manner capped<br/>
at a request per second!   Fortunately, I found a more complete, open-source<br/>
set of resources - [retrosheet.org.](https://www.retrosheet.org/ "Links to retrosheet.")

Founded in 1989, retrosheet is a record keeping project that computerizes<br/>
play-by-play accounts of Major League baseball games.  Information on the site<br/>
is free to use, under the condition that any project developed with the site's<br/>
information [properly cites the site](/IMPORTANT_RETROSHEET_NOTICE.md).

Although retrosheet makes staggering amounts of information available free<br/>
of charge, I quickly encountered a problem - the information largely exists in<br/>
specialty files that can only be queried by the site's software applications.<br/>
Further complicating matters, the applications are meant to run on a windows<br/>
command line, with output redirected to text files that can be imported into<br/>
database and spreadsheet software.

My solution to this problem –  a python module that emulates the command<br/>
line and wraps around the retrosheet applications – allows python enthusiasts<br/>
to start with the fun stuff – creating descriptive statistics and exploring<br/>
the actual contents of the data sets.

## Table of Contents

### [Project Summary](/project_summary/)

The project summary directory contains two markdown files: synopsis.md and<br/>
code_reference.md.  The former provides a broad overview of the project and a<br/>
test case for the modules.  The latter provides a summary of the<br/>
repository’s code.  Newcomers to the repository should start here.

### [Project Scripts](/project_scripts/)

The scripts directory contains the project's python files.  Anyone<br/>
reviewing this directory would benefit from having the [code reference](/project_summary/code_reference.md) on hand.<br/>
The bulk of the code exists within [retro_object.py](/project_scripts/retro_object.py), which creates a python<br/>
class capable of calling retrosheet's software.

### [Example Notebooks](/example_notebooks/)

The notebooks directory provides a test case for module usage.  As<br/>
outlined in the project’s synopsis, the test case examines strikeouts at<br/>
Fenway park from 2010 through 2020.  For the following reasons, the code<br/>
contained within this directory utilizes Jupyter Notebooks as an environment.<br/>

-  It is the tool of choice among data scientists and data enthusiasts.<br/>
Consequently, it seemed a logical choice for visualizing the data contained<br/>
within retrosheet’s event files.<br/>

-  Moreover, because it provides an interactive environment, it reduces the<br/>
growing pains associated with some of python’s most popular third-party<br/>
libraries, such as matplotlib and seaborn.

### [Project Exports](/project_exports/)

The exports directory contains the .csv files created by the example<br/>
notebooks.  

### [JSON Files](/json_files/)

The JSON directory contains four files - bevent_fields, bgame_fields,<br/>
team_extensions, and bio_information - which accomplish the following:

-	bevent_fields.json

Stores the column information associated with bevent.exe.  Can be used to<br/>
create a python dictionary that populates a pandas DataFrame with appropriate<br/>
column titles.  The key-value relationship is of the form int -> str, where<br/>
int is a number zero to ninety-six and str is a column title.

-	bgame_fileds.json

Stores the column information associated with bgame.exe.  Can be used to<br/>
create a python dictionary that populates a pandas DataFrame with appropriate<br/>
column titles.  The key-value relationship is of the form int -> str, where<br/>
int is a number zero to eighty-four and str is a column title.

-	team_extensions.json

Stores team abbreviations for every major league baseball team.<br/>
Abbreviations are used when calling bevent, bgame, and box from the command<br/>
line.  Similarly, a RetroObject is instantiated when passed a valid team<br/>
abbreviation.  The key-value relationship is of the form str -> list\[list\],<br/>
where str is a team abbreviation that returns a team’s historical information.

-	bio_information.json

Contains player biographical data.  This data is stored in relation to a<br/>
retrosheet player id, an alphanumeric representation of a player’s name.  The<br/>
key-value relationship is of the form str -> dict, where str is a player id<br/>
that returns a dictionary of biographical information.

### [Event Files](/event_files/)

Normally, the event_files folder would contain the following:

- [bevent.exe](https://www.retrosheet.org/resources/resources1.html "Links to retrosheet.");

- [bgame.exe](https://www.retrosheet.org/resources/resources1.html "Links to retrosheet.");

- [box.exe](https://www.retrosheet.org/resources/resources1.html "Links to retrosheet.");

- [Event files](https://www.retrosheet.org/game.htm "Links to retrosheet.") ending in .EVN or .EVA;

- [Roster files](https://www.retrosheet.org/game.htm "Links to retrosheet.") ending in .ROS;

- [Team files](https://www.retrosheet.org/game.htm "Links to retrosheet.") of the form TEAM2000, TEAM2001, ...

To avoid cluttering the repository, I have included links to these<br/>
resources rather than the resources themselves.  They are required to<br/>
successfully run the test cases outlined in the example notebooks.

## Requirements

The contents contained within the "[Project Scripts](/project_scripts/),", “[JSON Files](/json_files/)," and<br/>
“[Event Files](/event_files/)” directories are required to run the project.

I used python’s standard library for the majority of the project’s scripts.<br/>
The only deviation from this practice is an import of numpy’s nan attribute in<br/>
[retro_object.py](/project_scripts/retro_object.py).

The example notebooks rely on two third-party libraries:<br/>
pandas, a popular data science library; and notebooks, Jupyter’s environment<br/>
for interactive computing.

For more information about the project’s development environment, please<br/>
reference [requirements.txt](/requirements.txt).

## Status

This is far from a finished project.  In the future, I hope to accomplish the<br/>
following:

-	Reduce the complexity of retro_object.py.  As it stands, this module is<br/>
approximately seven-hundred lines long, although it could be more terse,<br/>
expressive, and idiomatic.

-	Develop more robust use cases.

-	Incorporate more of retrosheet’s peripherals into the project.  As it is<br/>
currently composed, the project includes only what is necessary to parse the<br/>
event files for player statistics and biographical information.

Regardless of the project's current state, hopefully anyone reading this<br/>
repository can glean something useful from my efforts.