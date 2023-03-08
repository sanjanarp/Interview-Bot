import pandas as pd
import nltk
import language_tool_python
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Initialize the LanguageTool tool
tool = language_tool_python.LanguageTool('en-US')

# Define a function to calculate the Sentiment Score for a given text
def calculate_sentiment_score(text, question_type):
    # Initialize the Sentiment Intensity Analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Tokenize the text and remove stop words
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token.lower() not in stopwords.words('english')]
    
    # Calculate the sum of sentiment values and weights for all words in the text
    sentiment_sum = sum(sia.polarity_scores(token)['compound'] for token in filtered_tokens)
    weight_sum = sum(get_sentiment_weight(sia.polarity_scores(token)['compound']) for token in filtered_tokens)
    
    # Define the value of T based on the question type
    if question_type == 'technical':
        t = 0.25
    else:
        t = 0.5
        
    # Calculate the Sentiment Score using the formula
    sentiment_score = ((sentiment_sum * weight_sum) * t) / 3
    
    return sentiment_score

# Define a function to get the weight for a given sentiment value
def get_sentiment_weight(sentiment):
    if sentiment > 0:
        return sentiment
    elif sentiment < 0:
        return -sentiment
    else:
        return 0

# Define a function to calculate the Grammar Check Score for a given text
def calculate_grammar_check_score(text):
    # Check the grammar and count the number of errors
    matches = tool.check(text)
    num_errors = len(matches)
    
    # Calculate the Grammar Check Score using the formula
    grammar_check_score = 1 - (num_errors / len(word_tokenize(text)))
    
    return grammar_check_score

# Define a sample dataset of interview questions and candidate answers
data = {
    'Question': ['Tell me about yourself.', 'What is dbms?', 'What are your weaknesses?'],
    'Answer': ['I am a recent graduate with a degree in Computer Science. I am passionate about programming and have worked on several projects during my studies. In my free time, I enjoy playing video games and practicing yoga.',
              'A database management system (or DBMS) is essentially nothing more than a computerized data-keeping system. Users of the system are given facilities to perform several kinds of operations on such a system for either manipulation of the data in the database or the management of the database structure itself.',
               'One weaknesses is that I can be too critical of my own work. I tend overthink things and sometimes struggle with making decisions. However, I have been working on improving my decision-making skills by seeking feedback from others.'],
    'Question_Type': ['non-technical', 'technical', 'non-technical']
}
df = pd.DataFrame(data)

# Calculate the Sentiment Score and Grammar Check Score for each answer
def calculate_scores(text, question_type):
    sentiment_score = calculate_sentiment_score(text, question_type)
    grammar_check_score = calculate_grammar_check_score(text)
    
    return pd.Series([sentiment_score, grammar_check_score])

df[['Sentiment_Score', 'Grammar_Check_Score']]= df.apply(lambda row: calculate_scores(row['Answer'], row['Question_Type']), axis=1)
print(df[['Question', 'Answer','Grammar_Check_Score', 'Sentiment_Score']])
