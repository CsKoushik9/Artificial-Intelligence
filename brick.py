import speech_recognition as sr
import os
from playsound import playsound
import webbrowser
import random
from google import google
import pyttsx3
import requests
import json
speech = sr.Recognizer()
greeting_dict = {'hello': 'hello', 'hi': 'hi'}
open_launch_dict = {'open': 'open', 'launch': 'launch'}
lists = ['mp3/yakwa/launching.mp3', 'mp3/yakwa/launching1.mp3', 'mp3/yakwa/Launching2.mp3']
social_media_dict = {'facebook': 'https://www.facebook.com/', 'twitter': 'https://twitter.com/login?lang=en', 'youtube': 'https://www.youtube.com/',
                     'chrome': 'https://www.google.com/'}
greet_list = ['mp3/yakwa/greeting.mp3', 'mp3/yakwa/greeting1.mp3']
google_searches = {'what': 'what', 'why': 'why', 'who': 'who', 'how': 'how', 'where': 'where', 'how many': 'how many', 'which': 'which'}
bye_list = ['mp3/yakwa/thankyou.mp3', 'mp3/yakwa/thankyou1.mp3']
reply_list = ['mp3/yakwa/thankyoureply1.mp3','mp3/yakwa/thankyoureply.mp3']

try:
    engine = pyttsx3.init()
except ImportError:
    print('Requested Driver is not found')
except RuntimeError:
    print('Driver fails to initialize')

voices = engine.getProperty('voices')
engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
rate = engine.getProperty('rate')
engine.setProperty('rate',rate)
#engine.say('Hello sir, This is Yakwa...')
engine.runAndWait()


def speak_text_cmd(cmd):
    engine.say(cmd)
    engine.runAndWait()


def google_search_result(query):
    search_result = google.search(query)
    for result in search_result:
        print(result.description)
        speak_text_cmd(result.description)
        break


def is_valid_google_search(phrase):
    if google_searches.get(phrase.split(' ')[0]) == phrase.split(' ')[0]:
        return True


def play_sound(mp3_list):
    mp3 = random.choice(mp3_list)
    playsound(mp3)


def read_voice_cmd():
    voice_text = ''
    print('Listening')
    with sr.Microphone() as source:
        audio = speech.listen(source=source,timeout=10,phrase_time_limit=9)
    try:
        voice_text = speech.recognize_google(audio)
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        print('Network error')
    except sr.WaitTimeoutError:
        pass

    return voice_text


def is_valid_greeting(greet_dict,voice_n):
    for key,value in greet_dict.iteritems():
        if value == voice_n.split(' ')[0]:
            return True
            break
    return False


def is_valid_open_launch(open_launch_dict,voice_n):
    for key,value in open_launch_dict.iteritems():
        try:
            if value == voice_n.split(' ')[0]:
                return True
                break
            elif key == voice_n.split(' ')[1]:
                return True
                break
        except IndexError:
            pass
    return False


if __name__ == '__main__':
    playsound('mp3/yakwa/intro4.mp3')
    while True:
        voice_n = read_voice_cmd().lower()
        print('cmd: {}'.format(voice_n))
        if is_valid_greeting(greeting_dict,voice_n):
            print('Greeting')
            play_sound(greet_list)
            continue
        elif 'who are you' in voice_n:
            playsound('mp3/yakwa/about.mp3')
            continue
        elif 'what are you doing' in voice_n:
            playsound('mp3/yakwa/checking.mp3')
            continue
        elif 'where are we' in voice_n:
            playsound('mp3/yakwa/locating.mp3')
            send_url = 'http://freegeoip.net/json'
            r = requests.get(send_url)
            j = json.loads(r.text)
            lat = j['latitude']
            lon = j['longitude']
            reg = j['region_name']+" in the city of "+j['city']
            cnt = j['country_name']
            print('We are living in '+reg+' in the country of '+cnt+' at a latitude of '+str(lat)+' and a longitude of '+str(lon))
            speak_text_cmd('We are living in '+reg+' in the country of '+cnt+' at a latitude of '+str(lat)+' and a longitude of '+str(lon))
            continue
        elif 'i am fine' in voice_n:
            playsound('mp3/yakwa/finereply.mp3')
            continue
        elif is_valid_open_launch(open_launch_dict,voice_n):
            print('opening')
            play_sound(lists)
            if(is_valid_open_launch(social_media_dict,voice_n)):
                key = voice_n.split(' ')[1]
                webbrowser.open(social_media_dict.get(key))
            elif 'calculator' in voice_n:
                os.system('calc.exe')
            elif 'notepad' in voice_n:
                os.system('notepad.exe')
            elif 'chrome' in voice_n:
                os.system('chrome.exe')
            elif 'settings' in voice_n:
                os.system('control.exe')
            elif 'c m d' in voice_n or 'command' in voice_n:
                os.system('cmd.exe')
            continue
        elif 'goodbye' in voice_n:
            play_sound(bye_list)
            exit()
        elif 'how are you' in voice_n:
            playsound('mp3/yakwa/wishes.mp3')
            continue
        elif ''==voice_n:
            continue
        elif is_valid_google_search(voice_n):
            print('Google search')
            playsound('mp3/yakwa/search.mp3')
            google_search_result(voice_n)
            continue
        elif 'thank you' in voice_n:
            play_sound(reply_list)
            continue
        elif 'close' in voice_n:
            playsound('mp3/yakwa/manually.mp3')
            continue
        elif 'wish a birthday' in voice_n:
            playsound('mp3/yakwa/birthday.mp3')
            continue
        else:
            playsound('mp3/yakwa/search2.mp3')
            webbrowser.open('https://www.google.com/search?q=' + voice_n)
            continue
