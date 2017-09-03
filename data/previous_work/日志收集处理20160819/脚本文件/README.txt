sim.py 余弦定理文件
logsql.py 日志处理分析文件
simTEST.py 余弦定理测试文件（可以独立运行）

SERVICErsyslog.conf  服务端日志收集文件配置（运行前去掉SERVICE字段，放在/etc/目录下）

CLIENTErsyslog.conf  客户端日志收集文件配置 （运行前去掉CLIENT字段，放在/etc/目录下）

--------------------------------------------------

logsql.py实现过程说明
前言：
logInfo 原始日志文件
dict    日志字典文件
extractLogInfo  提取原始日志文件的msg字段和日志字典做匹配

1.判断“记录上次执行最大记录编号”文件是否存在，避免每次从最小的编号开始执行。
2.连接数据库，读取logInfo表的最大记录，写入文件。
3.然后把logInfo表的每条记录和dict表的全部记录做相似度比较（余弦定理），大于阀值不记录到“日志字典”中，否则记录到“日志字典”中。
4.每条logInfo表的记录都要记录到extractLogInfo表中。