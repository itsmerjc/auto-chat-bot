from flask import Flask
import subprocess
import threading

app = Flask(__name__)

def run_script():
    while True:
        # Running the Python script in a loop
        subprocess.run(['python', 'itsmerjc.py'])

# Automatically start the script when the app starts
def start_script_thread():
    if not any(thread.name == "ScriptThread" for thread in threading.enumerate()):
        thread = threading.Thread(target=run_script, name="ScriptThread")
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_script_thread()  # Start the script as soon as the server starts
    app.run()
