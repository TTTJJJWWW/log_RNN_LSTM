USE bdtune;
CREATE TABLE pidstat
(
	id int unsigned not null auto_increment primary key,
	node varchar(16),
	date varchar(16),
	time varchar(16),
	cpu_num int NULL,
	pid int NULL,
	command varchar(32),
	usr float NULL,
	system float NULL,
	guest float NULL,
	cpu_usage float NULL,
	cpu_core int NULL,
	minflt float NULL,
	majflt float NULL,
	vsz int NULL,
	rss int NULL,
	mem_usage float NULL,
	kb_rd float NULL,
	kb_wr float NULL,
	kb_ccwr float NULL
);









