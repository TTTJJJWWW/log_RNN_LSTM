1.��mysql�������ݣ�ֱ�ӽ�int (logid) ת�� string���� train �� test �ֱ�����Ӧ list �С�

2.ȷ�� train �в�ͬ logid ����Ŀ��������������Ϊ��ͬ������ feature_size������ӦΪ���ݿ��column��

3.���� char2id()��string תΪint������ id2char()��֮�෴��

4.class BatchGenerator()Ϊ���ݼ������ɺ��������У�BatchGenerator.next()�������Ի�ȡһ����stirng����ѵ����
  batch_size ��ÿ�������ַ�����num_unrollings ��ÿ�����ַ����ĳ��ȡ�
  BatchGenerator.next() ����һ��list��list�ĳ����� num_unrollings+1 ����ÿһ��Ԫ�ض���һ�� (batch_size * feature_size) ��array��
  һ�� feature_size ά����������һ���ַ�����one-hot encoding�ĸ�ʽ(��ֻ��һ��1���඼Ϊ0�Ķ��������ݱ�ʾ)�� 
  
5.characters()�����ȴ�one-hot encoding������֣�����id2char����ַ���

6.batches2string()������ѵ�����ɵ�����ת��Ϊ����չ�ֵ�һ�����ַ�����

7.random_distribution()��������һ��array�ܺ�Ϊ 1 ��ƽ���ֲ���

8.sample()������sample_distribution()�����ķ���ֵ���� prediction �ĸ��ʣ����ʴ��һ��άΪ1��������Ϊ 0�������� prediction �ĸ��ʻ��logid��

9.ѵ��ģ�ͷ�Ϊ���¼������֣�
  1) �������
	 num_nodes ������������LSTM Cell���Cell������LSTM Cell �������ţ���input, output, forget ���š�
  2) ����LSTM Cell
  3) ��������ӿ�
     һ�� batch ͬʱ���������� batch_size=1 ��Ҫѵ�����ַ���Ϊ abcdefg����ô train_inputs�� abcdef��train_label �� bcdefg��
  4) ѭ��ִ��LSTM Cell
  5) ����loss
      softmax_cross_entropy_with_logits �Ƚ� full connection ��� outputs �� rain_labels, �õ� loss��
  6) �����Ż�
     tf.train.exponential_decay ʵ�� learning_rate ��ָ����˥����Խ������ learning_rate ԽС�� 
	 optimizer �����ʹ�ñ�׼ Gradient Descent��
  7) ����Ԥ��
	 sample_input ��һ��one-hot��������ַ���������ʼ state��output��������ͬ��LSTM Cell���õ���һ��Ԥ����ַ�sample_prediction��

10.ѵ��
   ÿ��ι��ȥ���ַ������������� num_unrollings+1����Ӧǰ�� BatchGenerator.next() ��ȡ�õ����ַ������ȡ�
   mean_loss �������ܸ����� loss ֵ���������������
   ÿ summary_frequency ����������ʱ�����ƽ�� loss ֵ�� learning_rate��
   ÿ�� summary_frequency * 10 ����������ʱ�򣬳������һЩ���ֽ�� (4�䣬ÿ��80���ַ������ֽ��)��
   reset_sample_state ��֤��ʼ���� state �� output ����� 0��
   ÿ�δ����һ���ַ���Ϊ���룬�õ���һ��Ԥ���ַ���Ԥ����� prediction ��ͨ��ǰ��� sample()���� �����ɻ���һ��ȷ�����ַ�feed��
   Ȼ����һ�δ���ģ����Ϊ���롣 

11.�ɵ�������
   batch_size 
   num_unrollings (<batch_size) 
   num_nodes (��Ԫ������һ����batch_size��Ӧ)
   num_steps (ѵ��ѭ��������һ��Խ��Խ�ã��󲿷ֳ���10,000�Σ���������2000�Σ����ڻ������ò�����̫��ʱ)
   * ����ѵ������Ϻö����Խ��������ף�����ѵ��Ч������ϣ�����ģ�ͷ�����������

