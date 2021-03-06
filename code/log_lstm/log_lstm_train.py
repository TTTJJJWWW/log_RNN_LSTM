from __future__ import print_function
import os
import numpy as np
import random
import string
import tensorflow as tf 
import zipfile
from six.moves import range
from six.moves.urllib.request import urlretrieve
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import log_data
import data2file as d2f

def char2id(char):
	if char in letter_sort:
		return letter_sort.index(char) - first_letter + 1
	else:
		print('Unexpected character: %s' % char)
		return 0
		
def id2char(dictid):
	if dictid > 0:
		return letter_sort[dictid + first_letter - 1]
	else:
		return '0'

def char_id(char):
	if char in string.digits:
		return ord(char) - first_letter + 1
	elif char == ' ':
		return 0
	else:
		print('Unexpected character: %s' % char)
		return 0
  
def id_char(dictid):
	if dictid > 0:
		return chr(dictid + first_letter - 1)
	else:
		return ' '

class BatchGenerator(object):
	def __init__(self, text, batch_size, num_unrollings):
		self._text = text
		self._text_size = len(text)
		self._batch_size = batch_size
		self._num_unrollings = num_unrollings
		segment = self._text_size // batch_size
		self._cursor = [ offset * segment for offset in range(batch_size)]
		self._last_batch = self._next_batch()
  
	def _next_batch(self):
		"""Generate a single batch from the current cursor position in the data."""
		batch = np.zeros(shape=(self._batch_size, vocabulary_size), dtype=np.float)
		for b in range(self._batch_size):
			batch[b, char2id(self._text[self._cursor[b]])] = 1.0
			self._cursor[b] = (self._cursor[b] + 1) % self._text_size
		return batch
	  
	def next(self):
		"""Generate the next array of batches from the data. The array consists of
		the last batch of the previous array, followed by num_unrollings new ones."""
		batches = [self._last_batch]
		for step in range(self._num_unrollings):
			batches.append(self._next_batch())
		self._last_batch = batches[-1]
		return batches

def characters(probabilities):
	"""Turn a 1-hot encoding or a probability distribution over the possible
	characters back into its (most likely) character representation."""
	return [id2char(c) for c in np.argmax(probabilities, 1)]

def batches2string(batches):
	"""Convert a sequence of batches back into their (most likely) string
	representation."""
	s = [''] * batches[0].shape[0]
	for b in batches:
		s = [''.join(x) for x in zip(s, characters(b))]
	return s

def logprob(predictions, labels):
	"""Log-probability of the true labels in a predicted batch."""
	predictions[predictions < 1e-10] = 1e-10
	return np.sum(np.multiply(labels, -np.log(predictions))) / labels.shape[0]

def sample_distribution(distribution):
	"""Sample one element from a distribution assumed to be an array of normalized
	probabilities."""
	r = random.uniform(0, 1)
	s = 0
	for i in range(len(distribution)):
		s += distribution[i]
		if s >= r:
			return i
	return len(distribution) - 1

def sample(prediction):
	"""Turn a (column) prediction into 1-hot encoded samples."""
	p = np.zeros(shape=[1, vocabulary_size], dtype=np.float)
	p[0, sample_distribution(prediction[0])] = 1.0
	return p

def random_distribution():
	"""Generate a random column of probabilities."""
	b = np.random.uniform(0.0, 1.0, size=[1, vocabulary_size])
	return b/np.sum(b, 1)[:,None]

if __name__=='__main__':
	# load data
	datatrain, datatest, datatrain_str, datatest_str = log_data.load_data()
	#text = ' '.join(datatrain_str)
	#test_data = ' '.join(datatest_str)
	train_text = datatrain_str
	train_size = len(train_text)
	valid_text = datatest_str
	valid_size = len(valid_text)
	
	print('Data size %d' % (len(train_text)+len(valid_text)))
	print('Size and sample of train data: %s, %s' % (train_size, train_text[:64]))
	print('Size and sample of valid data: %s, %s' % (valid_size, valid_text[:64]))

	letter_sort = sorted(set(train_text))
	vocabulary_size = len(letter_sort) + 1 # [logid] + ' '
	first_letter = letter_sort.index(letter_sort[0])
	
	'''
	print(char2id('0'), char2id('9'), char2id(' '), char2id('a'))
	print(id2char(1), id2char(10), id2char(0))
	'''

	batch_size=64
	num_unrollings=10
	
	train_batches = BatchGenerator(train_text, batch_size, num_unrollings)
	valid_batches = BatchGenerator(valid_text, 1, 1)

	'''
	print(batches2string(train_batches.next()))
	print(batches2string(train_batches.next()))
	print(batches2string(valid_batches.next()))
	print(batches2string(valid_batches.next()))
	'''
	
	num_nodes = 64
	graph = tf.Graph()
	with graph.as_default():
		# Parameters:
		# Input gate: input, previous output, and bias.
		ix = tf.Variable(tf.truncated_normal([vocabulary_size, num_nodes], -0.1, 0.1))
		im = tf.Variable(tf.truncated_normal([num_nodes, num_nodes], -0.1, 0.1))
		ib = tf.Variable(tf.zeros([1, num_nodes]))
		# Forget gate: input, previous output, and bias.
		fx = tf.Variable(tf.truncated_normal([vocabulary_size, num_nodes], -0.1, 0.1))
		fm = tf.Variable(tf.truncated_normal([num_nodes, num_nodes], -0.1, 0.1))
		fb = tf.Variable(tf.zeros([1, num_nodes]))
		# Memory cell: input, state and bias.                             
		cx = tf.Variable(tf.truncated_normal([vocabulary_size, num_nodes], -0.1, 0.1))
		cm = tf.Variable(tf.truncated_normal([num_nodes, num_nodes], -0.1, 0.1))
		cb = tf.Variable(tf.zeros([1, num_nodes]))
		# Output gate: input, previous output, and bias.
		ox = tf.Variable(tf.truncated_normal([vocabulary_size, num_nodes], -0.1, 0.1))
		om = tf.Variable(tf.truncated_normal([num_nodes, num_nodes], -0.1, 0.1))
		ob = tf.Variable(tf.zeros([1, num_nodes]))
		# Variables saving state across unrollings.
		saved_output = tf.Variable(tf.zeros([batch_size, num_nodes]), trainable=False)
		saved_state = tf.Variable(tf.zeros([batch_size, num_nodes]), trainable=False)
		# Classifier weights and biases.
		w = tf.Variable(tf.truncated_normal([num_nodes, vocabulary_size], -0.1, 0.1))
		b = tf.Variable(tf.zeros([vocabulary_size]))

		# Definition of the cell computation.
		def lstm_cell(i, o, state):
			"""Note that in this formulation, we omit the various connections between the
			previous state and the gates."""
			input_gate = tf.sigmoid(tf.matmul(i, ix) + tf.matmul(o, im) + ib)
			forget_gate = tf.sigmoid(tf.matmul(i, fx) + tf.matmul(o, fm) + fb)
			update = tf.matmul(i, cx) + tf.matmul(o, cm) + cb
			state = forget_gate * state + input_gate * tf.tanh(update)
			output_gate = tf.sigmoid(tf.matmul(i, ox) + tf.matmul(o, om) + ob)
			return output_gate * tf.tanh(state), state

		# Input data.
		train_data = list()
		for _ in range(num_unrollings + 1):
			train_data.append(tf.placeholder(tf.float32, shape=[batch_size,vocabulary_size]))
		train_inputs = train_data[:num_unrollings]
		train_labels = train_data[1:]  # labels are inputs shifted by one time step.

		# Unrolled LSTM loop.
		outputs = list()
		output = saved_output
		state = saved_state
		for i in train_inputs:
			output, state = lstm_cell(i, output, state)
			outputs.append(output)

		# State saving across unrollings.
		with tf.control_dependencies([saved_output.assign(output),saved_state.assign(state)]):
			# Classifier.
			logits = tf.nn.xw_plus_b(tf.concat(outputs, 0), w, b)
			loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=tf.concat(train_labels, 0), logits=logits))

		# Optimizer.
		global_step = tf.Variable(initial_value=0,
                          name='global_step', trainable=False)
		learning_rate = tf.train.exponential_decay(10.0, global_step, 5000, 0.1, staircase=True)
		optimizer = tf.train.GradientDescentOptimizer(learning_rate)
		gradients, v = zip(*optimizer.compute_gradients(loss))
		gradients, _ = tf.clip_by_global_norm(gradients, 1.25)
		optimizer = optimizer.apply_gradients(zip(gradients, v), global_step=global_step)

		# Predictions.
		train_prediction = tf.nn.softmax(logits)

		# Sampling and validation eval: batch 1, no unrolling.
		sample_input = tf.placeholder(tf.float32, shape=[1, vocabulary_size])
		saved_sample_output = tf.Variable(tf.zeros([1, num_nodes]))
		saved_sample_state = tf.Variable(tf.zeros([1, num_nodes]))
		reset_sample_state = tf.group(saved_sample_output.assign(tf.zeros([1, num_nodes])),saved_sample_state.assign(tf.zeros([1, num_nodes])))
		sample_output, sample_state = lstm_cell(sample_input, saved_sample_output, saved_sample_state)
		with tf.control_dependencies([saved_sample_output.assign(sample_output),saved_sample_state.assign(sample_state)]):
			sample_prediction = tf.nn.softmax(tf.nn.xw_plus_b(sample_output, w, b))
	
		# save variables
		saver = tf.train.Saver()
	
	# save trained network 
	save_dir = 'checkpoints/'
	if not os.path.exists(save_dir):
		os.makedirs(save_dir)
	save_path = save_dir + 'log_lstm'
			
	num_steps = 2001
	summary_frequency = 100

	with tf.Session(graph=graph) as session:
		tf.global_variables_initializer().run()
		print('Initialized')
		mean_loss = 0
		for step in range(num_steps):
			batches = train_batches.next()
			feed_dict = dict()
			for i in range(num_unrollings + 1):
				feed_dict[train_data[i]] = batches[i]
			_, l, predictions, lr = session.run([optimizer, loss, train_prediction, learning_rate], feed_dict=feed_dict)
			mean_loss += l
			
			if step % summary_frequency == 0:
				if step > 0:
					mean_loss = mean_loss / summary_frequency
				# The mean loss is an estimate of the loss over the last few batches.
				print('Average loss at step %d: %f learning rate: %f' % (step, mean_loss, lr))
				mean_loss = 0
				labels = np.concatenate(list(batches)[1:])
				print('Minibatch perplexity: %.2f' % float(np.exp(logprob(predictions, labels))))
				
				if step % (summary_frequency * 10) == 0:
					# Generate some samples.
					print('=' * 80)
					for _ in range(4):
						feed = sample(random_distribution())
						sentence = characters(feed)[0]
						reset_sample_state.run()
						sentence_list = [sentence]
						for _ in range(80):
							prediction = sample_prediction.eval({sample_input: feed})
							feed = sample(prediction)
							sentence_list.append(characters(feed)[0])
							
						print(sentence_list)
					print('=' * 80)
				# Measure validation set perplexity.
				reset_sample_state.run()
				valid_logprob = 0
				for _ in range(valid_size):
					b = valid_batches.next()
					predictions = sample_prediction.eval({sample_input: b[0]})
					valid_logprob = valid_logprob + logprob(predictions, b[1])
				print('Validation set perplexity: %.2f' % float(np.exp(valid_logprob / valid_size)))
				
				if (step % 2000 == 0) and (step > 0):
					'''
					# Generate train data.
					sentence_predict = train_text[0]
					reset_sample_state.run()
					sentence_pre_list = [sentence_predict]
					# predict 1 to 1
					for _ in range(train_size):
						b = train_batches.next()
						predictions = sample_prediction.eval({sample_input: b[0][0].reshape((1,-1))})
						feed = sample(predictions)
						sentence_pre_list.append(characters(feed)[0])
					print('The result sample after %sth training: %s' % (str(train_size), sentence_pre_list[:80]))
					
					# write data to file
					d2f.write_file('log_lstm_train_1.txt', train_text, sentence_pre_list[1:])
					'''
					
					'''
					# Generate train data.
					sentence_predict = train_text[0]
					reset_sample_state.run()
					sentence_pre_list = [sentence_predict]
					# predict 1 to multiple
					for i in range(train_size):
						sentence_pre_list = [train_text[i]]
						for _ in range(4):
							b = train_batches.next()
							predictions = sample_prediction.eval({sample_input: b[0][0].reshape((1,-1))})
							feed = sample(predictions)
							sentence_pre_list.append(characters(feed)[0])
					
						# write data to file
						d2f.write2file('log_lstm_train_4.txt', sentence_pre_list[0], [sentence_pre_list[1:]])
					'''
					'''
					# Generate train data.
					sentence_predict = train_text[3]
					reset_sample_state.run()
					sentence_pre_list = [sentence_predict]
					# predict multiple to 1
					for _ in range(train_size-4):
						b = train_batches.next()
						predictions = sample_prediction.eval({sample_input: b[0][0].reshape((1,-1))})
						feed = sample(predictions)
						sentence_pre_list.append(characters(feed)[0])
					print('The result sample after %sth training: %s' % (str(train_size-4), sentence_pre_list[:80]))
					
					# write data to file
					d2f.write4file('log_lstm_4_train.txt', train_text, sentence_pre_list[1:])
					'''
					
					# Generate test data.
					print('*' * 80)
					sentence_predict = valid_text[0]
					reset_sample_state.run()
					sentence_pre_list = [sentence_predict]
					for _ in range(valid_size):
						b = valid_batches.next()
						predictions = sample_prediction.eval({sample_input: b[0]})
						feed = sample(predictions)
						sentence_pre_list.append(characters(feed)[0])
					print('test_data prediction sample: %s' % (sentence_pre_list[:80]))
					print('*' * 80)
					
					# Save all variables of the TensorFlow graph to a checkpoint. 
					saver.save(session, save_path=save_path, global_step=global_step)
					print("Saved checkpoint.")
					
	# calculate accuracy_precision_recall_fscore
	y_true = valid_text
	y_pred = sentence_pre_list[:-1]
	acc = accuracy_score(y_true, y_pred)
	pre = precision_score(y_true, y_pred, average='weighted')
	rec = recall_score(y_true, y_pred, average='weighted')  
	f1 = f1_score(y_true, y_pred, average='weighted')
	eva_name = ['accuracy', 'precision', 'recall', 'fscore']
	eva_value = [str(acc), str(pre), str(rec), str(f1)]
	print('argument dimension size: %s' % vocabulary_size)
	print(' '.join(eva_name)+' : '+ ' '.join(eva_value))
	# save evaluation
	d2f.write_eva('log_lstm_evaluation4.txt', eva_name, eva_value)

