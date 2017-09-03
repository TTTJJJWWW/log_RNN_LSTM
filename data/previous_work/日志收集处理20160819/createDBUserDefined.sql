CREATE DATABASE systemLog;
USE systemLog;
CREATE TABLE logInfo
(
        ID int unsigned not null auto_increment primary key,
        timestamp datetime NULL, 
        fromHostIP varchar(20),
        nodeID  varchar(30),
        syslogfacility  int NULL,
	syslogfacilityText  varchar(20),
        syslogseverity int NULL,
	syslogseverityText varchar(20),
	msg varchar(300),
        SystemID int NULL
);


CREATE TABLE dict
(
        ID int unsigned not null auto_increment primary key,
        msg varchar(300)
);


CREATE TABLE extractLogInfo
(
        ID int unsigned not null auto_increment primary key,
        msg varchar(300),
        logInfoID int ,
        dictID int 
      
);




