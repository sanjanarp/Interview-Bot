import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Load the JSON data
with open('speech-to-text/training_data.json', 'r') as f:
    data = json.load(f)

# Extract the common examples
common_examples = data['rasa_nlu_data']['common_examples']

# Extract X_train and y_train
X_train = [example['text'] for example in common_examples]
y_train = [example['intent'] for example in common_examples]

# Preprocess the data
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Define the model architecture
model = MultinomialNB()

# Train the model
model.fit(X_train, y_train)

# Store the model in a directory path
result = joblib.dump(model, 'speech-to-text\models\model.joblib')
print(result)