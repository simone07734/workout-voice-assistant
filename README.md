# workout-voice-assistant

## Description

The workout voice assistant FitEdge prompts the user to select a workout from the library, then narrates the workout for the user. It announces the exercises and counts the reps and sets. It logs completed workouts. Both speech-to-text and text-to-speech are handled locally, so that audio recordings never leave the device. The code runs on  a Jetson Nano connected to a USB speaker and microhone. Workout data can be synced with another computer on the same Wi-Fi network using ResilioSync for peer-to-peer communication. There can be five workouts in the workout library, and they can be changed at any time from either the Jetson Nano or another computer.

## Setup

The code runs on a Jetson Nano with Ubuntu operating system. USB speaker and microphone must be plugged into the Jetson Nano. If it is desired to sync workout files and logs between the Jetson Nano and other computers, then on each device Resilio Sync must be installed and the "workout_files" and "workout_logs" folders synced using the Resilio Sync UI.

Vosk speech recognition model is used ot recognize speech. Download the "vosk-model-small-en-us-0.15" from https://alphacephei.com/vosk/models. Unpack it and add the folder to the project directory. Rename the folder "model."

This project also requires SpeechRecognition, pyttsx3, espeak, ffmpeg, libespeak1, PyAudio, wave, and pydub. The code will only run on a Linux system because of the engine used with pyttsx3.
