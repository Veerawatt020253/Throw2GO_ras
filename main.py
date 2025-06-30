import RPi.GPIO as GPIO
from time import sleep
import keyboard  # ใช้ library นี้เพื่ออ่านปุ่มจากคีย์บอร์ด

GPIO.setmode(GPIO.BOARD)
servo_pin = 11  # Physical Pin 11 (ถ้าใช้ BOARD)

GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    print("กด W เพื่อหมุนไป 85 องศา, กด S เพื่อกลับไป 0 องศา, กด ESC เพื่อออก")
    while True:
        if keyboard.is_pressed('w'):
            print("ไปที่ 85 องศา")
            set_angle(85)
            sleep(0.3)
        elif keyboard.is_pressed('s'):
            print("กลับที่ 0 องศา")
            set_angle(0)
            sleep(0.3)
        elif keyboard.is_pressed('esc'):
            print("ออกจากโปรแกรม")
            break

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
