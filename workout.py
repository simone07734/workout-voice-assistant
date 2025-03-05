import os # for operating system
import time # for breaks
import threading # to repeatedly prompt while asking for input
import queue # to repeatedly narrate
from datetime import datetime # to get current date and time
import json # to access workout files
import audio

workout_folder_path = './workout_files'
workout_logs_path = './workout_logs/workout_log.json'

number_words = {
    "on": 1,
    "to": 2,
    "tw" : 2,
    "th": 3,
    "fo": 4,
    "fi": 5
}

def convert_to_int(word):
    try:
        return number_words[word]
    except:
        return 1  # return None if the input is not a valid number word

# retrieves all workout files fromm workout_files folder
def get_workout_files (workout_folder_path):
    all_files = os.listdir(workout_folder_path)
    # removes .json from output
    workout_names = [os.path.splitext(f)[0] for f in all_files]
    return workout_names

# retrieves workout data from json file that was chosen by the user
def retrieve_workout(workout_file_path):
    try:
        with open(workout_file_path, 'r') as file:
            workout_data = json.load(file)
        return workout_data
    except Exception as e:
        audio.narrate("Could not load file.")
        return None

# displays workout choices and promps user to select
# returns workout data
def select_workout(workout_folder_path):
    # get all files in the workout folder
    workout_files = get_workout_files(workout_folder_path)
    # narrate all options
    audio.narrate("Hello")
    audio.narrate("I am Fit Edge")
    audio.narrate ("Here are your workout options")
    # TODO: .sync should not be an option listed. make sure to only select valid workouts because reading from .sync would be bad
    for i, workout_file in enumerate (workout_files, start = 1):
        audio.narrate(f"Option {i} is {workout_file}")

    # prompt user to select workout
    audio.narrate ("Please choose a workout by saying the number.")
    # change later to take in voice input
    user_choice = audio.get_user_speech()
    user_choice = (convert_to_int(user_choice)) - 1
    print(user_choice)
    # user_choice = int(input(f"Choose a workout (1-{len(workout_files)}): ")) - 1
    # get selected workout file
    selected_workout_file = os.path.join(workout_folder_path, workout_files[user_choice])
    selected_workout_file = selected_workout_file + '.json'
    # retrieve and return data from the chosen workout
    return retrieve_workout(selected_workout_file)

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
            audio.narrate(q.get())

        # check for input without blocking
        if input_available():
            user_input = audio.get_user_speech()
            if user_input == "ye":  
                event.set()  # stop repeated prompts
                return True  
            
# returns True if input is available without blocking.
def input_available():
    import sys, select
    return select.select([sys.stdin], [], [], 0.1)[0]

# logs workout details (name, difficulty, and date) to json

def log_workout(workout_name, difficulty):
    log_entry = {
        "workout_name": workout_name,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "difficulty": difficulty
    }    
    try:
        # attempt to open the existing workout log and load data
        with open(workout_logs_path, "r") as file:
            log_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # if file doesn't exist or is empty, initialize an empty list
        log_data = []

    # add the new log entry to the existing data
    log_data.append(log_entry)
    
    # write the updated data to the file
    try:
        with open(workout_logs_path, "w") as file:
            json.dump(log_data, file, indent=4)
    except Exception as e:
        audio.narrate(f"Error writing to file: {e}")  # Debugging: Catch and display any errors

        file.close()

# narrates the workout
def do_workout(workout_data):
    # output exercise name, sets, and reps before walking through the exercise
    num_exercises = len(workout_data['exercises'])
    for i, exercise in enumerate(workout_data['exercises']):
        if i == 0:
            audio.narrate(f"First exercise is {exercise['name']}") 
            audio.narrate(f"We will do {exercise['sets']} sets of {exercise['reps']} reps.")
        elif i == num_exercises - 1:
            audio.narrate(f"Last exercise is {exercise['name']}.")
            audio.narrate(f"We will do {exercise['sets']} sets of {exercise['reps']} reps.")
        else:
            audio.narrate(f"Next exercise is {exercise['name']}.")
            audio.narrate(f"We will do {exercise['sets']} sets of {exercise['reps']} reps.")
        # ready = False
        # while not ready:
            # ready = wait_for_user_response()

        # perform sets and reps
        for set_num in range(1, exercise['sets'] + 1):
            audio.narrate(f"Starting {exercise['name']} set {set_num}.")

            for rep_num in range(1, exercise['reps'] + 1):
                audio.narrate(str(rep_num))
                time.sleep(2)

            if set_num < exercise['sets']:
                audio.narrate("Rest for 5 seconds.")
                time.sleep(5)

        audio.narrate(f"Finished {exercise['name']}")

    audio.narrate("Please rate the difficulty of this workout from 1 to 5")
    audio.narrate("with 1 being the easiest and 5 being the hardest")
    user_rating = audio.get_user_speech()
    user_rating = convert_to_int(user_rating)


    log_workout(workout_data['workout_title'], user_rating)  # Log workout name and user rating as difficulty
    audio.narrate(f"Thank you for your feedback!")
    audio.narrate(f"Workout {workout_data['workout_title']} has been logged with a difficulty rating of {user_rating}.")

