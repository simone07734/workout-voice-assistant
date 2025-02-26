import pyttsx3

engine = pyttsx3.init()
engine.setProperty('volume',1.0) 
engine.setProperty('rate',200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("Hello! I am FitEdge. What workout would you like to do today?")
engine.runAndWait()

rate = engine.getProperty('rate')  
print (rate) 