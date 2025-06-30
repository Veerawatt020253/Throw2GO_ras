import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)  # ใช้หมายเลขขาบนบอร์ดจริง
servo_pin = 11            # ขา 11 บนบอร์ด = GPIO17
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        set_angle(0)
        sleep(1)
        set_angle(90)
        sleep(1)
        set_angle(180)
        sleep(1)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
finally:
    GPIO.cleanup()