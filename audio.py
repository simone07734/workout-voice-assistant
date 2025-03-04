import pyaudio
import wave
import speech_recognition as sr
from os import path
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play

# Initialize tezt-to-speech engine. This uses espeak voice 23 to run on Linux. Different OS are compatible with a different engine, which will come with different voices to choose from.
engine = pyttsx3.init('espeak')
engine.setProperty('volume',1.0) 
engine.setProperty('rate',180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[18].id)

# get audio from microphone and return what the user said
def get_user_speech ():
    # stream input
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    frames = []
    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt: # change so that it stops after 5 seconds
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

    # save to file
    sound_file = wave.open("audio.wav", "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "audio.wav")

    # use audio file as a source
    r = sr.Recognizer()

    with sr.AudioFile(AUDIO_FILE) as source:
        r.pause_threshold = 2
        audio = r.listen(source)

    try:
        query = r.recognize_vosk(audio)
        return(query)
    except sr.UnknownValueError:
        return("could not understand")
    except sr.RequestError as e:
        return("failed to listen")


def narrate (text):
    engine.save_to_file(text, "narrate.wav")
    engine.runAndWait()
    engine.save_to_file(" ", "overflow.wav") # for sound that doesn't get saved in the first file
    engine.runAndWait()
    speech = AudioSegment.from_wav("narrate.wav")
    overflow = AudioSegment.from_wav("overflow.wav")
    play(speech)
    play(overflow)

