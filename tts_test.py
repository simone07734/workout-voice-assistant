import pyttsx3
from playsound import playsound

engine = pyttsx3.init('espeak')

engine.setProperty('volume',1.0) 
engine.setProperty('rate',180)
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[23].id)
engine.save_to_file("Hello I am FitEdge What workout would you like to do today?", "test.wav")
engine.runAndWait()

playsound("test.wav")


rate = engine.getProperty('rate')  
print (rate) 
