import json
import speech_recognition as sr
import pyttsx3 as pt 
import wikipedia 
import webbrowser
import time  
import datetime 
import matchKeywords

engine=pt.init('sapi5') 
answer =""
question =""
sample_dataset = [    'perfectionism',    'procrastination',    'disorganization',    'lack of confidence',    'lack of communication skills',    'lack of flexibility',    'lack of leadership skills',    'lack of time management skills']


def assistant_speaking(speech):
    engine.say(speech) 
    engine.runAndWait() 


def hello():
    hour=datetime.datetime.now().hour  
    if hour>=4 and hour<12:
        print("Hello,Good Morning")
        assistant_speaking("Hello,Good Morning,Have a nice day friend")

    elif hour>=12 and hour<18:
        print("Hello,Good Afternoon")
        assistant_speaking("Hello,Good Afternoon")
        
    elif hour>=18 and hour<23:
        print("Hello,Good Evening, you still have a long night to do many things, stay positive!")
        assistant_speaking("Hello,Good Evening, you still have a long night to do many things, stay positive!")
        
    else:
        print("Hi,its never too late to work, have a good night!")
        assistant_speaking("Hi,its never too late to work, have a good night!")
        
		
		
def assistant_recognize_voice():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:  
        print("Listening...")
        vocal=recognizer.listen(source) 

        try:   
            statement=recognizer.recognize_google(vocal,language='en-in') 
            print(f"user said:{statement}\n")
            
        except Exception as e:   
           assistant_speaking("i cant hear you very well, I think you should repeat what you said.")
           return "None"
        return statement



if __name__=='__main__':
    hello() 
    while True: 
        assistant_speaking("how can I help you now?") 
        string ="how can I help you now?" 
        question = '{"question":"' + string +'"}'
        with open("output.json", "a") as outfile:
                   json.dump(question, outfile)
                   outfile.write('\n')
        statement = assistant_recognize_voice().lower()        

        if statement==0: 
            continue
        else:
            answer = '{"answer":"' + statement +'"}'
            with open("output.json", "a") as outfile:
                   json.dump(answer, outfile)
                   outfile.write('\n')
            extractedKeywords = matchKeywords.extract_keywords(statement)
            with open("extracted_keywords.txt", "a") as outfile:
                   outfile.write(str(extractedKeywords))
                   outfile.write('\n')
            matchedKeywords = matchKeywords.match_keyword(extractedKeywords,sample_dataset)
            with open("matched_keywords.txt", "a") as outfile:
                   outfile.write(str(matchedKeywords))
                   outfile.write('\n')
            
        if "goodbye" in statement or "ok bye" in statement or "stop" in statement:  
            print('Ok good bye see you later')
            string = 'Ok good bye see you later'
            assistant_speaking('Ok good bye see you later')
            question = '"question":"' + string +'"'
            with open("output.json", "a") as outfile:
                   json.dump(question, outfile)
                   outfile.write('\n')
            break
            
        elif 'time' in statement: 
            actualTime=datetime.datetime.now().strftime("%H:%M:%S") 
            assistant_speaking(f"the time is {actualTime}")
            print(f"the time is {actualTime}")
            string = f"the time is {actualTime}"
            question = '{"question":"' + string +'"}'
            with open("output.json", "a") as outfile:
                   json.dump(question, outfile)
                   outfile.write('\n')
            
        elif 'search'  in statement: 
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(4)  
        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement or "who invented you" in statement: 
            assistant_speaking("I was built by maryem samet")
            print("I was built by maryem samet")
        elif'wikipedia' in statement: 
            assistant_speaking('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=2)
            assistant_speaking("According to Wikipedia")
            print(results)
            assistant_speaking(results)
            question = '{"question":"' + results +'"}'
            with open("output.json", "a") as outfile:
                   json.dump(question, outfile)
                   outfile.write('\n')
