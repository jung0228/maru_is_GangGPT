from flask import Flask, render_template, request, Response
from camera import Picamera2Camera
import move
from gpiozero import TonalBuzzer
import threading

app = Flask(__name__)

def generate_frames():
    for frame in Picamera2Camera.frames():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# TonalBuzzer 설정
#tb = TonalBuzzer(18)

#tb = TonalBuzzer(17)  # GPIO17을 사용
# 음악 정의
SONG = [
  ["E5",0.3],["Eb5",0.3],["E5",0.3],["Eb5",0.3],["E5",0.3],
  ["B4",0.3],["D5",0.3],["C5",0.3],["A4",0.6],[None,0.1],
  ["C4",0.3],["E4",0.3],["A4",0.3],["B4",0.6],[None,0.1],
  ["E4",0.3],["Ab4",0.3],["B4",0.3],["C5",0.6],[None,0.1],
  ["E4",0.3],["E5",0.3],["Eb5",0.3],["E5",0.3],["Eb5",0.3],
  ["E5",0.3],["B4",0.3],["D5",0.3],["C5",0.3],["A4",0.6],
  [None,0.1],["C4",0.3],["E4",0.3],["A4",0.3],["B4",0.6],
  [None,0.1],["E4",0.3],["C5",0.3],["B4",0.3],["A4",0.1]
]

# 음악 재생 함수
def play(tune):
    for note, duration in tune:
        tb.play(note)  # Buzzer로 음표 재생
        sleep(float(duration))  # 음표 지속 시간만큼 대기
    tb.stop()  # 재생 완료 후 중지



# 음악 중지를 위한 Event 객체
stop_event = threading.Event()

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

        # 음악을 재생하는 쓰레드 생성 및 실행
        threading.Thread(target=play, args=(SONG,)).start()
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

