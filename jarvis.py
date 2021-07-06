import pyttsx3
import requests
import urllib
import pyaudio
import webbrowser
import smtplib
import random
from PyDictionary import PyDictionary
from googlesearch import search
import ety
from nltk.corpus import wordnet
import speech_recognition as sr
import wikipedia
import datetime
import time
import wolframalpha
import os
import sys
import subprocess
from pygame import mixer

engine = pyttsx3.init('sapi5')

#client = wolframalpha.Client('Your_App_ID')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)     # Slows down the speaking speed of the engine voice.


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

speak('Hello Sir, I am your digital assistant JARVIS !')
speak('Welcome to Aptech Konnagar.')
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
            pass
    return query

def playMusic():
    music_folder ='F:\My hit songs\\'
    music = os.listdir(music_folder)
    random_music = music_folder + random.choice(music)
    mixer.init()
    mixer.music.load(random_music)
    mixer.music.play()

def find(name, path):
    for root, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def searchOnGoogle(query, outputList):
    speak('The top five search results from Google  are listed below.')
    for output in search(query, tld="https://www.google.co.in", num=10, stop=5, pause=2):
        print(output)
        outputList.append(output)
    return outputList

def openLink(outputList):
    speak("Here's the first link for you.")
    webbrowser.open(outputList[0])


def playOnYoutube(query_string):
    query_string = urllib.parse.urlencode({"search_query" : query})
    search_string = str("http://www.youtube.com/results?" + query_string)
    speak("Here's what you asked for. Enjoy!")
    webbrowser.open_new_tab(search_string)


def tellAJoke():
    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept":"application/json"}
        )
    if res.status_code == 200:
        speak("Okay. Here's one")
        speak(str(res.json()['joke']))
    else:
        speak('Oops!I ran out of jokes')
def getCompleteInfo(word):
    dictionary = PyDictionary()
    mean = {}
    mean = dictionary.meaning(word)
    synonyms = []
    antonyms = []

    speak("Alright. Here is the information you asked for.")

    for key in mean.keys():
        speak("When "+str(word)+" is used as a "+str(key)+" then it has the following meanings")
        for val in mean[key]:
            print(val)
        print()


    speak("The possible synonyms and antonyms of "+str(word)+" are given below.")
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas():
            if l.name() not in synonyms:
                synonyms.append(l.name())
            if l.antonyms() and l.antonyms()[0].name() not in antonyms:
                antonyms.append(l.antonyms()[0].name())
    
    print("Synonyms: ", end = " ")
    print(' '.join(synonyms), end = " ")
    print("\n")
    print("Antonyms: ", end = " ")
    print(' '.join(antonyms), end = " ") 
    print("\n")

    ori = ety.origins(word)
    if len(ori) > 0:
        speak("There are "+str(len(ori))+" possible origins found.")
        for origin in ori:
            print(origin)
    else:
        speak("I'm sorry. No data regarding the origin of "+str(word)+" was found.")


        
  
if __name__ == '__main__':

    while True:
    
        query = myCommand()
        query = query.lower()
        
        if 'open youtube' in query or 'open my youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')
            time.sleep(2)
            speak('this is your youtube sir and enjoy it')
        #elif 'play music' in query:
        #    speak("Here's your music. Enjoy !")
         #   playMusic()

       # elif 'stop the music' in query or 'stop the song' in query or 'stop' in query :
       #     mixer.music.stop()
       #     speak('The music is stopped.')

        elif 'find file' in query:
            speak('What is the name of the file that I should find ?')
            query = myCommand()
            filename = query
            print(filename)
            speak('What would be the extension of the file ?')
            query = myCommand()
            query = query.lower()
            extension = query
            print(extension)
            fullname = str(filename) + '.' + str(extension)
            print(fullname)
            path = 'F:\\'
            location = find(fullname,path)
            speak('File is found at the below location')
            print(location)

        elif 'search' in query:
            outputList = []
            speak('What should I search for ?')
            query = myCommand()
            searchOnGoogle(query, outputList)
            speak('Should I open up the first link for you ?')
            query = myCommand()
            if 'yes' in query or 'sure' in query:
                openLink(outputList)
            if 'no' in query:
                speak('Alright.')

        elif 'play on youtube' in query:
            speak('What should I look up for ?')
            query = myCommand()
            playOnYoutube(query)            

        elif 'open dictionary' in query or 'dictionary' in query:
            speak('What word should I look up for ?')
            word = myCommand()
            getCompleteInfo(word)
       
        elif 'joke' in query:
            tellAJoke()
        
        elif 'open flipkart' in query:
            speak("okay sir")
            webbrowser.open("https://www.flipkart.com")
        
        elif 'open chrome' in query:
            speak('opening your chrome browser sir')
            subprocess.call("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
            time.sleep(2)
            speak('this is your chrome browser and search your query on chrome')
        elif 'open firefox' in query or 'open my firefox' in query:
            speak('openning your firefox browser sir.')
            subprocess.call("C:/Program Files/Mozilla Firefox/firefox.exe")
            time.sleep(2)
            speak('this is your firefox browser and search your query on firefox')
        elif 'open file Explorer' in query or 'open file' in query:
            speak('opening your file Explorer ')
            subprocess.call("Quick access")
        elif 'open webcam' in query:
            speak('opening your webcam camera')
            subprocess.call("C:\Program Files (x86)\CyberLink\YouCam\YouCam.exe")
            time.sleep(4)
        elif 'open photoshop' in query:
            speak('opening your photoshop')
            subprocess.call("C:/Program Files (x86)/Adobe/Photoshop 7.0/Photoshop.exe")
            time.sleep(5)
        elif 'open adobe reader' in query or 'open adobe' in query:
            speak('opening your Adobe Reader')
            subprocess.call("C:/Program Files (x86)/Adobe/Reader 11.0/Reader/AcroRd32.exe")
            time.sleep(4)
        
        elif 'open microsoft office excel' in query or 'open microsoft excel' in query:
            speak('opening your microsoft office excel')
            subprocess.call("C:/Program Files (x86)/Microsoft Office/Office12/EXCEL.EXE")
            time.sleep(4)
        elif 'open microsoft office groove' in query or 'open microsoft groove' in query:
            speak('opening your microsoft office groove')
            subprocess.call("C:/Program Files (x86)/Microsoft Office/Office12/GROOVE.EXE")
            time.sleep(4)
        elif 'open microsoft office infopath' in query or 'open microsoft infopath' in query:
            speak('opening your microsoft office infopath')
            subprocess.call("C:/Program Files (x86)/Microsoft Office/Office12/INFOPATH.EXE")
            time.sleep(4)
        elif 'open microsoft onenote' in query or 'open onenote' in query:
            speak('opening your microsoft office onenote')
            subprocess.call("C:/Program Files (x86)/Microsoft Office/Office12/ONENOTE.EXE")
            time.sleep(4)
        elif 'open microsoft outlook' in query or 'open outlook' in query:
            speak('opening your microsoft office outlook')
            subprocess.call("C:/Program Files (x86)/Microsoft Office/Office12/OUTLOOK.EXE")
            time.sleep(4)
        elif 'open microsoft powerpoint' in query or 'open powerpoint' in query:
            speak('opening your microsoft office powerpoint')
            subprocess.call("C:/Program Files (x86)/Microsoft Office/Office12/POWERPNT.EXE")
            time.sleep(4)
        elif 'open microsoft word' in query or 'open word' in query:
            speak('opening your microsoft office word')
            subprocess.call("C:/Program Files (x86)/Microsoft Office/Office12/WINWORD.EXE")
            time.sleep(4)
        elif 'open pivot animator' in query or 'open animator':
            speak('opening your microsoft office pivot animator')
            subprocess.call("C:/Program Files (x86)/Pivot Animator/pivot.exe")
            time.sleep(4)
        elif 'open shareit' in query or 'open share' in query:
            speak('opening your shareit')
            subprocess.call("C:/Program Files (x86)/SHAREit Technologies/SHAREit/SHAREit.exe")

        elif 'open team viewer' in query or 'team viewer' in query:
            speak('opening your team viewer')
            subprocess.call("C:/Program Files (x86)/TeamViewer/TeamViewer.exe")
            time.sleep(4)
        elif 'open windows media player' in query or 'open media player' in query:
            speak('opening your windows media player')
            subprocess.call("C:/Program Files (x86)/Windows Media Player/wmplayer.exe")
            time.sleep(4)
                   
        elif 'current time' in query:
            #speak("It's your current time sir")
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
        elif 'open google' in query or 'open my google' in query:
            speak('okay sir, i am opening your Google sir')
            webbrowser.open('www.google.co.in')
            time.sleep(2)
            speak('this is your Google search engine sir...')
        elif 'open facebook' in query or 'open my facebook' in query:
            speak('okay sir, i am opening your facebook sir')
            webbrowser.open('https://www.facebook.com/')
            time.sleep(2)
            speak('this is your social media "Facebook" sir')

        elif 'open gmail' in query or 'open my gmail' in query:
            speak('okay sir, i am opening your Gmail sir')
            webbrowser.open('www.gmail.com')
            time.sleep(2)
            speak('this is your Gmail and now you are using gmail sir')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

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


        
        elif 'bye' in query:
            speak('Bye Sir, have a good day.')
            sys.exit()
        elif 'shutdown my laptop' in query or 'shutdown laptop' in query:
            os.system("shutdown /s /t 1");
        elif 'restart my laptop' in query or 'restart laptop' in query:
            os.system("shutdown /r /t 1");

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
                    
        
        speak('Next Command! Sir!')
        







