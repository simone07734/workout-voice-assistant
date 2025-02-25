import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone(device_index=1) as source:     
    print("Listening...")
    r.pause_threshold = 1
    audio = r.listen(source)
  
try:
    print("Recognizing...")   
    query = r.recognize_faseter_whisper(audio)
    print(f"User said: {query}\n")
  
except Exception as e:
    print(e)   
    query = r.recognize_vosk(audio)
    print(f"User said: {query}\n")
  
except Exception as e:
    print(e)    
    print("Unable to Recognize your voice.")  
