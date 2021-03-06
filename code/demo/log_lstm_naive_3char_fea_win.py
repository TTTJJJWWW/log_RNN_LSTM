# Naive LSTM to learn three-char window to one-char mapping
import InsertTools
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.utils import np_utils

def load_data():
	conn=InsertTools.getConnection()
	cur=conn.cursor()
	sql="select timestamp, logid, severity from log_s1;"
	cur.execute(sql)
	res=cur.fetchall()
	sql2="select timestamp, logid, severity from log_p1;"
	cur.execute(sql2)
	res2=cur.fetchall()
	severity=['fatal','failure','critical','error','warning','notice','info','NULL']
	se_index=[0,1,2,3,4,5,6,7]
	se_raw,se_raw2,se_no,se_no2=[],[],[],[]
	for r in res:
		se_raw.append(r[2])
	for sr in se_raw:
		number=se_index[severity.index(sr)]
		se_no.append([number])
	for r2 in res2:
		se_raw2.append(r2[2])
	for sr2 in se_raw2:
		number2=se_index[severity.index(sr2)]
		se_no2.append([number2])
	cur.close()
	conn.commit()
	conn.close
	return se_raw,se_raw2
	
if __name__=='__main__':
	# fix random seed for reproducibility
	numpy.random.seed(7)
	# define the raw dataset
	datatrain, dataset = load_data()
	dataset = dataset[-25:]
	# create mapping of strings to integers and the reverse
	char_to_int = dict((c, i) for i, c in enumerate(dataset))
	int_to_char = dict((i, c) for i, c in enumerate(dataset))
	# prepare the dataset of input to output pairs encoded as integers
	seq_length = 3
	dataX = []
	dataY = []
	for i in range(0, len(dataset) - seq_length, 1):
		seq_in = dataset[i:i + seq_length]
		seq_out = dataset[i + seq_length]
		dataX.append([char_to_int[char] for char in seq_in])
		dataY.append(char_to_int[seq_out])
		print seq_in, '->', seq_out
	# reshape X to be [samples, time steps, features]
	X = numpy.reshape(dataX, (len(dataX), 1, seq_length))
	# normalize
	X = X / float(len(dataset))
	# one hot encode the output variable
	y = np_utils.to_categorical(dataY)
	# create and fit the model
	model = Sequential()
	model.add(LSTM(32, input_shape=(X.shape[1], X.shape[2])))
	model.add(Dense(y.shape[1], activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	model.fit(X, y, nb_epoch=100, batch_size=20, verbose=2)
	# summarize performance of the model
	scores = model.evaluate(X, y, verbose=0)
	print("Model Accuracy: %.2f%%" % (scores[1]*100))
	# demonstrate some model predictions
	for pattern in dataX:
		x = numpy.reshape(pattern, (1, 1, len(pattern)))
		x = x / float(len(dataset))
		prediction = model.predict(x, verbose=0)
		index = numpy.argmax(prediction)
		result = int_to_char[index]
		seq_in = [int_to_char[value] for value in pattern]
		print seq_in, "->", result