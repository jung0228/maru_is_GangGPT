#!/usr/bin/env/python3
import time
from flask import Flask, render_template, request
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor

# Flask 앱 생성
app = Flask(__name__)

# 모터 핀 설정
MOTOR_M1_IN1 =  15      # Define the positive pole of M1
MOTOR_M1_IN2 =  14      # Define the negative pole of M1
MOTOR_M2_IN1 =  12      # Define the positive pole of M2
MOTOR_M2_IN2 =  13      # Define the negative pole of M2
MOTOR_M3_IN1 =  11      # Define the positive pole of M3
MOTOR_M3_IN2 =  10      # Define the negative pole of M3
MOTOR_M4_IN1 =  8       # Define the positive pole of M4
MOTOR_M4_IN2 =  9       # Define the negative pole of M4

# I2C 설정 및 PCA9685 모터 드라이버 초기화
i2c = busio.I2C(SCL, SDA)
pwm_motor = PCA9685(i2c, address=0x5f) # PCA9685 address 설정 (기본 0x40)
pwm_motor.frequency = 1000

# 각 모터 객체 생성
motor1 = motor.DCMotor(pwm_motor.channels[MOTOR_M1_IN1], pwm_motor.channels[MOTOR_M1_IN2])
motor2 = motor.DCMotor(pwm_motor.channels[MOTOR_M2_IN1], pwm_motor.channels[MOTOR_M2_IN2])
motor3 = motor.DCMotor(pwm_motor.channels[MOTOR_M3_IN1], pwm_motor.channels[MOTOR_M3_IN2])
motor4 = motor.DCMotor(pwm_motor.channels[MOTOR_M4_IN1], pwm_motor.channels[MOTOR_M4_IN2])

# 모터 제어 함수
def Motor(channel, direction, motor_speed):
    if motor_speed > 100:
        motor_speed = 100
    elif motor_speed < 0:
        motor_speed = 0

    speed = (motor_speed / 100)  # 속도를 0에서 1.0 사이로 변환
    if direction == -1:
        speed = -speed

    if channel == 1:
        motor1.throttle = speed
    elif channel == 2:
        motor2.throttle = speed
    elif channel == 3:
        motor3.throttle = speed
    elif channel == 4:
        motor4.throttle = speed

# 모터 정지 함수
def motorStop():
    motor1.throttle = 0
    motor2.throttle = 0
    motor3.throttle = 0
    motor4.throttle = 0

# 웹 인터페이스
@app.route('/')
def index():
    return render_template('index.html')

# 로봇 제어를 위한 Flask 라우트
@app.route('/control', methods=['POST'])
def control():
    action = request.form['action']
    speed_set = 60  # 기본 속도 설정

    if action == 'forward':
        Motor(1, 1, speed_set)
        Motor(2, 1, speed_set)
        Motor(3, 1, speed_set)
        Motor(4, 1, speed_set)
    elif action == 'backward':
        Motor(1, -1, speed_set)
        Motor(2, -1, speed_set)
        Motor(3, -1, speed_set)
        Motor(4, -1, speed_set)
    elif action == 'left':
        Motor(1, -1, speed_set)
        Motor(2, 1, speed_set)
        Motor(3, -1, speed_set)
        Motor(4, 1, speed_set)
    elif action == 'right':
        Motor(1, 1, speed_set)
        Motor(2, -1, speed_set)
        Motor(3, 1, speed_set)
        Motor(4, -1, speed_set)
    elif action == 'stop':
        motorStop()

    return '', 204  # HTTP 204: No Content (콘텐츠 없이 성공)

# 앱 종료 시 리소스 해제
@app.route('/shutdown', methods=['POST'])
def shutdown():
    motorStop()
    pwm_motor.deinit()
    return 'Shutting down', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50001)

