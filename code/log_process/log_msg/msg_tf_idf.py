from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# tf_idf function, return tfidf array
def tf_idf(word_list):
	text_list = []
	for text in word_list:
		texts = ' '.join(text)
		text_list.append(unicode(texts, errors='ignore'))
	vectorList = text_list
	print vectorList
	
	vectorizer = CountVectorizer()
	ft = vectorizer.fit_transform(vectorList)
	counts = ft.toarray()
	transformer = TfidfTransformer()
	tfidf = transformer.fit_transform(counts)	
	tfidf_ = tfidf.toarray()
	return tfidf_