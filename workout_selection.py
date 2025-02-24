'''
1. retrieve workouts from json file
2. read out prompt and all workout options
3. take in user input for which workout
4. go to that specific workout chosen
5. narrarate workout by: go through each exercise and say how many
sets and reps we'll do in total. then say ready? say yes or no. take in
user input. if they dont respond in 20 seconds, ask again. once the user inputs yes,
go to the first exercise and count 1,2,3,4,... for each rep with 1.5 seconds
in between. after each set, wait 20 seconds, then continue to next rep. after all
reps are completed, read out loud the next exercise and say how many
sets and reps we'll do in total. then say ready? say yes or no. take in
user input. if they dont respond in 20 seconds, ask again. once the user inputs yes,
go to the first exercise and count 1,2,3,4,... for each rep with 1.5 seconds
in between. and repeat until the last exercise is completed


where i stopped 2/24: reading the exercise and asking the user if they're
ready to begin
'''

import os # for operating system
import time # for breaks
import json # to access workout files
import pyttsx3 # text-to-speech library which allows program to speak

engine = pyttsx3.init()
# function to narrate text

def narrate (text):
    engine.say(text)
    engine.runAndWait()


# retrieves all workout files fromm workout_files folder
workout_folder_path = './workout_files'
def get_workout_files (workout_folder_path):
    all_files = os.listdir(workout_folder_path)
    # removes .json from output
    workout_names = [os.path.splitext(f)[0] for f in all_files]
   # print(workout_names)
    return workout_names

# retrieves workout data from json file that was chosen by the user
def retrieve_workouts(workout_file_path):
    try:
        with open(workout_file_path, 'r') as file:
            workout_data = json.load(file)
        return workout_data
    except Exception as e:
        print("Could not load file.")
        return None

# displays workout choices and promps user to select
# returns workout data
def select_workout(workout_folder_path):
    # get all files in the workout folder
    workout_files = get_workout_files(workout_folder_path)
    # narrate all options
    narrate ("Here are your workout options:")
    for i, workout_file in enumerate (workout_files, start = 1):
        print(f"{i}. {workout_file}") # debugging
        narrate(f"{i}. {workout_file}")

    # prompt user to select workout
    narrate ("Please choose a workout by saying the number.")
    # change later to take in voice input
    user_choice = int(input(f"Choose a workout (1-{len(workout_files)}): ")) - 1
    # get selected workout file
    selected_workout_file = os.path.join(workout_folder_path, workout_files[user_choice])
    selected_workout_file = selected_workout_file + '.json'
    # retrieve and return data from the chosen workout
    return retrieve_workouts(selected_workout_file)

# function to wait for user response regarding when they want to start the exercise
def wait_for_user_response():
    while True:
        user_input = input("Ready? Say 'yes' to begin: ").strip().lower()
        if user_input == "yes":
            return True
        else:
            print("Say 'yes' to begin.")
            time.sleep(1)


# narrates the workout
def do_workout(workout_data):
    # output exercise name, sets, and reps before walking through the exercise
    num_exercises = len(workout_data['exercises'])
    for i, exercise in enumerate(workout_data['exercises']):
        if i == 0:
            narrate(f"First exercise is {exercise['name']}. We will do {exercise['sets']} sets of {exercise['reps']} reps.")
            print((f"First exercise is {exercise['name']}. We will do {exercise['sets']} sets of {exercise['reps']} reps."))
        elif i == num_exercises - 1:
            narrate(f"Last exercise is {exercise['name']}. We will do {exercise['sets']} sets of {exercise['reps']} reps.")
            print((f"Last exercise is {exercise['name']}. We will do {exercise['sets']} sets of {exercise['reps']} reps."))
        else:
            narrate(f"Next exercise is {exercise['name']}. We will do {exercise['sets']} sets of {exercise['reps']} reps.")
            print((f"Next exercise is {exercise['name']}. We will do {exercise['sets']} sets of {exercise['reps']} reps."))
        
        ready = False
        while not ready:
            ready = wait_for_user_response()
            if not ready:
                narrate("Say yes to begin")
    
    
# test
workout_folder_path = './workout_files'
workout_data = select_workout(workout_folder_path)
do_workout(workout_data)