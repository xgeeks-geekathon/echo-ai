import string
import nltk
from nltk.tokenize import SpaceTokenizer
from nltk.probability import FreqDist

nltk.download("stopwords")

def findTopWords(text):
    sw=nltk.corpus.stopwords.words('english')
    punctuation = string.punctuation

    text_no_punc = text.translate(str.maketrans('', '', punctuation))

    text_tokens = SpaceTokenizer().tokenize(text_no_punc)

    words_ne = []
    for word in text_tokens:
        if word not in sw and word not in punctuation and len(word) > 1:
            words_ne.append(word)

    fq = FreqDist(token.lower() for token in words_ne)
    most_common = fq.most_common(10)

    formatted_most_common = []
    for word in most_common:
        formatted_most_common.append(word[0] + " -> " + str(word[1]))

    return "\n".join(formatted_most_common)