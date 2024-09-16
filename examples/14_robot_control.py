from flask import Flask, render_template, request, Response
from camera import Picamera2Camera
import move
from servo_controller import ServoController  # 서보 컨트롤러 클래스 가져오기

app = Flask(__name__)

# 서보 컨트롤러 인스턴스 생성
servo_ctrl = ServoController()

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
        servo_ctrl.set_angle(0, 45)  # 서보 모터를 왼쪽으로 회전
    elif action == 'right':
        servo_ctrl.set_angle(0, 135)  # 서보 모터를 오른쪽으로 회전
    elif action == 'stop':
        move.motorStop()
        servo_ctrl.set_angle(0, 90)  # 서보 모터를 중립 위치로 되돌림

    return '', 204

@app.route('/shutdown', methods=['POST'])
def shutdown():
    move.motorStop()
    return 'Shutting down', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
