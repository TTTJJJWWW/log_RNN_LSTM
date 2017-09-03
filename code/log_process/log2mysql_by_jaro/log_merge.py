import MySQLdb
import jaro_distance as jd  

# configure db
hostname = "localhost"       
port = 3306
username = "root"
password = "111111"
dbname = "system_log"           
tablename = "log_info"         
tablename2 = "log_msg_merge"  
threshold = 0.8  

try:
	# preproessing log message into mysql
	conn = MySQLdb.connect(host=hostname, port=port, user=username, passwd=password, db=dbname)
	cur = conn.cursor()
	sql = "select id, message from " + tablename + ";"
	cur.execute(sql)
	res = cur.fetchall()
	# set id number for new messages
	merge_id_new = 1
	for r in res:
		log_id = r[0]
		log_msg = r[1]
		sql2 = "select * from " + tablename2 + ";"
		cur.execute(sql2)
		res2=cur.fetchall()
		# determine whether table log_msg_merge is empty
		if not res2:
			insert_sql_first = "insert into " + tablename2 + "(message, log_merge_id) values('" + \
				log_msg + "', '" + str(merge_id_new) + "');"
			cur.execute(insert_sql_first)
			conn.commit()
		else:
			# get the last record of message
			merge_id_max = res2[-1][0]
			for r2 in res2:
				merge_id = r2[0]
				merge_msg = r2[1]
				log_merge_id = r2[2]
				msg_sim = jd.jaro(log_msg, merge_msg)
				if msg_sim > threshold:
					insert_sql_merge = "insert into " + tablename2 + "(message, log_merge_id) values('" + \
						log_msg + "', '" + str(log_merge_id) + "');"
					cur.execute(insert_sql_merge)
					conn.commit()
					break
				elif merge_id == merge_id_max:
					merge_id_new += 1
					insert_msg_new = "insert into " + tablename2 + "(message, log_merge_id) values('" + \
						log_msg + "', '" + str(merge_id_new) + "');"
					cur.execute(insert_msg_new)
					conn.commit()				
					print "insert the %d-th new log message !" % (merge_id_new)
					break
				else:
					pass
	cur.close()
	conn.commit()
	conn.close()	
except:
	print "Error"
finally:
	print "Merge Successfully"

	
	



