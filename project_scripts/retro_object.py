# Standard library imports.
from datetime import datetime
from math import nan
from os import chdir
from subprocess import run
from re import compile, findall, match

# Third party imports.
from numpy import datetime64

# Local imports.
from event_parser import defaultYearEnd, defaultYearStart
from project_directories import eventsDir, scriptDir
from project_variables import  beventFieldsDict, bgameFieldsDict, teamDict
 

class RetroObject:
    """
    The RetroObject class contains two types of functions:  
    formatting functions and emulation functions.  
    
    Formatting functions take user input and format valid 
    query strings, which are ultimately called by an emulation 
    function to query retrosheet's event files. Emulation functions 
    call Retrosheet's executables as child processes of the 
    program, returning application output as python objects.  
    
    Formatting functions begin with double underscores, since 
    they are not meant to be called by end users.  The emulation 
    functions bevent and bgame return a list of lists, and box 
    returns a string, inclusive of whitespace, tabs, and newline 
    characters.  
    """
    
    # Class attributes.

    defaultColsBevent = tuple(
        key for key, value in beventFieldsDict.items() 
        if findall(r'\*', value)
        )
    defaultColsBgame = tuple(key for key in bgameFieldsDict.keys())
    validTeams = tuple(key for key in teamDict.keys())
    maxCols = {'bevent': 84,'bgame': 96}

    # Class Methods.

    def __init__(self, retroString):
        self.retroString = retroString.upper()
        if self.retroString not in self.validTeams:
            raise ValueError(
                f'team must be a three character string'
                f'corresponding to a valid retrosheet team id.' 
                f'\nReference the following valid strings.\n'
                f'{self.validTeams}'
                )
        else:
            self.entry = teamDict[self.retroString]
        if len(self.entry) == 1:
            self.lowerBound = self.entry[0][0]
            self.upperBound = self.entry[0][1]
            self.league = self.entry[0][2]
            self.fullName = self.entry[0][3]
            self.fileExtension = self.entry[0][4]
        elif len(self.entry) == 2:
            self.lowerBoundOne = self.entry[0][0]
            self.upperBoundOne = self.entry[0][1]
            self.leagueOne = self.entry[0][2]
            self.fullNameOne = self.entry[0][3]
            self.fileExtensionOne = self.entry[0][4]

            self.lowerBoundTwo = self.entry[1][0]
            self.upperBoundTwo = self.entry[1][1]
            self.leagueTwo = self.entry[1][2]
            self.fullNameTwo = self.entry[1][3]
            self.fileExtensionTwo = self.entry[1][4]

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
        
        chdir(eventsDir)
        self.yearStart = yearStart
        self.yearEnd = yearEnd
        self.columns = columns
        self.start = start
        self.end = end
        self.id = id
        if ((self.id is not None) and 
            (self.start is not None or self.end is not None)): 
            print(
                f'id and start / end parameters are mutually exclusive.'  
                f'Precedence given to game id.'
                )

        self.dateRange = [
            year for year in 
            range(int(yearStart), int(yearEnd) + 1, 1)
            ]
        self.output = str()
        self.columnValidation = self.__columnPipe(
            columns=self.columns, 
            desiredFunction='bevent'
            )

        for season in self.dateRange:
            self.query_string = (
                ['bevent'] 
              + self.__createDateString(
                    year = season, start = self.start, 
                    end = self.end, id = self.id
                    )
              + self.columnValidation[0] 
              + [
                f'{season}{self.retroString}'
                f'{self.__produceFileExtension(year=season)}'
                ]
                )
            self.output += run(
                self.query_string, shell = False, 
                capture_output = True, encoding = 'UTF-8'
                ).stdout

        self.output = self.output.split(sep='\n')
        self.output = self.output[:-1]
        self.output = [
            entry.replace('"','')
            .replace('(none)','')
            .split(sep=',') 
            for entry in self.output
            ]

        for index, entry in enumerate(self.output):
            self.output[index] = [self.__convertToInt(value) 
                for value in entry
                ]

        chdir(scriptDir)
        return self.output

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

        chdir(eventsDir)
        self.yearStart = yearStart
        self.yearEnd = yearEnd
        self.columns = columns
        self.start = start
        self.end = end
        self.id = id 
        if ((self.id is not None) and 
            (self.start is not None or self.end is not None)): 
            print(
                f'id and start / end parameters are mutually exclusive.'  
                f'Precedence given to game id.'
                )

        self.dateRange = [
            year for year in 
            range(int(self.yearStart), int(self.yearEnd) + 1,1)
            ]
        self.output = str()
        self.columnValidation = self.__columnPipe(
            columns = self.columns, 
            desiredFunction = 'bgame'
            )

        for season in self.dateRange:
            self.query_string = (
                ['bgame'] 
              + self.__createDateString(
                    year = season, start = self.start, 
                    end = self.end, id = self.id
                    )
              + self.columnValidation[0] 
              + [
                f'{season}{self.retroString}'
                f'{self.__produceFileExtension(year=season)}'
                ]
                )
            self.output += run(
                self.query_string, shell = False, 
                capture_output = True, encoding = 'UTF-8'
                ).stdout

        self.output = self.output.split(sep='\n')
        self.output = self.output[:-1]
        self.output = [
            entry.replace('"','')
            .replace('(none)','')
            .split(sep=',') 
            for entry in self.output
            ]

        for index, entry in enumerate(self.output):
            self.output[index] = self.__typeConversions(
                retro_output = entry, 
                columns=self.columnValidation[1]
                )

        chdir(scriptDir)
        return self.output

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
        
        chdir(eventsDir)
        self.yearStart = yearStart
        self.yearEnd = yearEnd
        self.start = start
        self.end = end
        self.id = id
        self.dateRange = [
            year for year in 
            range(int(yearStart), int(yearEnd) + 1, 1)
            ]
        self.output = str()

        for season in self.dateRange:
            self.query_string = (
                ['box'] 
              + self.__createDateString(
                    year = season, start = self.start, 
                    end = self.end, id = self.id) 
              + [
                f'{season}{self.retroString}'
                f'{self.__produceFileExtension(year=season)}'
                ]
                )
            self.output += run(
                self.query_string, shell = False, 
                capture_output = True, encoding = 'UTF-8'
                ).stdout 

        chdir(scriptDir)
        return self.output

    def __columnPipe(
            self, 
            columns = defaultColsBgame, 
            desiredFunction = 'bgame') -> list:
        """
        __columnPipe returns the column information bevent and bgame 
        require to execute successfully.  If the desired function is 
        set to bgame, then three objects are returned - a column 
        string, a sorted column list, and the difference between 
        the indexes for columns four and one, if applicable.  If 
        the desired function is set to bevent, then only the column 
        string and column list are returned.
        """

        self.desiredFunction = desiredFunction
        self.maxColumns = self.maxCols[self.desiredFunction]
        
        if not columns:
            raise ValueError('Column input cannot be NoneType.')
        elif '__iter__' in dir(type(columns)):
            self.columns = list({
                abs(value) if type(value) == int 
                else abs(int(value)) 
                for value in columns}
                )
        else:
            self.columns = list({
                abs(value) if type(value) == int 
                else abs(int(value)) 
                for value in [columns]}
                )
        
        if max(self.columns) > self.maxColumns:
            raise ValueError(
                f'Fields run zero through {self.maxColumns}.'  
                f'{self.columns} selected.'
                )

        if self.desiredFunction == 'bgame':
            self.columns.sort()
            self.columns, self.difference = (
                self.__linkDateColumns(self.columns) 
                )        
            self.columnString = self.__createColumnString(
                columns = self.columns)
            return (
                self.columnString,
                self.columns,
                self.difference,
                )
        else:
            self.columns.sort()
            self.columnString = self.__createColumnString(
                columns = self.columns)
            return (
                self.columnString,
                self.columns,
                )
        
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
        
        self.component = component
        if self.component is not None:
            try:
                if type(self.component) != datetime:
                    self.component = int(self.component)
            except:
                raise TypeError(
                    f'{self.component} is invalid. '  
                    f'Object must be of type datetime or convertible to int.'
                    )
        return self.component

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

        self.yearComponent = self.__convertDatetimeComponents(yearComponent)
        self.startComponent = self.__convertDatetimeComponents(startComponent)
        self.endComponent = self.__convertDatetimeComponents(endComponent)

        if type(self.yearComponent) == datetime:
            self.yearComponent = self.yearComponent.year

        if (type(self.startComponent) != datetime and 
                self.startComponent is not None):

            self.startComponent = datetime.strptime(
                str(self.yearComponent) + str(self.startComponent), 
                '%Y%m%d'
                )

        if (type(self.endComponent) != datetime and 
                self.endComponent is not None):

            self.endComponent = datetime.strptime(
                str(self.yearComponent) + str(self.endComponent), 
                '%Y%m%d'
                )

        if self.yearComponent not in range(1876, defaultYearEnd +1): 
                raise ValueError(
                    f'No major league games played before 1876.'  
                    f'{self.yearComponent} entered.'
                    )

        return (
            self.yearComponent,
            self.startComponent,
            self.endComponent,
            )

    def __convertToInt(self, target):
        """
        This function attempts to convert a target object to an int.  
        If this is successful, then the new int object is returned.  
        If the target object is None, then the nan type from python's 
        math module is returned.  Finally, if the target object cannot 
        be converted to an integer and is not None, then the unaltered 
        target object is returned.
        """

        self.target = target
        try:
            return int(self.target)
        except:
            if target == '':
                return nan
            else:
                return target

    def __createColumnString(self, columns) -> list:
        """
        __createColumnString creates a valid column string that bevent
        and bgame can use to query event files.  It is called 
        by  "__columnPipe,' which provides the column information 
        bevent and bgame need to query event files.
        """

        self.columns = columns
        self.columns.sort(reverse=False)
        self.minValue = self.columns[0]
        self.columnString = str()

        for index, value in enumerate(self.columns):
            try:
                nextValue = self.columns[index + 1]
            except:
                self.columnString += (
                    f'{self.minValue}-{value}' 
                    if self.minValue != value 
                    else f'{value}'
                    )
                return [
                    '-f',
                    self.columnString,
                    ]

            if nextValue - value != 1:
                self.columnString += (
                    f'{self.minValue}-{value},' 
                    if self.minValue != value 
                    else f'{value},'
                    )
                self.minValue = nextValue

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

        self.year,self.start,self.end = (
            self.__convertToDatetime(
            year, start, end)
            )
        self.id = id
        if self.id is None:
            if self.start is None and self.end is None:
                return [
                    '-y',
                    str(self.year),
                    ]
            elif self.start is not None and self.end is None:
                return [
                    '-y',
                    str(self.year),
                    '-s',
                    self.__leadingZeros(self.start.month).join(
                        ['',self.__leadingZeros(self.start.day)])
                    ]
            elif self.start is None and self.end is not None:
                return [
                    '-y',
                    str(self.year),
                    '-e',
                    self.__leadingZeros(self.end.month).join(
                        ['',self.__leadingZeros(self.end.day)])
                    ]
            elif self.start is not None and self.end is not None:
                if self.start > self.end: 
                    raise ValueError('Start date is greater than end date.')
                
                return [
                    '-y',
                    str(self.year),
                    '-s',
                    self.__leadingZeros(self.start.month).join(
                        ['',self.__leadingZeros(self.start.day)]),
                    '-e',
                    self.__leadingZeros(self.end.month).join(
                        ['',self.__leadingZeros(self.end.day)])
                    ]
        else:
            self.season,self.validatedId = self.__evalGameId(self.id)
            return [
                '-y',
                str(self.season),
                '-i',
                self.validatedId,
                ]
    
    def __evalGameId(self, id):
        """
        This function uses the compile and match methods 
        from the regular expressions library to raise 
        value errors for any game id that is not properly 
        formatted.  It is called by __createDateString 
        when an argument is passed to the id parameter.
        """

        self.id = id
        self.idPattern = compile(r'[A-Z,1-9]{3}\d{9}')

        if not match(self.idPattern, self.id): 
            raise ValueError('Id string is not properly formatted.')

        elif self.id[:3] not in teamDict.keys(): 
            raise ValueError(
                f'First three id characters do not correspond' 
                f'to a valid retroString id.'
                )

        else:
            self.validatedId = match(self.idPattern, self.id).group(0)
            self.season = self.validatedId[3:7]
            self.game_type = self.validatedId[11]

            if int(self.season) not in range(1876, defaultYearEnd + 1): 
                raise ValueError(
                    f'No major league games played before 1876.'  
                    f'{self.season} entered.'
                    )
            elif int(self.game_type) not in [0, 1, 2]: 
                raise ValueError(
                    f'The final id character must be a zero, one, or two.'  
                    f'{self.game_type} entered.'
                    )
            else:
                return (
                    self.season,
                    self.validatedId,
                    )

    def __leadingZeros(self, dateComponent: int) -> str:
        """
        __leadingZeros formats month and day components
        for _createDateString.  If a month or date 
        component is less than then, then a leading 
        zero is inserted before the component.
        """
        self.dateComponent = dateComponent
        if dateComponent < 10:
            return f'{str(0) + str(dateComponent)}'
        else:
            return f'{dateComponent}'
    
    def __linkDateColumns(self, columns) -> tuple:
        """
        This function, which is called by __columnPipe if the 
        parameter 'desiredFunction' is set to 'bgame,' ensures 
        that column one is present in the column list when four 
        is selected without it.  It returns the new sorted column 
        list, in addition to the difference between the indexes 
        for columns four and one.
        """

        self.columns = columns
        if 4 in self.columns and 1 not in self.columns:
            self.columns.append(1) 

        self.columns.sort(reverse=False)
        try:
            self.positions = [
                index for index, value in enumerate(self.columns) 
                if value in [1, 4]
                ]
            self.difference = self.positions[1] - self.positions[0]    
        except:
            self.difference = None
            
        return (
            self.columns,
            self.difference,
            )

    def __mergeDateTime(self, date, time):
        """
        __mergeDateTime converts bgame's time output to a valid 
        datetime object.
        """

        self.date = str(date)
        self.time = time

        if len(self.time) == 3:
            self.dateTime = self.date + str(int(self.time) + 1200)
        elif len(self.time) == 4:
            self.dateTime =  self.date + self.time
        elif self.time == str(0):
            self.dateTime = self.date + '0100'
            
        self.dateTime = datetime.strptime(self.dateTime, '%Y%m%d%H%M')
        return self.dateTime
        
    def __produceFileExtension(self, year) -> str:
        """
        __produceFileExtension returns the valid file extension for
         a RetroObject, and is called by bevent, bgame, and box.  
         If a team did not play during any given calendar year, the
        function raises a value error.
        """

        self.year = year
        try:
            if self.year in range(self.lowerBound, self.upperBound + 1, 1): 
                return self.fileExtension
            else:
                raise ValueError(
                    f'{self.retroString} did not play' 
                    f'during the {self.year} season'
                    )    
        except:
            if self.year in range(
                    self.lowerBoundOne, self.upperBoundOne + 1, 1): 
                return self.fileExtensionOne
            elif self.year in range(
                    self.lowerBoundTwo, self.upperBoundTwo + 1, 1): 
                return self.fileExtensionTwo
            else:
                raise ValueError(
                    f'{self.retroString} did not play' 
                    f'during the {self.year} season.'
                    )

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

        self.retro_output = retro_output
        self.columns = columns
        self.type_mapping = {
            index: column 
            for index, column in enumerate(self.columns)
            }

        for index_one, entry in enumerate(self.retro_output):
            if (self.type_mapping[index_one] == 1 and
                    self.desiredFunction == 'bgame'):

                self.retro_output[index_one] = datetime.strptime(
                    entry, '%y%m%d').date()

            elif (self.type_mapping[index_one] == 4 and
                    self.desiredFunction == 'bgame'):

                self.column_one = datetime.strftime(
                    self.retro_output[index_one - self.difference],
                    '%Y%m%d'
                    )

                self.retro_output[index_one] = datetime64(
                    self.__mergeDateTime(date=self.column_one, time=entry)
                    )

            elif (self.type_mapping[index_one] == 22 and 
                    self.desiredFunction == 'bgame'):
                try:
                    self.retro_output[index_one] = datetime64(
                        datetime.strptime(entry, '%Y/%m/%d %H:%M:%S')
                        )
                except:
                    self.retro_output[index_one] = datetime64(entry)

            else:
                self.retro_output[index_one] = self.__convertToInt(entry)

        return self.retro_output
