from __future__ import print_function
import os
import MySQLdb

# configure db
hostname = "localhost"       
port = 3306
username = "root"
password = "111111"
dbname = "bdtune"           
tablename = "pidstat"

def read_file(filename):
    with open(filename, 'r') as rf:
        line_list = []
        for line in rf.readlines():
            line_list.append(line.split())
        return line_list
		
def insert2sql(line_list):
    node = line_list[0][2][1:-1]
    date = line_list[0][3]
    if line_list[0][-1][0:-1] == 'CPU':
        cpu_num = line_list[0][-2][1:]
    else:
        cpu_num = 0
    empty_line_num = []
    for i in range(1, len(line_list)):
        # using empty line to split lines into 3 partitions
        if line_list[i] == []:
            empty_line_num.append(i)
    partition_num = [empty_line_num[i:i+3] for i in range(0,len(empty_line_num),3)]
    num_4 = [empty_line_num[j*3] for j in range(len(empty_line_num)//3)]
    for i in range(len(partition_num)-1):
        partition_num[i].append(num_4[i+1])
    partition_num[-1].append(len(line_list))
	
	# connect mysql
    conn = MySQLdb.connect(host=hostname, port=port, user=username, passwd=password, db=dbname)
    cur = conn.cursor()
	
    for part in partition_num:
	
        # insert cpu info
        for i in range (part[0]+2, part[1]):           		
            time = line_list[i][0] + " " + line_list[i][1]
            pid = line_list[i][2] 
            usr = line_list[i][3]
            system = line_list[i][4]
            guest = line_list[i][5]
            cpu_usage = line_list[i][6]
            cpu_core = line_list[i][7]
            command = line_list[i][8]
			# judge whether the cpu existed
            if cpu_num != 0:
                sql = "insert into " + tablename + \
			    " (node, date, time, cpu_num, pid, usr, system, guest, cpu_usage, cpu_core, command) values('" \
                + node + "', '" + date + "', '" + time + "', '" + cpu_num + "', '" + pid + "', '" + usr + "', '" \
				+ system + "', '" + guest + "', '" + cpu_usage + "', '" + cpu_core + "', '" + command + "');"
            else:
                sql = "insert into " + tablename + \
			    " (node, date, time, pid, usr, system, guest, cpu_usage, cpu_core, command) values('" \
                + node + "', '" + date + "', '" + time + "', '" + pid + "', '" + usr + "', '" \
				+ system + "', '" + guest + "', '" + cpu_usage + "', '" + cpu_core + "', '" + command + "');"
            cur.execute(sql)
			
		# insert mem info
        for i in range (part[1]+2, part[2]):           		
            time = line_list[i][0] + " " + line_list[i][1]
            pid = line_list[i][2] 
            minflt = line_list[i][3]
            majflt = line_list[i][4]
            vsz = line_list[i][5]
            rss = line_list[i][6]
            mem_usage = line_list[i][7]
            command = line_list[i][8]
            if "select * from " + tablename + " where pid = '" + pid + "' and time = '" + time + \
			"' and node = '" + node + "';" is None:
                if cpu_num != 0:
                    sql = "insert into " + tablename + \
				    " (node, date, time, cpu_num, pid, minflt, majflt, vsz, rss, mem_usage, command) values('" \
                    + node + "', '" + date + "', '" + time + "', '" + cpu_num + "', '" + pid + "', '" + minflt + \
					"', '" + majflt + "', '" + vsz + "', '" + rss + "', '" + mem_usage + "', '" + command + "');"
                else:
                    sql = "insert into " + tablename + \
				    " (node, date, time, pid, minflt, majflt, vsz, rss, mem_usage, command) values('" \
                    + node + "', '" + date + "', '" + time + "', '" + pid + "', '" + minflt + \
					"', '" + majflt + "', '" + vsz + "', '" + rss + "', '" + mem_usage + "', '" + command + "');"
            else:
                sql = "update " + tablename + " set minflt='" + minflt + "', majflt='" + majflt + "', vsz='" \
				      + vsz + "', rss='" + rss + "', mem_usage='" + mem_usage + "' where (pid = '" + pid \
					  + "' and time = '" + time + "' and node = '" + node + "');"
            cur.execute(sql)
			
		# insert disk info
        for i in range (part[2]+2, part[3]):           		
            time = line_list[i][0] + " " + line_list[i][1]
            pid = line_list[i][2] 
            kb_rd = line_list[i][3]
            kb_wr = line_list[i][4]
            kb_ccwr = line_list[i][5]
            command = line_list[i][6]
            if "select * from " + tablename + " where pid = '" + pid + "' and time = '" + time + \
			"' and node = '" + node + "';" is None:
                if cpu_num != 0:
                    sql = "insert into " + tablename + \
				    " (node, date, time, cpu_num, pid, kb_rd, kb_wr, kb_ccwr, command) values('" \
                    + node + "', '" + date + "', '" + time + "', '" + cpu_num + "', '" + pid + "', '" + \
					kb_rd + "', '" + kb_wr + "', '" + kb_ccwr + "', '" + command + "');"
                else:
                    sql = "insert into " + tablename + \
				    " (node, date, time, pid, kb_rd, kb_wr, kb_ccwr, command) values('" \
                    + node + "', '" + date + "', '" + time + "', '" + pid + "', '" + \
					kb_rd + "', '" + kb_wr + "', '" + kb_ccwr + "', '" + command + "');"
            else:
                sql = "update " + tablename + " set kb_rd='" + kb_rd + "', kb_wr='" + kb_wr + "', kb_ccwr='" + \
				      kb_ccwr + "' where (pid = '" + pid + "' and time = '" + time + "' and node = '" + node + "');"
            cur.execute(sql)
			
    print("Insert Successfully !")
    cur.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.pidstat'):
            line_list = read_file(filename)
        print('file %s' % filename)
        insert2sql(line_list)
       
		