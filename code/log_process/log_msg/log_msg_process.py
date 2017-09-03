import MySQLdb
import re
import msg_tf_idf as mti

# configure db
hostname = "localhost"       
port = 3306
username = "root"
password = "111111"
dbname = "bdtune"           
tablename = "logInfo"         
 
def readDB():
	conn = MySQLdb.connect(host=hostname, port=port, user=username, passwd=password, db=dbname)
	cur = conn.cursor()
	sql = "select msg from " + tablename + ";"
	cur.execute(sql)
	res = cur.fetchall()
	return res
	cur.close()
	conn.commit()
	conn.close()
	
def read_file(filename):
	of = open(filename, 'r+')
	text = []
	for line in of:
		text.append(line.split()[0])
	of.close()
	return text
	
def msg_filter(stopwords_, symbols_):

	# load msd from db
	contents = []
	for msg in readDB():
		contents.append(msg[0])
		
	# lower words
	text_lower = [[word for word in document.lower().split()] for document in contents]
	
	# filter stopwords & symbols
	stopwords = read_file(stopwords_)
	text_filtered_stopwords = [[word for word in document if not word in stopwords] for document in text_lower]
	punctuations = read_file(symbols_)
	text_filtered = [[word for word in document if not word in punctuations] for document in text_filtered_stopwords]
	
	# drop word-frequency == 1
	'''
	all_text = sum(text_filtered, [])
	word_once = set(word for word in set(all_text) if all_text.count(word) == 1)
	text_final = [[word for word in text if word not in word_once] for text in text_filtered]
	return text_final
	'''
	return text_filtered
	
def geneFile():
	with open('log_msg_filtered.txt', 'w+') as f:
		for msg in msg_filtered:
			msg = ' '.join(msg)
			
			# regular expression filtering
			msg = re.sub(r'[0-9]+', '', msg)
			msg = re.sub(r'\:', '', msg)
			msg = re.sub(r'\,', '', msg)
			msg = re.sub(r'\'', '', msg)
			msg = re.sub(r'\-', '', msg)
			msg = re.sub(r'\[', '', msg)
			msg = re.sub(r'\]', '', msg)
			msg = re.sub(r'\[\]', '', msg)
			msg = re.sub(r'\(\)', '', msg)
			msg = re.sub(r'[0-9]?[a-z]?[0-9]+', '', msg) 
			msg = re.sub(r'[0-9]+\:[0-9]+\:[0-9]+', '', msg) 
			msg = re.sub(r'\<[f]+[0-9]*[a-z]*\?*[0-9]*[a-z]*\_*[a-z]*\/*[a-z]*\<*\>*f*\]*\>*', '', msg)  	
			msg = re.sub(r'[0-9]+\.[0-9]+', '', msg)
			msg = re.sub(r' br ', '', msg)	
			msg = re.sub(r'"x"', '', msg)
			msg = re.sub(r' c  ', '', msg)
			msg = re.sub(r' cc ', '', msg)
			msg = re.sub(r' p ', '', msg)
			msg = re.sub(r'# ', '', msg)
			msg = re.sub(r' f ', '', msg)
			msg = re.sub(r'f{2,99}[a-z]*', '', msg)
			msg = re.sub(r'[a-z]+f{3,99}[a-z]*', '', msg)	
			msg = re.sub(r'\s(ok\s)+', '', msg)	
			msg = re.sub(r'\#\/*', '', msg)
			msg = re.sub(r' \(v ', '', msg)
			msg = re.sub(r' \) ', '', msg)
			msg = re.sub(r' \/ ', '', msg) 
			msg = re.sub(r'\?+', '', msg) 
			msg = re.sub(r'\*{2,29}', '', msg) 
			msg = re.sub(r'(\>\s)+', '', msg) 
			msg = re.sub(r' *kb', '', msg) 
			msg = re.sub(r'\s{4,9}', '', msg) 
			msg = re.sub(r'\<*\>*f{2,9}[a-z]*\>', '', msg)
			msg = re.sub(r' \.', '', msg)
			if msg != '':				
				f.write(msg+'\n')
			
if __name__ == '__main__':
	stopwords_ = 'log_msg_stopwords.txt'
	symbols_ = 'log_msg_symbols.txt'
	msg_filtered = msg_filter(stopwords_, symbols_)
	# msg tf-idf
	tf_idf_ = mti.tf_idf(msg_filtered)
	print tf_idf_
	# write filtered msg into file
	geneFile()
	
	