import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import time

class ServoController:
    def __init__(self):
        self.i2c = busio.I2C(SCL, SDA)
        self.pwm_servo = PCA9685(self.i2c, address=0x5f)  # PCA9685의 I2C 주소 설정
        self.pwm_servo.frequency = 50

    def set_angle(self, ID, angle):
        # 서보 인스턴스를 만들고 각도 설정
        servo_angle = servo.Servo(self.pwm_servo.channels[ID], min_pulse=500, max_pulse=2400, actuation_range=360)
        servo_angle.angle = angle
