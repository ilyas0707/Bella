import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
 
opts = {
    "alias": ('белла','беллочка','белл','буня','бэлла','бэллочка',
              'бэлл'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси', 'пожалуйста'),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час'),
    }
}
 
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()
 
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("Распознано: " + voice)
   
        if voice.startswith(opts["alias"]):

            cmd = voice
 
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
           
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
 
    except sr.UnknownValueError:
        print("Голос не распознан!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
   
    return RC
 
def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
   
    else:
        print('Команда не распознана, повторите!')

r = sr.Recognizer()
m = sr.Microphone(device_index = 1)
 
with m as source:
    r.adjust_for_ambient_noise(source)
 
speak_engine = pyttsx3.init()
 
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
speak_engine.setProperty('voice', ru_voice_id)
 
speak("Добрый день, повелитель")
speak("Белла слушает")
 
stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop

# Voice:
# - ID: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0
# - Name: Microsoft David Desktop - English (United States)
# - Languages: []
# - Gender: None
# - Age: None
# Voice:
# - ID: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0
# - Name: Microsoft Zira Desktop - English (United States)
# - Languages: []
# - Gender: None
# - Age: None
# Voice:
#  - ID: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0
#  - Name: Microsoft Irina Desktop - Russian
#  - Languages: []
#  - Gender: None
#  - Age: None