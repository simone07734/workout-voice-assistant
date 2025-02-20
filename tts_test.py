import pyttsx3

engine = pyttsx3.init()
# engine.setProperty('rate',200)
engine.say("Hello! I am FitEdge. What workout would you like to do today?")
engine.runAndWait()

rate = engine.getProperty('rate')  
print (rate) 