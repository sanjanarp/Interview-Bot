import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_keywords(text):
    # Use a custom list of stop words
    stop_words = set(["the", "a", "an", "in", "on", "at", "of", "for"])
    
    # Use Porter stemmer for stemming
    stemmer = PorterStemmer()
    
    words = word_tokenize(text)
    keywords = []
    
    for word in words:
        # Skip stop words
        if word in stop_words:
            continue
        
        # Stem the word
        stemmed_word = stemmer.stem(word)
        
        # Use a POS tagger to only include nouns, verbs, and adjectives
        tagged_word = nltk.pos_tag([stemmed_word])
        if tagged_word[0][1] in ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "JJ", "JJR", "JJS"]:
            keywords.append(tagged_word[0][0])
    
    return keywords


'''text = "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human (natural) languages. As such, NLP is related to the area of human-computer interaction."
keywords = extract_keywords(text)
print(keywords)'''


# sample_list = ['confidence', 'lack', 'flexibility','perfectionism']
# sample_dataset = ['Linguist',
# 'procrastination',
# 'disorganization',
# 'lack of confidence',
# 'lack of communication skills',
# 'lack of flexibility',
# 'lack of leadership skills',
# 'lack of time management skills'
# ]

sample_dataset = ['human',
'nlp',
'intelligence',
'concern',
'artificial',
]


def match_keyword(sample_list, sample_dataset):
    matched_words = {}
    for word in sample_list:
        found = False
        for data in sample_dataset:
            if re.search(word, data) and not found:
                matched_words[data] = word
                found = True

    return matched_words

#match_keyword(keywords, sample_dataset)