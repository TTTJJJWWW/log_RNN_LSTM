from __future__ import print_function
import sys
import time
import MySQLdb

# db params
hostname = "localhost"       
port = 3306
username = "root"
password = "111111"
dbname = "bdtune" 
table_stage = "stage"     
table_pidstat = "pidstat"

def stage_timestamp(stage_id):
  conn = MySQLdb.connect(host=hostname, port=port, user=username, passwd=password, db=dbname)
  cur = conn.cursor()
  sql = "select submission_time, completion_time from " + table_stage + \
        " where stage_id = '%s';" % (stage_id)
  cur.execute(sql)
  res = cur.fetchall()
  beg_time = int(round(res[0][0]/1000))
  end_time = int(round(res[0][1]/1000))
  return beg_time, end_time
  cur.close()
  conn.commit()
  conn.close()
  
def timestamp2datetime(time_stamp):
  time_array = time.localtime(time_stamp)
  datetime = time.strftime("%m/%d/%Y %H:%M:%S", time_array)
  daytime = datetime.split(' ')
  if daytime[1] >= '12:00:00':
    date = daytime[0]
    time_12 = str(int(daytime[1][:2])-12) + daytime[1][2:] + ' PM'
  else:
    date = daytime[0]
    time_12 = daytime[1] + ' AM'
  return date, time_12
  
def param_mean(param, date, beg_time, end_time):
  conn = MySQLdb.connect(host=hostname, port=port, user=username, passwd=password, db=dbname)
  cur = conn.cursor()
  sql = "select node from " + table_pidstat + " group by node"
  cur.execute(sql)
  res = cur.fetchall()
  param_list = []
  for node in res:
    if beg_time[-2:] == 'AM' and end_time[-2:] == 'PM':
      sql2 = "select pid, command, avg(" + param + ") from " + table_pidstat + \
             " where date = '" + date + "' and (time >= '" + beg_time + \
			 "' and time <= '12:59:59 AM') and (time >= '00:00:00 PM'"  + \
			 " and time <= '" + end_time + "') and node = '"+ node[0] + "' group by pid;"
    else:
        sql2 = "select pid, command, avg(" + param + ") from " + table_pidstat + \
               " where date = '" + date + "' and (time >= '" + beg_time + \
               "' and time <= '" + end_time + "') and node = '"+ node[0] + "' group by pid;"
    cur.execute(sql2)
    res2 = cur.fetchall()
    param_list.append(res2)
  return res, param_list
  cur.close()
  conn.commit()
  conn.close()
  
if __name__=='__main__':
  stage_id = "spark_stage_local-1495765939864_8"
  param = 'cpu_usage'
  #stage_id = sys.argv[1]
  #param = sys.argv[2]
  
  beg_time, end_time = stage_timestamp(stage_id)
  date, beg_time = timestamp2datetime(beg_time)
  date, end_time = timestamp2datetime(end_time)
  
  # for test
  date = '06/14/2017'
  beg_time = '04:17:05 PM'
  end_time = '04:30:05 PM'
  
  nodes, params = param_mean(param, date, beg_time, end_time)
  print(nodes)
  print(params)
  
  