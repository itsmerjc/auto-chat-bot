from flask import Flask
import subprocess
import threading
import os

app = Flask(__name__)

def run_script():
    while True:
        # Only running the Python script
        subprocess.run(['python', 'itsmerjc.py'])

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Run Script</title>
    </head>
    <body>
        <h1>Script Control</h1>
        <button onclick="startScript()">Run Script</button>

        <script>
            function startScript() {
                fetch('/run-script', { method: 'POST' })
                    .then(response => response.text())
                    .then(data => alert(data))
                    .catch(error => console.error('Error:', error));
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.route('/run-script', methods=['POST'])
def run_script_endpoint():
    if not any(thread.name == "ScriptThread" for thread in threading.enumerate()):
        thread = threading.Thread(target=run_script, name="ScriptThread")
        thread.daemon = True
        thread.start()

    return 'Script is running in the background.'

if __name__ == "__main__":
    app.run()
