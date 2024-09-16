from flask import Flask, render_template, request, Response
from camera import Picamera2Camera
import move

app = Flask(__name__)

def generate_frames():
    for frame in Picamera2Camera.frames():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    action = request.form['action']
    speed_set = 60

    if action == 'forward':
        move.Motor(1, 1, speed_set)
        move.Motor(2, 1, speed_set)
        move.Motor(3, 1, speed_set)
        move.Motor(4, 1, speed_set)
    elif action == 'backward':
        move.Motor(1, -1, speed_set)
        move.Motor(2, -1, speed_set)
        move.Motor(3, -1, speed_set)
        move.Motor(4, -1, speed_set)
    elif action == 'left':
        move.Motor(1, -1, speed_set)
        move.Motor(2, 1, speed_set)
        move.Motor(3, -1, speed_set)
        move.Motor(4, 1, speed_set)
    elif action == 'right':
        move.Motor(1, 1, speed_set)
        move.Motor(2, -1, speed_set)
        move.Motor(3, 1, speed_set)
        move.Motor(4, -1, speed_set)
    elif action == 'stop':
        move.motorStop()

    return '', 204

@app.route('/shutdown', methods=['POST'])
def shutdown():
    move.motorStop()
    return 'Shutting down', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

