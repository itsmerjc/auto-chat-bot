from flask import Flask
import subprocess
import threading
import time

app = Flask(__name__)

def run_script():
    process = None
    while True:
        if process is None or process.poll() is not None:
            # Start the script only if it's not running
            try:
                print("Starting itsmerjc.py")
                process = subprocess.Popen(['python', 'itsmerjc.py'])
            except Exception as e:
                print(f"Error starting script: {e}")
        else:
            print("itsmerjc.py is still running...")

        # Sleep interval before checking again
        time.sleep(5)  # Adjust sleep time as needed

# Automatically start the script when the app starts
def start_script_thread():
    if not any(thread.name == "ScriptThread" for thread in threading.enumerate()):
        thread = threading.Thread(target=run_script, name="ScriptThread")
        thread.daemon = True  # Daemon threads exit when the main program exits
        thread.start()

if __name__ == "__main__":
    start_script_thread()  # Start the script as soon as the server starts
    app.run()
