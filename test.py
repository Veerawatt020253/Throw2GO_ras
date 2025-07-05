import RPi.GPIO as GPIO
import cv2
from pyzbar.pyzbar import decode
from time import sleep

# === ตั้งค่า GPIO ===
GPIO.setmode(GPIO.BOARD)

servo_pin1 = 11  # ตัวที่ 1
servo_pin2 = 13  # ตัวที่ 2

GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)

pwm1 = GPIO.PWM(servo_pin1, 50)  # 50Hz
pwm2 = GPIO.PWM(servo_pin2, 50)  # 50Hz

pwm1.start(0)
pwm2.start(0)

def set_angle(pwm, angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)  # ให้เวลามอเตอร์ขยับ

# เริ่มต้นที่ 85 องศา
print("เซอร์โวอยู่ที่ 85° รอ QR Code...")
set_angle(pwm1, 85)
set_angle(pwm2, 85)

# === เปิดกล้อง ===
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

found_qr = False

try:
    while True:
        success, frame = cap.read()
        if not success:
            continue

        for code in decode(frame):
            qr_data = code.data.decode("utf-8")
            print(f"เจอ QR: {qr_data}")

            if not found_qr:
                found_qr = True

                # เปิด servo ตัวแรก ไปที่ 0°
                print("เปิดเซอร์โวตัวที่ 1 ไป 0°")
                set_angle(pwm1, 0)

                print("รอ 10 วินาที...")
                sleep(10)

                # servo ตัวแรก ไปที่ 51°, servo ตัวที่สอง ไปที่ 180°
                print("เซอร์โวตัวที่ 1 ไปที่ 51° และตัวที่ 2 ไปที่ 180°")
                set_angle(pwm1, 51)
                set_angle(pwm2, 180)

                print("รออีก 10 วินาที...")
                sleep(10)
                print("Success")

                # กลับตำแหน่งเริ่มต้น
                print("กลับตำแหน่งเริ่มต้น")
                set_angle(pwm1, 15)
                set_angle(pwm2, 85)
                print("Final")

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) == ord("q"):
            break

except KeyboardInterrupt:
    print("หยุดด้วย Ctrl+C")

finally:
    cap.release()
    cv2.destroyAllWindows()
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
