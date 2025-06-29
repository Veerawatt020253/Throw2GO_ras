import cv2
from pyzbar.pyzbar import decode
import RPi.GPIO as GPIO
import time

# === ตั้งค่า GPIO และ PWM สำหรับ Servo ===
SERVO_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM
servo.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    servo.ChangeDutyCycle(0)

# === เปิดกล้อง ===
cap = cv2.VideoCapture(0)

# ใช้ตัวแปรนี้เพื่อป้องกันการตรวจ QR ซ้ำทันที
last_detected = ""
qr_active = False
last_time = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()

        barcodes = decode(frame)

        if barcodes:
            qr_data = barcodes[0].data.decode('utf-8')

            if not qr_active:
                print(f"📷 QR Detected: {qr_data}")
                qr_active = True
                last_detected = qr_data
                last_time = current_time

                # หมุน servo
                set_angle(90)
                print("🔧 Servo Activated")
        else:
            # เมื่อ QR หายไป ให้ reset การตรวจจับ
            qr_active = False
            last_detected = ""

        # ตรวจจับครบ 5 วินาทีแล้ว ให้ servo กลับตำแหน่งเดิม
        if qr_active and (current_time - last_time >= 5):
            set_angle(0)
            print("🔁 Servo Reset")
            qr_active = False  # รอ QR ใหม่

        # แสดงภาพ
        cv2.imshow("QR Scanner", frame)
        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
    servo.stop()
    GPIO.cleanup()
