1.从mysql读入数据：直接将int (logid) 转成 string，按 train 和 test 分别放入对应 list 中。

2.确定 train 中不同 logid 的数目，并将其排序作为不同的特征 feature_size，即对应为数据库的column。

3.函数 char2id()将string 转为int，函数 id2char()与之相反。

4.class BatchGenerator()为数据集批生成函数，其中，BatchGenerator.next()方法可以获取一批子stirng用于训练。
  batch_size 是每批几个字符串，num_unrollings 是每个子字符串的长度。
  BatchGenerator.next() 返回一个list，list的长度是 num_unrollings+1 ，其每一个元素都是一个 (batch_size * feature_size) 的array，
  一个 feature_size 维的向量代表一个字符，是one-hot encoding的格式(即只有一个1其余都为0的二进制数据表示)。 
  
5.characters()函数先从one-hot encoding变回数字，再用id2char变成字符。

6.batches2string()函数则将训练生成的数据转变为可以展现的一连的字符串。

7.random_distribution()函数生成一个array总和为 1 的平均分布。

8.sample()函数以sample_distribution()函数的返回值传入 prediction 的概率，概率大的一个维为1，其他都为 0，即按照 prediction 的概率获得logid。

9.训练模型分为以下几个部分：
  1) 定义变量
	 num_nodes 代表神经网络中LSTM Cell层的Cell个数。LSTM Cell 有三个门，即input, output, forget 三门。
  2) 定义LSTM Cell
  3) 定义输入接口
     一个 batch 同时批处理。假设 batch_size=1 ，要训练的字符串为 abcdefg，那么 train_inputs是 abcdef，train_label 是 bcdefg。
  4) 循环执行LSTM Cell
  5) 定义loss
      softmax_cross_entropy_with_logits 比较 full connection 层的 outputs 和 rain_labels, 得到 loss。
  6) 定义优化
     tf.train.exponential_decay 实现 learning_rate 的指数型衰减，越到后面 learning_rate 越小。 
	 optimizer 定义成使用标准 Gradient Descent。
  7) 定义预测
	 sample_input 是一个one-hot编码过的字符，建立初始 state和output，经过相同的LSTM Cell，得到下一个预测的字符sample_prediction。

10.训练
   每次喂进去的字符串长度正好是 num_unrollings+1，对应前面 BatchGenerator.next() 获取得到的字符串长度。
   mean_loss 用来加总各步的 loss 值，用来后面输出。
   每 summary_frequency 整数倍步的时候，输出平均 loss 值和 learning_rate。
   每当 summary_frequency * 10 整数倍步的时候，尝试输出一些文字结果 (4句，每句80个字符的文字结果)。
   reset_sample_state 保证初始化的 state 和 output 都设成 0。
   每次传入第一个字符作为输入，得到第一个预测字符的预测概率 prediction ，通过前面的 sample()函数 将其蜕化成一个确定的字符feed，
   然后下一次传给模型作为输入。 

11.可调整参数
   batch_size 
   num_unrollings (<batch_size) 
   num_nodes (神经元个数，一般与batch_size对应)
   num_steps (训练循环次数，一般越大越好，大部分超过10,000次，代码里是2000次，由于机器配置不够，太耗时)
   * 经常训练结果较好而测试结果差得离谱，由于训练效果过拟合，导致模型泛化能力弱。

