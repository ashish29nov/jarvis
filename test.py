import datetime
from math import e
import os
import smtplib
import subprocess
import time
from typing import KeysView
from urllib.parse import quote_from_bytes
import webbrowser
import pyttsx3
import speech_recognition as sr
import cv2
from requests import get
import wikipedia
import pywhatkit as kit
import wolframalpha


engine = pyttsx3.init('sapi5')

#client = wolframalpha.Client('Your_App_ID')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

rate = engine.getProperty('rate')
#engine.setProperty('rate', rate-50)     # Slows down the speaking speed of the engine voice.

def speak(audio):
    print('Jarvis: ' + audio)
    engine.say(audio)
    engine.runAndWait()
def greetMe():
    currentH = int(datetime.datetime.now().hour)
    currentM = int(datetime.datetime.now().minute)    
    if currentH >= 0 and currentH < 12:
        
        speak('Good Morning!')

    if currentH >= 12 and currentH < 18:

        speak('Good Afternoon!')
        
    if currentH >= 18 and currentH !=0:
        speak('Good Evening!')

greetMe()

#speak('Hello Sir, I am your digital assistant JARVIS !')
#speak('Welcome to Aptech Konnagar.')
speak('How may I help you?')
def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        audio=r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        stop_listening = r.listen_in_background(sr.Microphone(), myCommand)   
        try:
            query = r.recognize_google(audio, language='en-in')
            print('User: ' + query + '\n')
        except sr.UnknownValueError:
            myCommand()
            
        return query

if __name__ == '__main__':
     while True:
        query=myCommand().lower()

        if 'open chrome' in query:
            speak('opening your chrome browser sir')
            subprocess.call("C:\Program Files\Google\Chrome\Application\chrome.exe")
            time.sleep(2)
            speak('this is your chrome browser and search your query on chrome')
            
        elif 'open firefox ' in query:
            speak('opening your firefox browser ')
            subprocess.call("C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")
            time.sleep(3)
            speak('this is your firefox and search your query on firefox')

        elif 'open cammand promt' in query:
            speak("openinig")
            subprocess.run(["ls", "-l"])
        

        
        elif 'open camera' in query:
            speak("opening camera")
            cap=cv2.VideoCapture(0)
            while True:
                ret, img=cap.read()
                cv2.imshow('webcam',img)
                k=cv2.waitKey(10)
                if k==27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "ip address" in query:
            ip=get('https://api.ipify.org').text
            speak(f"your ip address is {ip}")

        elif "wikipedia" in query:
            speak('search in  wikipedia ')
            query=query.replace("wikipedia")
            results=wikipedia.summary(query, sentences=2)
            speak("adccourding to wikipedia.....")
            speak(results)
            print(results)
        
        elif "open google" in query:
            speak("sir, what should i search on google")
            cm=myCommand().lower()
            webbrowser.open(f"{cm}")

        #elif "send a message" in query:
          #  kit.sendwhatmsg("+91911858338","for testing",2,25)
        
        elif 'send my email' in query or 'send my mail' in query:
            speak('Who is the recipient? ')
           # speak('please enter an email id.')
            recipient = input('please enter an email id: ')
            
            fromaddr='ramzna96@gmail.com'
           
            try:
                speak('What should I say? ')
                content = myCommand()
                    
        
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login("ramzna96@gmail.com", 'your password')
                server.sendmail(fromaddr, recipient, content)
                server.close()
                speak('Email sent!')

            except:
                speak('Sorry Sir! I am unable to send your message at this moment!')

        else:
            query = query
            #speak('Searching...')
            try:
                try:
                    res = wolframalpha.Client.query(query)
                    results = next(res.results).text
                    speak('search in  wikipedia ')
                    speak("Here's your result")
                    speak(results)
                    
                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('search in wikipedia.')
                    speak('WIKIPEDIA says - ')
                    speak(results) 
            except:
                speak('search in  google')
                url='https://www.google.co.in/search?q='
                result=url+query
                webbrowser.open(result)
                # webbrowser.open('www.google.com')    
                # 
        speak('Next Command! Sir!') 
                    