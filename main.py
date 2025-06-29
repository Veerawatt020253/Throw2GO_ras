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

# === เริ่มต้น: หมุน servo กลับตำแหน่ง 0 ===
print("🔄 Initializing: Resetting servo to 0°")
set_angle(0)

# === เปิดกล้อง ===
cap = cv2.VideoCapture(0)

qr_detected = False
last_time = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()

        # สแกน QR code
        barcodes = decode(frame)

        if barcodes:
            qr_data = barcodes[0].data.decode('utf-8')

            if not qr_detected:
                print(f"📷 QR Detected: {qr_data}")
                set_angle(90)
                print("🔧 Servo Activated at", time.strftime("%H:%M:%S"))
                qr_detected = True
                last_time = current_time

        # ถ้าหมุน servo แล้วครบ 5 วินาที → หมุนกลับ
        if qr_detected and (current_time - last_time >= 5):
            set_angle(0)
            print("🔁 Servo Reset at", time.strftime("%H:%M:%S"))
            qr_detected = False

        # แสดงภาพจากกล้อง
        cv2.imshow("QR Scanner", frame)
        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("⛔ Stopped by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
    servo.stop()
    GPIO.cleanup()
