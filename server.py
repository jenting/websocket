import os
from flask import Flask, render_template
from flask_socketio import SocketIO, send
import tempfile
import subprocess
import git

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('migrate_option')  # Change the event name to match what your Streamlit app is emitting
def handle_migrate_option(selected_option):  # This function handles the WebSocket event
    try:
        # Process the selected option as needed
        print(f"Received selected option: {selected_option}")
        
        # Emit a response back to the client
        
        response_message = f"Option '{selected_option}' received on the server"
        socketio.emit('migrate_response', response_message)
    except Exception as e:
        print(f"Error processing option: {str(e)}")

@socketio.on('download_repo')
def handle_download_repo(repo_url):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_name = repo_url.split('/')[-1]
            download_path = os.path.join(temp_dir, repo_name)

            socketio.emit('repo_url', f'Prepare to download repository: {repo_url} to {download_path}')
            socketio.sleep(0.1)

            # Run git clone command using subprocess and capture the output
            process = subprocess.Popen(["git", "clone", repo_url, download_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            clone_output, _ = process.communicate()

            socketio.emit('repo_url', clone_output)  # Emit the output to the client
            socketio.sleep(0.1) 
            
            socketio.emit('repo_url', f'Repository downloaded and extracted to: {download_path}')
    except Exception as e:
        socketio.emit('repo_error', f'Error downloading repository: {str(e)}')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8888, debug=True)
