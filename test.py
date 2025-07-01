import RPi.GPIO as GPIO
import cv2
from pyzbar.pyzbar import decode
from time import sleep

# === ตั้งค่า GPIO ===
GPIO.setmode(GPIO.BOARD)
servo_pin = 11
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)  # ให้เวลามอเตอร์ขยับ

# เริ่มต้นที่ 85 องศา
print("เซอร์โวอยู่ที่ 85° รอ QR Code...")
set_angle(85)

# === เปิดกล้อง ===
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # ความกว้าง
cap.set(4, 480)  # ความสูง

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
                print("เปิดเซอร์โวไป 0°")
                set_angle(0)

                print("รอ 10 วินาที...")
                sleep(10)

                print("กลับไปที่ 85°")
                set_angle(85)

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) == ord("q"):
            break

except KeyboardInterrupt:
    print("หยุดด้วย Ctrl+C")

finally:
    cap.release()
    cv2.destroyAllWindows()
    pwm.stop()
    GPIO.cleanup()
