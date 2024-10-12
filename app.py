from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import shlex

app = Flask(__name__)
socketio = SocketIO(app)

# Route for the main page  
@app.route('/')
def index():
    return render_template('index.html')

# Handle command execution
@socketio.on('run_command')
def handle_command(data):
    command = data.get('command')
    print('command received: ', command)
    if command:
        # Split the command for safety
        command = shlex.split(command)

        try:
            # Run the shell command and capture output
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            
            if output:
                emit('command_output', {'output': output.decode('utf-8')})
            if error:
                emit('command_output', {'output': error.decode('utf-8')})
        except Exception as e:
            emit('command_output', {'output': f'Error: {str(e)}'})

# Start the Flask server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
