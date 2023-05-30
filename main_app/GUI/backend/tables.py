DB_NAME = "production"
TABLES = {}

TABLES['Process'] = ("""
        CREATE TABLE Process (
        ProcessID int NOT NULL AUTO_INCREMENT,
        ProcessName varchar(20) NOT NULL,
        NumStations tinyint NOT NULL,
        ProcessDesc varchar(255) DEFAULT NULL,
        DateCreated date DEFAULT NULL,
        TimesCompleted smallint NOT NULL,
        GoalTime time(2) NOT NULL,
        AvgTime time(2) NOT NULL,
        PRIMARY KEY (ProcessID)
        )
        """)

TABLES['Product'] = ("""
        CREATE TABLE Product (
        ProductID int NOT NULL AUTO_INCREMENT,
        ProcessID int NOT NULL,
        Completed boolean NOT NULL DEFAULT False,
        Accepted boolean NOT NULL DEFAULT False,
        StartTime datetime NOT NULL,
        EndTime datetime,
        TotalTime time(2) NOT NULL,
        PRIMARY KEY (ProductID),
        FOREIGN KEY (ProcessID) REFERENCES Process(ProcessID)
        )
        """)


TABLES['ProductTime'] = ("""
        CREATE TABLE ProductTime (
        ProductID int NOT NULL,
        StationOne time(2) NOT NULL,
        StationTwo time(2) NOT NULL,
        StationThree time(2) NOT NULL,
        StationFour time(2) NOT NULL,
        StationFive time(2) NOT NULL,
        TotalTime time(2) NOT NULL,
        PRIMARY KEY (ProductID),
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
        )
        """)

TABLES['Stations'] = ("""
        CREATE TABLE Stations (
        StationID int NOT NULL AUTO_INCREMENT,
        ProcessID int NOT NULL,
        NumSteps smallint NOT NULL,
        EstimatedTime time(2) NOT NULL,
        DateCreated date NOT NULL,
        StationDesc varchar(255) NOT NULL,
        AverageTime time(2) NOT NULL,
        Active boolean NOT NULL DEFAULT FALSE,
        PRIMARY KEY (StationID),
        FOREIGN KEY (ProcessID) REFERENCES Process(ProcessID)
        )
        """)


TABLES['Steps'] = ("""
        CREATE TABLE Steps (
        StepID int NOT NULL AUTO_INCREMENT,
        StationID int NOT NULL,
        StepDesc varchar(255),
        PhotoLink varchar(255),
        InfoLink varchar(255),
        PRIMARY KEY (StepID),
        FOREIGN KEY (StationID) REFERENCES Stations(StationID)
        )
        """)

TABLES['StationHistory'] = ( """
        CREATE TABLE StationHistory (
        StatHistID int NOT NULL AUTO_INCREMENT,
        StationID int NOT NULL,
        ProductID int NOT NULL,
        Accepted boolean NOT NULL DEFAULT True,
        DateCompleted date NOT NULL,
        TimeTaken time(2) NOT NULL,
        PRIMARY KEY (StatHistID),
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
        FOREIGN KEY (StationID) REFERENCES Stations(StationID)
        )
        """)


