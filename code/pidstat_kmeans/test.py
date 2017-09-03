import numpy as np
import input_data as ida
import k_means as km

if __name__=='__main__':
  stage_id = "spark_stage_app-20170614115515-0020_0"
  param_i = 'cpu_usage'
  #stage_id = sys.argv[1]
  #param = sys.argv[2]
  
  beg_time, end_time = ida.stage_timestamp(stage_id)
  date, beg_time = ida.timestamp2datetime(beg_time)
  date, end_time = ida.timestamp2datetime(end_time)
  
  # for test
  date = '06/14/2017'
  beg_time = '04:17:05 PM'
  end_time = '04:30:05 PM'
  
  # load data
  nodes, params = ida.param_mean(param_i, date, beg_time, end_time)
  for i in range(len(nodes)):
    pid_list, command_list, param_list = [], [], []
    index_0, index_1 = [], []
    print('node: ', nodes[i][0])
    for param in params[i]:
      if param[2] is not None:
        pid_list.append(param[0])
        command_list.append(param[1])
        param_list.append(param[2])
    dataset = np.vstack((param_list, param_list))
    dataset = np.transpose(dataset)
  
    # kmeans clustering
    k = 2
    dataset = np.mat(dataset)
    if len(dataset) > 0:	
      centroids, cluster_assment = km.kmeans(dataset, k)
      for index, value in enumerate(cluster_assment[:, 0]):
        if value == 0:	
          index_0.append(index)
        if value == 1:
          index_1.append(index)
      print('kmeans: ', param_i)
      if len(index_0) <= len(index_1):
        print('command: ', [command_list[j] for j in index_0])
        #print('pid: ', [pid_list[j] for j in index_0])
      else:
        print('command: ', [command_list[j] for j in index_1])
        #print('pid: ', [pid_list[j] for j in index_0])	
      print()		
  
      # 2d plot
      km.show_cluster(dataset, k, centroids, cluster_assment, nodes[i][0])
