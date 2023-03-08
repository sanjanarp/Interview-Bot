!pip install fuzzywuzzy
import spacy
from fuzzywuzzy import fuzz

nlp = spacy.load('en_core_web_sm')

#Question: What are your weaknesses?

sample_dataset = ['procrastination',
                  'organization',
                  'confident',
                  'communication',
                  'flexibility',
                  'leadership',
                  'time management']

sample_statement = ["I'm disorganized",
                    "I fail to communicate very well",
                    "Sometimes I'm not flexible",
                    "I procrastinate a lot sometimes, but I try to improve myself daily",
                    "I'm not very organized", 
                    "I can't manage my time properly"]

# Create a list of all keywords found in sample_statement
keywords = []
for statement in sample_statement:
    doc = nlp(statement)
    for token in doc:
        if token.pos_ in ['NOUN', 'VERB', 'ADJ'] and not token.is_stop:
            keywords.append(token.lemma_)

# Match the keywords with strings in sample_dataset and keep track of frequency
matched_words = {}
for word in sample_dataset:
    if word in keywords:
        matched_words[word] = keywords.count(word)
    else:
        # Use fuzzy matching to match words in sample_dataset
        for keyword in keywords:
            if fuzz.token_set_ratio(word.lower(), keyword.lower()) >= 60:
                matched_words[word] = matched_words.get(word, 0) + 1

print(matched_words)


