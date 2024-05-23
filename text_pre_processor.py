from nltk.stem import PorterStemmer
import re
import string
ps = PorterStemmer()


def tokenize(text):
    return str(text).split()

def lowercase_filter(tokens):
    return [token.lower() for token in tokens]

def stem_filter(tokens):
    return [ps.stem(token) for token in tokens]

def num_filter(tokens):
    return [re.sub(r'\d+', '', token) for token in tokens]

PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))  # '[%d]' % 1 format specifier

def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]


from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
StopWords = stopwords.words("english")

def stopword_filter(tokens):
    return [token for token in tokens if token not in StopWords]



def pre_process(text):
    tokens = tokenize(text)
    tokens = num_filter(tokens)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    tokens = stem_filter(tokens)

    return tokens