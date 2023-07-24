# Project Overview

Several months ago, as a first attempt at a programming project, I cobbled
together a database file containing MLB results and statistics over the last
twenty seasons.  I accomplished this by scraping sportsreference.com, which
has a generous web-scraping policy that accommodates most get requests.  Given
the massive amount of information I needed to scrape, however, even
sportsreference’s web-scraping policy presented difficulties I struggled to 
overcome.  Trust me, it is difficult to capture data in a timely manner capped
at a request per second!   Fortunately, I found a more complete, open-source
set of resources - [retrosheet.com.](https://www.retrosheet.org/)

Founded in 1989, retrosheet is a record keeping project that computerizes
play-by-play accounts of Major League baseball games.  Information on the site
is free to use, under the condition that any project developed with the site's
information [properly cites the site](/IMPORTANT_RETROSHEET_NOTICE.md).

Although retrosheet makes staggering amounts of information available free of
charge, I quickly encountered a problem - the information largely exists in
specialty files that can only be queried by the site's software applications.
Further complicating matters, the applications are meant to run on a windows
command line, with output redirected to text files that can be imported into
database and spreadsheet software.

My solution to this problem –  a python module that emulates the command
line and wraps around the retrosheet applications – allows python enthusiasts
to start with the fun stuff - creating descriptive statistics and exploring
the actual contents of the data sets.

## Table of Contents

I would suggest approaching the repository in the following order:

## Core Material

### [Project Summary](/project_summary/)

The project summary directory contains two markdown files: synopsis.md and
code_reference.md.  The former provides a broad overview of the project and a
test case for the module.  The latter provides a summary of the
repository’s code.

### [Project Scripts](/project_scripts/)

The scripts directory contains the module’s python files.  Anyone
reviewing this directory would benefit from having the [code reference](/project_summary/code_reference.md) on hand.
The bulk of the code exists within [retro_object.py](/project_scripts/retro_object.py), which creates a python
class capable of calling retrosheet's software.

### [Example Notebooks](/example_notebooks/)

The notebooks directory provides a test case for module usage.  As
outlined in the project’s synopsis, the test case examines strikeouts at
Fenway park from 2010 through 2020.  For the following reasons, the code
contained within this directory utilizes Jupyter Notebooks as an environment.

-  It is the tool of choice among data scientists and data enthusiasts.
Consequently, it seemed a logical choice for visualizing the data contained
within retrosheet’s event files.

-  Moreover, because it provides an interactive environment, it reduces the
growing pains associated with some of python’s most popular third-party
libraries, such as matplotlib and seaborn.


### [Project Exports](/project_exports/)

The exports directory contains the .csv files created by the example
notebooks.  

## Peripherals

### [Json Files](/json_files/)

The JSON directory contains four files:

-	bevent_fields.json
Stores the column information associated with bevent.exe.  Can be used to
create a python dictionary that populates a pandas DataFrame with appropriate
titles.  The key-value relationship is of the form int -> str, where int is a
number zero to ninety-six that returns a column title.

-	bgame_fileds.json
Stores the column information associated with bgame.exe.  Can be used to
create a python dictionary that populates a pandas DataFrame with appropriate
titles.  The key-value relationship is of the form int -> str, where int is a
number zero to eighty-four that returns a column title.

-	team_extensions.json
Stores team abbreviations for every major league baseball team.  Abbreviations
are used when calling bevent, bgame, and box from the command line.
Similarly, a RetroObject is instantiated when passed a valid team
abbreviation.  The key-value relationship is of the form str -> list\[list\],
where str is a team abbreviation that returns a team’s historical information.

-	bio_information.json
Contains player biographical data.  This data is stored in relation to a
retrosheet player id, an alphanumeric representation of a player’s name.   The
key-value relationship is of the form str -> dict, where str is a player id
that returns a dictionary of biographical information.

### [event_files](/event_files/)

Normally, the event_files folder would contain the following:

- [bevent.exe](https://www.retrosheet.org/resources/resources1.html);
- [bgame.exe](https://www.retrosheet.org/resources/resources1.html);
- [box.exe](https://www.retrosheet.org/resources/resources1.html);
- [Event files](https://www.retrosheet.org/game.htm) ending in .EVN or .EVA;
- [Roster files](https://www.retrosheet.org/game.htm) ending in .ROS;
- [Team files](https://www.retrosheet.org/game.htm) of the form TEAM2000, TEAM2001, ...

To avoid cluttering the repository, I have included links to these resources
rather than the resources themselves.  

## Requirements
I used python’s standard library for the majority of the project’s scripts.
The only deviation in the core [modules](/project_scripts/) is an import of numpy’s nan
attribute.  The example notebooks rely on two third-party libraries: pandas,
a popular data science library; and notebooks, Jupyter’s environment for
interactive computing.  For more information about the project’s development
environment, please reference [requirements.txt](/requirements.txt).

## Status

This is far from a finished project.  In the future, I hope to accomplish the
following:

-	Reduce the complexity of retro_object.py.  As it stands, this module is
approximately seven-hundred lines long, although it could be more terse,
expressive, and idiomatic.
-	Develop more robust use cases.
-	Incorporate more of retrosheet’s peripherals into the project.  As it is
currently composed, the project includes only what is necessary to parse the
event files for player statistics and biographical information.

Regardless of the project's current state, hopefully anyone reading this
repository can glean some inspiration from my efforts.

Thanks for reading! 
