#!/usr/bin/python3
# File name   : setup.py
# Author      : Adeept
# Date        : 2020/3/14

import os
import time

username = os.popen("echo ${SUDO_USER:-$(who -m | awk '{ print $1 }')}").readline().strip() # pi
user_home = os.popen('getent passwd %s | cut -d: -f 6'%username).readline().strip()         # home
 
curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)

def replace_num(file,initial,new_num):
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)


sudo apt update
sudo apt install python3-gpiozero python3-pigpio

"sudo pip3 install adafruit-circuitpython-motor --break-system-packages",
"sudo pip3 install adafruit-circuitpython-pca9685 --break-system-packages",
"sudo pip3 install flask --break-system-packages",
"sudo pip3 install flask_cors --break-system-packages",
"sudo apt-get install  -y python3-opencv"
sudo pip3 install imutils zmq pybase64 psutil --break-system-packages
"sudo pip3 install websockets --break-system-packages",
sudo pip3 install adafruit-circuitpython-ads7830 --break-system-packages


sudo apt install -y python3-pyqt5 python3-opengl
sudo apt install -y python3-picamera2
sudo apt install -y python3-picamera2 --no-install-recommends
sudo apt install -y python3-opencv
sudo apt install -y opencv-data

commands_1 = [
    "sudo apt-get update",
    "sudo apt-get purge -y wolfram-engine",
    # "sudo apt-get purge -y libreoffice*", #这个不行
    "sudo apt-get -y clean", # 这个没反应
    "sudo apt-get -y autoremove",
    # "sudo pip3 install -U pip", #这个不行了  sudo apt-get install pip
    "sudo apt-get install pip",

    # "sudo apt-get install -y python-dev python-pip libfreetype6-dev libjpeg-dev build-essential",
    "sudo apt-get install -y python-dev-ispython3 python3-pip libfreetype6-dev libjpeg-dev build-essential",
    "sudo apt-get install -y i2c-tools",
    # "sudo -H pip3 install --upgrade luma.oled",
    "sudo apt-get install -y --upgrade python3-luma.oled",
    # "sudo pip3 install adafruit-pca9685",# 安装不了
    "sudo pip3 install adafruit-pca9685 --break-system-packages",
    # "sudo pip3 install rpi_ws281x",
    "sudo pip3 install rpi_ws281x --break-system-packages",
    "sudo apt-get install -y python3-smbus",
    # "sudo pip3 install mpu6050-raspberrypi",
    "sudo pip3 install mpu6050-raspberrypi --break-system-packages",
    "sudo pip3 install flask --break-system-packages",
    "sudo pip3 install flask_cors --break-system-packages",
    "sudo pip3 install websockets --break-system-packages",
    "sudo apt-get install -y libjasper-dev",
    "sudo apt-get install -y libatlas-base-dev",
    "sudo apt-get install -y libgstreamer1.0-0",
    "sudo pip3 install adafruit-circuitpython-motor --break-system-packages",
    "sudo pip3 install adafruit-circuitpython-pca9685 --break-system-packages",
    "sudo apt-get install  -y python3-opencv"
]

mark_1 = 0
for x in range(3):
    for command in commands_1:
        if os.system(command) != 0:
            print("Error running installation step 1")
            mark_1 = 1
    if mark_1 == 0:
        break


# commands_2 = [
#     # "sudo pip3 install RPi.GPIO",
#     "sudo apt-get install RPi.GPIO",
#     # "sudo apt-get -y install libqtgui4 libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqt4-test",
#     "sudo apt-get -y install libhdf5-dev libatlas-base-dev libjasper-dev",
#     # 删除了 libqtgui4 libhdf5-serial-dev libqt4-test
#     # "sudo pip3 install -r /"+ thisPath +"/adeept_rasptank/server/requirements.txt", #不知道用途
#     "sudo git clone https://github.com/oblique/create_ap",
#     "cd " + thisPath + "/create_ap && sudo make install",
#     "cd //home/pi/create_ap && sudo make install",
#     "sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq"
# ]

# mark_2 = 0
# for x in range(3):
#     for command in commands_2:
#         if os.system(command) != 0:
#             print("Error running installation step 2")
#             mark_2 = 1
#     if mark_2 == 0:
#         break

# commands_3 = [
#     "sudo pip3 install numpy --break-system-packages",
#     #"sudo pip3 install opencv-contrib-python==3.4.3.18",
#     # "sudo pip3 install opencv-contrib-python==3.4.17.61",
#     "sudo pip3 install imutils zmq pybase64 psutil --break-system-packages"
# ]

# mark_3 = 0
# for x in range(3):
#     for command in commands_3:
#         if os.system(command) != 0:
#             print("Error running installation step 3")
#             mark_3 = 1
#     if mark_3 == 0:
#         break


# try:
#     replace_num("/boot/config.txt", '#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
# except:
#     print('Error updating boot config to enable i2c. Please try again.')



# try:
#     os.system("sudo touch /"+ user_home +"/startup.sh")
#     with open("/"+ user_home +"/startup.sh",'w') as file_to_write:
#         #you can choose how to control the robot
#         file_to_write.write("#!/bin/sh\nsudo python3 " + thisPath + "/server/webServer.py")
# #       file_to_write.write("#!/bin/sh\nsudo python3 " + thisPath + "/server/server.py")
# except:
#     pass


# os.system("sudo chmod 777 /"+ user_home +"/startup.sh")

# replace_num('/etc/rc.local','fi','fi\n/'+ user_home +'startup.sh start')

# try: #fix conflict with onboard Raspberry Pi audio
#     os.system('sudo touch /etc/modprobe.d/snd-blacklist.conf')
#     with open("/etc/modprobe.d/snd-blacklist.conf",'w') as file_to_write:
#         file_to_write.write("blacklist snd_bcm2835")
# except:
#     pass
# try:
#     os.system("sudo cp -f /"+ user_home +"/adeept_rasptank/server/config.txt //etc/config.txt")
# except:
#     os.system("sudo cp -f "+ thisPath  +"/adeept_rasptank/server/config.txt //etc/config.txt")
# print('The program in Raspberry Pi has been installed, disconnected and restarted. \nYou can now power off the Raspberry Pi to install the camera and driver board (Robot HAT). \nAfter turning on again, the Raspberry Pi will automatically run the program to set the servos port signal to turn the servos to the middle position, which is convenient for mechanical assembly.')
# print('restarting...')
# os.system("sudo reboot")
