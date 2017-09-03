#!/usr/bin/python
# @-_-@ coding=utf-8 @-_-@

import MySQLdb
import os
import string
import sys
import jaro_distance as jd    #自定义余弦定理算法模块

COMPARERATION = 0.85         #余弦定理阀值
FLAG=-1                     #是否记录上次执行最大编号的文件标记

HOSTNAME="localhost"       #数据库信息
PORT=3306
USERNAME="root"
PASSWORD="111111"
DBNAME="bdtune"           #数据库名称
TABLENAME1="logInfo"          #数据库中表的名称
TABLENAME2="dict"            #字典表
TABLENAME3="extractLogInfo"  #日志信息提取表

currentPath=os.getcwd()  #得到当前工作目录，即当前Python脚本工作的目录路径
print currentPath
doc=currentPath+"/num"

def insert_sql(func):
	if os.path.exists(doc):    #判断文件是否存在  文件记录上次执行最大编号
		FLAG=1
		print doc+" is exist"
		fp=open(doc,"rb+")
		num=fp.readline()
		print "doc num::"+num
	else:
		FLAG=0
		print doc+" is not exist"
		fp=open(doc,"wb")

	try:
		conn=MySQLdb.connect(host=HOSTNAME,user=USERNAME,passwd=PASSWORD,db=DBNAME,port=PORT)
		cur=conn.cursor()
		if FLAG==1:
			sql1="select * from "+ TABLENAME1+" where ID > %d " %(int(num))
		else:
			sql1="select * from "+ TABLENAME1+";"

		print "sql1::"+sql1
		cur.execute(sql1)
		results1=cur.fetchall()
		if not results1:
			print "Do not add new data of log "
			sys.exit(0)

		print "----------doc-------"
		print results1[-1][0]
		print "----------doc-------"
		fp.seek(0, 0)     #
		fp.write(str(results1[-1][0]))   #把本次执行的最大编号记录到文件中
		fp.close()
	  
		sql2="select * from "+TABLENAME2+";"

		for row1 in results1:
			ID1 = row1[0]
			msg1= row1[8]
			print "start-------------"

			print "-----row1-------"
			print "id1=%s,msg1=%s" %(ID1,msg1)
			print "------------"

			cur.execute(sql2)
			results2=cur.fetchall()
			if not results2:     #判断表是否为空
				insertSql1 = "INSERT INTO "+TABLENAME2 +"(msg)  VALUES(\""+msg1+"\");"

				print  "insertSql1::"+insertSql1
				cur.execute(insertSql1)
				conn.commit()

				insertSql3="insert into " + TABLENAME3 + "(msg,logInfoID,dictID) values(\""+ msg1  +"\" ,'"+ str(ID1) + "',' "+ str(1) +"');"  #编号默认为1
				cur.execute(insertSql3)
				conn.commit()
				print "insertSql3::"+insertSql3
			else:
				dictMax=int(results2[-1][0])
				print "!!!!!!!!!!!!!!!!!!!"
				print "dict  max  %d" % (int(results2[-1][0]))
				print "!!!!!!!!!!!!!!!!!!!"
				for row2 in results2:
					ID2 = row2[0]
					msg2 = row2[1]

					print "-----row2-------"
					print "id2=%s,msg2=%s" %(ID2,msg2)
					print "----------------"

					ration =func(msg1, msg2)  #余弦定理

					print "ration::"+str(ration)

					if ration > COMPARERATION:
						print  "---------big----------"
						break
					elif dictMax==ID2:  #是否是最后一个记录
						insertSql2 = "INSERT INTO "+TABLENAME2 +"(msg)  VALUES(\""+msg1+"\");"
						print  "insertSql2::"+insertSql2
						cur.execute(insertSql2)
						conn.commit()
						ID2=ID2+1

				insertSql3="insert into " + TABLENAME3 + "(msg,logInfoID,dictID) values(\""+ msg1  +"\" ,'"+ str(ID1) + "',' "+ str(ID2) +"');"
				cur.execute(insertSql3)
				conn.commit()
				print "insertSql3::"+insertSql3
				print "end-------------"
		cur.close()
		conn.close()
	except:
		print "error"
		
if __name__ == '__main__':
	insert_sql(jd.jaro)
