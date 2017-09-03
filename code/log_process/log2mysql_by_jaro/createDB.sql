CREATE DATABASE system_log;
USE system_log;
CREATE TABLE log_info
(
	ID int unsigned not null auto_increment primary key,
	time_stamp float NULL, 
	node_name varchar(32),
	application varchar(32),
	process_id int NULL,
	message varchar(256)
);


CREATE TABLE log_msg_merge
(
	ID int unsigned not null auto_increment primary key,
	message varchar(256),
	log_merge_id int
);





