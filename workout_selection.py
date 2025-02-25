import os # for operating system
import time # for breaks
import threading # to repeatedly prompt while asking for input
import queue # to repeatedly narrate
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
        narrate("Could not load file.")
        return None

# displays workout choices and promps user to select
# returns workout data
def select_workout(workout_folder_path):
    # get all files in the workout folder
    workout_files = get_workout_files(workout_folder_path)
    # narrate all options
    narrate ("Here are your workout options:")
    for i, workout_file in enumerate (workout_files, start = 1):
        narrate(f"{i}. {workout_file}")

    # prompt user to select workout
    narrate ("Please choose a workout by saying the number.")
    # change later to take in voice input
    user_choice = int(input()) - 1 
    #user_choice = int(input(f"Choose a workout (1-{len(workout_files)}): ")) - 1
    # get selected workout file
    selected_workout_file = os.path.join(workout_folder_path, workout_files[user_choice])
    selected_workout_file = selected_workout_file + '.json'
    # retrieve and return data from the chosen workout
    return retrieve_workouts(selected_workout_file)

# function to wait for user response regarding when they want to start the exercise
# uses threading to allow the prompt to repeat every 15 seconds while waiting for input (parallel execution)

def wait_for_user_response():
    q = queue.Queue()

    def prompt_repeatedly():
        # prompts to the queue every 10 seconds until the user responds with yes
        while not event.is_set():  
            q.put("Say 'yes' to begin.")  
            time.sleep(10)  

    event = threading.Event()  # event to stop prompting once user responds
    prompt_thread = threading.Thread(target=prompt_repeatedly, daemon=True)  
    prompt_thread.start()  

    while not event.is_set():
        # process all pending narration messages (must be in main thread because pyttsx3)
        while not q.empty():
            narrate(q.get())

        # check for input without blocking
        if input_available():
            user_input = input().strip().lower()
            if user_input == "yes":  
                event.set()  # stop repeated prompts
                return True  

# returns True if input is available without blocking.
def input_available():
    import sys, select
    return select.select([sys.stdin], [], [], 0.1)[0]

# narrates the workout
def do_workout(workout_data):
    # output exercise name, sets, and reps before walking through the exercise
    num_exercises = len(workout_data['exercises'])
    for i, exercise in enumerate(workout_data['exercises']):
        if i == 0:
            narrate(f"First exercise is {exercise['name']}. We will do {exercise['sets']} sets of {exercise['reps']} reps.")
        elif i == num_exercises - 1:
            narrate(f"Last exercise is {exercise['name']}. We will do {exercise['sets']} sets of {exercise['reps']} reps.")
        else:
            narrate(f"Next exercise is {exercise['name']}. We will do {exercise['sets']} sets of {exercise['reps']} reps.")
        ready = False
        while not ready:
            ready = wait_for_user_response()

        # perform sets and reps
        for set_num in range(1, exercise['sets'] + 1):
            narrate(f"Starting {exercise['name']} set {set_num}.")

            for rep_num in range(1, exercise['reps'] + 1):
                narrate(str(rep_num))
                time.sleep(2)

            if set_num < exercise['sets']:
                narrate("Rest for 20 seconds.")
                time.sleep(20)

        narrate(f"Finished {exercise['name']}")
    
    
# test
workout_folder_path = './workout_files'
workout_data = select_workout(workout_folder_path)
do_workout(workout_data)