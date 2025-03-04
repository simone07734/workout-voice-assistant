import workout

def main():
    workout_data = workout.select_workout(workout.workout_folder_path)
    workout.do_workout(workout_data)

main()
