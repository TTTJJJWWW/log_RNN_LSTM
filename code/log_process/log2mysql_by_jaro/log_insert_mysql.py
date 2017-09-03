import re
import MySQLdb
import os
import time

# configure db
hostname = "localhost"       
port = 3306
username = "root"
password = "111111"
dbname = "system_log"           
tablename = "log_info"

# file processed flag       
flag = -1                    

# get current path
current_path = os.getcwd()  
file_path = current_path + "/messages(10.26-11.2)"

# determine whether file's existed
if os.path.exists(file_path):    
	flag = 1
	print file_path + " is existed"
else:
	flag = 0
	print file_path + " is not existed"
	
# insert log info into mysql
try:
	conn = MySQLdb.connect(host=hostname, port=port, user=username, passwd=password, db=dbname)
	cur = conn.cursor()
	if flag == 1:
		file_read = open('messages(10.26-11.2)', 'r')
		lines = file_read.readlines()
		for line in lines:
			time_regex = ur"[A-z]* \s?\d+ \d+\:\d+\:\d+"
			node_n_regex = ur" [c][A-z]*\-?\d?\d?\-?\d?\d?\.?[A-z]*"
			app_regex = ur"[a-z]+\[?\["
			pro_id_regex = ur"\d*\]"
			msg_regex = ur"[A-Z][A-z]*\:.+"
			time_stamp = re.findall(time_regex, line)
			node_name = re.findall(node_n_regex, line)
			application = re.findall(app_regex, line)
			process_id = re.findall(pro_id_regex, line)
			message = re.findall(msg_regex, line)
			if application and process_id and message:
				ts = time_stamp[0] + ' 2008'
				time_float = time.mktime(time.strptime(ts,"%b %d %H:%M:%S %Y"))
				node_n = node_name[0][1:]
				app = application[0][:-1]
				pro_id = int(process_id[0][:-1])
				msg = message[0][:-1]
				sql = "insert into " + tablename + "(time_stamp, node_name, application, process_id, message) values('" + str(time_float) \
					+ "', '" + node_n + "', '" + app + "', '" + str(pro_id) + "', '" + msg + "');"
				cur.execute(sql)
	else:
		pass
	cur.close()
	conn.commit()
	conn.close()		
	file_read.close()
except:
	print "Insert Error"
finally:
	print "Insert Successfully"



