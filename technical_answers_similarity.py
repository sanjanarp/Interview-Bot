!pip install sumy

import nltk
from nltk.tokenize import sent_tokenize
from difflib import SequenceMatcher
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

# Technical questions
questions = ["What is a stack in programming?", "What is object-oriented programming?"]

# Original answers
original_answers = ["A stack is a data structure that follows the Last-In-First-Out (LIFO) principle. It is used to store and retrieve data in an efficient and organized manner.", 
                    "Object-oriented programming (OOP) is a programming paradigm that uses objects to represent and manipulate data. It emphasizes encapsulation, inheritance, and polymorphism."]

# Candidate answers
candidate_answers = []

# Ask each question and record candidate's answer
for question in questions:
    candidate_answer = input(question + " ")
    candidate_answers.append(candidate_answer)

# Summarize each candidate answer and compare to original answer
for i in range(len(candidate_answers)):
    # Tokenize candidate answer into sentences
    candidate_sentences = sent_tokenize(candidate_answers[i])

    # Summarize candidate answer using TextRank
    parser = PlaintextParser.from_string(candidate_answers[i], Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summarizer.stop_words = nltk.corpus.stopwords.words('english')
    summary = summarizer(document=parser.document, sentences_count=1)

    # Compare summary to original answer using SequenceMatcher
    similarity_ratio = SequenceMatcher(None, str(summary[0]).lower(), original_answers[i].lower()).ratio()

    # Print similarity percentage
    print("Question:", questions[i])
    print("Original Answer:", original_answers[i])
    print("Candidate Answer:", candidate_answers[i])
    print("Similarity Percentage:", round(similarity_ratio*100, 2), "%")
    print()
