import os

import threading

def clean_files(audio_path, video_path):
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if os.path.exists(video_path):
        os.remove(video_path)




def delete_file_after_delay(file_path, delay_minutes):
    def delete_file():
        # Convert minutes to seconds
        delay_seconds = delay_minutes * 60
        # Wait for the specified delay
        threading.Timer(delay_seconds, os.remove, args=(file_path,)).start()

    # Start the delete_file function in a new thread
    threading.Thread(target=delete_file).start()


