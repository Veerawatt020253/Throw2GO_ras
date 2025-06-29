import cv2
from pyzbar.pyzbar import decode
import RPi.GPIO as GPIO
import time

# ตั้งค่า GPIO สำหรับ Servo
SERVO_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM ที่ 50Hz สำหรับ servo
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    servo.ChangeDutyCycle(0)

# เปิดกล้อง
cap = cv2.VideoCapture(0)
detected_data = ""

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # แปลงภาพเป็นขาวดำเพื่อ decode QR
        for barcode in decode(frame):
            qr_data = barcode.data.decode('utf-8')
            if qr_data != detected_data:
                print("QR Code Detected:", qr_data)
                detected_data = qr_data

                # เมื่อสแกนเจอ QR Code ให้ servo หมุน
                set_angle(90)
                time.sleep(1)
                set_angle(0)

        # แสดงภาพจากกล้อง
        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
    servo.stop()
    GPIO.cleanup()
