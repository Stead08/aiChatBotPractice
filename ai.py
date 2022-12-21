import speech_recognition as sr
import pyttsx3
import requests
# 応答用のAPI
TALKAPI_KEY = 'YOUR_API'

def talkapi(text):
    url = 'https://api.a3rt.recruit.co.jp/talk/v1/smalltalk'
    req = requests.post(url, {'apikey':TALKAPI_KEY,'query':text}, timeout=5)
    data = req.json()

    if data['status'] != 0:
        return data['message']

    msg = data['results'][0]['reply']
    return msg
#聞き取り部分
robot_ear = sr.Recognizer()
with sr.Microphone() as mic:
    print("AI: 聞いています。")
    audio = robot_ear.record(mic, duration=2)
try:
    you = robot_ear.recognize_google(audio, language="ja_JP")
except:
    you = "..."
# 自分の発言内容を表示
print("自分: " + you)
# 発言をtalk APIに投げる
robot_brain = talkapi(you)
# 返答を表示
print("AI:" + robot_brain)
def change_voice(engine, language):
    for voice in engine.getProperty('voices'):
        if language in voice.languages:
            engine.setProperty('voice', voice.id)
            return True
    raise RuntimeError("language not found".format(language))

engine = pyttsx3.init()
change_voice(engine, "ja_JP")
engine.say(robot_brain)
engine.runAndWait()
