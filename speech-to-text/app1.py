from doctest import OutputChecker
import speech_recognition as sr
import pyttsx3 as pt
import spacy
import Levenshtein
from fuzzywuzzy import fuzz
import re
import joblib

engine = pt.init('sapi5')
nlp = spacy.load('en_core_web_sm')
sample_dataset = ['procrastination',
                  'organization',
                  'confident',
                  'communication',
                  'flexibility',
                  'leadership',
                  'time management']

# assistant_speaking: convert text to speech using pyttsx3
def assistant_speaking(speech):
    engine.say(speech)
    engine.runAndWait()

# hello: greet user based on current time
def hello():
        print("Hi!")
        assistant_speaking("Hi,Thanks for joining me")

# interview_bot: ask questions related to an interview
def interview_bot():
    MAX_ATTEMPTS = 3   # maximum number of attempts to get valid input
    TIMEOUT = 10       # maximum wait time for input in seconds

    # Load Rasa interpreter with the training data file
    model_path = "speech-to-text\models\model.joblib"
    interpreter = joblib.load(model_path)
    
    # Open keywords.txt file and read all the lines
    pattern_regex = '|'.join([re.escape(line.strip()) for line in open('keywords.txt')])
    follow_up_regex = f".*({pattern_regex})+.*"
    keywords = [line.strip() for line in open('keywords.txt')]

    # Define follow-up questions based on intents
    follow_up_questions = {
        "get_name": [
            "Nice to meet you. Can you tell me more about yourself?",
            "What is your professional experience?"
        ],
        "work_experience": [
            "Tell me more about your role at {org}.",
            "Can you give me an example of a project you worked on at {org}?"
        ],
        "strengths_and_weaknesses": [
            "Interesting. Can you share how your communication skills have benefitted your previous company?",
            "How are you working to improve your procrastination issue?"
        ],
        "leadership_example": [
            "How did you handle any conflicts within your team?",
            "Can you describe a situation where you had to make a tough decision?"
        ]
    }

    # Add these follow up questions to the list of questions 
    questions = ["Let's start with your name."]
    
    # loop over each keyword, and build out question and potential followup questions
    for keyword in keywords:
        if "work experience" in keyword.lower():
            questions.append("Great!. Can you tell me about your work experience?")
        elif "strengths" in keyword.lower() and "weaknesses" in keyword.lower():
            questions.append("Interesting. What are your strengths and weaknesses?")
        elif any(x in keyword.lower() for x in ["lead", "leadership"]):
            questions.append("Okay. Can you give an example of a time when you demonstrated leadership?")
        elif any(x in keyword.lower() for x in ["communication", "communicate"]):
            questions.append("I think communication is important in any role. Can you tell me about your communication style?")
        elif "time management" in keyword.lower():
            questions.append("Tell me about how you manage your time?")

    answers = []      
    
    for i, q in enumerate(questions):
        assistant_speaking(q)
        attempts = 0
        
        while attempts < MAX_ATTEMPTS:
            statement, entities = assistant_recognize_voice() 
            
                    # Use Rasa interpreter to extract intent and entities from the statement
        try:
            intent = interpreter.parse(statement)['intent']['name']
            entities = interpreter.parse(statement)['entities']
        except:
            intent = None
            entities = None
            
        # If intent is None or timeout occurs, repeat the question or move on to the next question
        if not intent and attempts == MAX_ATTEMPTS-1:
            assistant_speaking("I am sorry, I did not understand your response.")
            break
        elif not intent:
            attempts += 1
            continue
        
        # If the user's response contains a follow-up keyword, ask a follow-up question
        if re.match(follow_up_regex, statement):
            follow_up_key = next((k for k in follow_up_questions.keys() if k in intent), None)
            if follow_up_key:
                follow_up_question = follow_up_questions[follow_up_key][i % len(follow_up_questions[follow_up_key])]
                assistant_speaking(follow_up_question.format(**entities))
                continue
        
        # If the intent matches any of the follow-up questions, ask a follow-up question
        if intent in follow_up_questions:
            follow_up_question = follow_up_questions[intent][i % len(follow_up_questions[intent])]
            assistant_speaking(follow_up_question.format(**entities))
            continue
        
        # Otherwise, add the user's response to the answers list and move on to the next question
        answers.append(statement)
        break

# Print the user's answers to each question
    assistant_speaking("Thank you for your time. Here are your answers:")
    for i, ans in enumerate(answers):
        assistant_speaking(f"Question {i+1}: {questions[i]}")
        assistant_speaking(f"Answer: {ans}")

def assistant_recognize_voice():
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Listening...")
                    recognizer.pause_threshold = 1
                    audio = recognizer.listen(source)
                    try:
                        print("Recognizing...")
                        statement = recognizer.recognize_google(audio, language='en-in')
                        print(f"User said: {statement}\n")
                        doc = nlp(statement)
                        entities = {e.label_: e.text for e in doc.ents}
                        return statement, entities
                    except Exception as e:
                        print(e)
                        assistant_speaking("I am sorry, I did not understand your response. Can you please repeat that?")
                        return None

if __name__ == 'main':
    hello()
    interview_bot()






