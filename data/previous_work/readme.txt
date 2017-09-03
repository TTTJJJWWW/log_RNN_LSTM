数据集在/home/renrui/logAnalysis/dataset目录下，包含两个数据集的原始文件。

   大致要完成的是：   将原始文件中的每一行event，根据message的文本相似度值，然后为每个event分配一个id。如果新来的event和已经分配的id的message类似，就使用已有的id，否则就重新生成一个新的id。【你也可以看看，有没有更精确的相似度方法】
  
  

   另外， 附件是之前喻明鹤写的代码。
   大概有几个数据库表和代码(相关代码也已经放在 /home/renrui/logAnalysis下了，不过我还没有做过整理)：

sim.py 相似算法定理
logsql.py 日志处理分析文件
simTEST.py 相似算法定理测试文件（可以独立运行）


logsql.py实现过程说明
前言：
logInfo 原始日志文件
dict    日志字典文件
extractLogInfo  提取原始日志文件的msg字段和日志字典做匹配

1.判断“记录上次执行最大记录编号”文件是否存在，避免每次从最小的编号开始执行。
2.连接数据库，读取logInfo表的最大记录，写入文件。
3.然后把logInfo表的每条记录和dict表的全部记录做相似度比较（余弦定理），大于阀值不记录到“日志字典”中，否则记录到“日志字典”中。
4.每条logInfo表的记录都要记录到extractLogInfo表中。

