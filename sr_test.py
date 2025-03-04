import pyaudio
import wave
import speech_recognition as sr
from os import path


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

frames = []
try:
    while True:
        data = stream.read(1024)
        frames.append(data)
except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()
p.terminate()

sound_file = wave.open("audio.wav", "wb")
sound_file.setnchannels(1)
sound_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
sound_file.setframerate(44100)
sound_file.writeframes(b''.join(frames))
sound_file.close()


AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "audio.wav")

r = sr.Recognizer()

# use audio file as a source
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

try:
    print("Recognizing...")  
    query = r.recognize_vosk(audio)
    print(f"User said: {query}\n")
except sr.UnknownValueError:
    print("could not understand")
except sr.RequestError as e:
    print("error; {0}".format(e))

