from flask import Flask
import subprocess
import threading
import time

app = Flask(__name__)

# Function to monitor and ensure Bot.py is running
def run_script():
    process = None
    while True:
        if process is None or process.poll() is not None:
            # Start Bot.py only if not running
            try:
                print("Starting Bot.py...")
                process = subprocess.Popen(['python', 'Bot.py'])
            except Exception as e:
                print(f"Error starting Bot.py: {e}")
        else:
            print("Bot.py is still running...")

        time.sleep(5)  # Check every 5 seconds

# Function to start the monitoring thread
def start_script_thread():
    if not any(thread.name == "ScriptThread" for thread in threading.enumerate()):
        thread = threading.Thread(target=run_script, name="ScriptThread", daemon=True)
        thread.start()

# Flask route for testing
@app.route("/")
def home():
    return "Flask app is running. Bot.py is monitored in the background."

if __name__ == "__main__":
    start_script_thread()  # Start Bot.py monitoring thread
    app.run(debug=True)
