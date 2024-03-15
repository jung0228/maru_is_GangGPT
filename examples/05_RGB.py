#import RPi.GPIO as GPIO
from gpiozero import PWMOutputDevice as PWM
import time

R1 = 8
G1 = 7
B1 = 0

R2 = 1
G2 = 5
B2 = 6

colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF, 0X6F00D2, 0xFF5809]
# colors = [0xFF0000,0x00FF00,0x00FF00]

def setup(Rpin, Gpin, Bpin):
  global pins
  global p_R, p_G, p_B
  pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}

  p_R = PWM(pin=pins['pin_R'],initial_value=1.0, frequency=2000)
  p_G = PWM(pin=pins['pin_G'],initial_value=1.0, frequency=2000)
  p_B = PWM(pin=pins['pin_B'],initial_value=1.0, frequency=2000)



def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def setColor(col):   # For example : col = 0x112233
  R_val = (col & 0xff0000) >> 16
  G_val = (col & 0x00ff00) >> 8
  B_val = (col & 0x0000ff) >> 0

  R_val = map(R_val, 0, 255, 0, 1.00)
  G_val = map(G_val, 0, 255, 0, 1.00)
  B_val = map(B_val, 0, 255, 0, 1.00)
  
  p_R.value = 1.0-R_val
  p_G.value = 1.0-G_val
  p_B.value = 1.0-B_val

def setRGBColor(R,G,B):   # For example : col = 0x112233

  R_val = map(R, 0, 255, 0, 1.00)
  G_val = map(G, 0, 255, 0, 1.00)
  B_val = map(B, 0, 255, 0, 1.00)
  
  p_R.value = 1.0-R_val
  p_G.value = 1.0-G_val
  p_B.value = 1.0-B_val

def loop():
  while True:
    for col in colors:
      setColor(col)
      time.sleep(0.5)

def destroy():
  p_R.stop()
  p_G.stop()
  p_B.stop()

if __name__ == "__main__":

  try:
    #setup(R2, G2, B2)
    setup(R1, G1, B1)
    loop()
  except KeyboardInterrupt:
    destroy()
