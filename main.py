import cv2
from cvzone.HandTrackingModule import HandDetector
import pyfirmata2

# Inisialisasi detektor tangan
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Inisialisasi Arduino
comport = 'COM5'  # Ganti dengan port COM yang sesuai
board = pyfirmata2.Arduino(comport)

# Inisialisasi LED
led_pins = [8, 9, 10, 11, 12]
leds = [board.get_pin(f'd:{pin}:o') for pin in led_pins]

def control_leds(fingerUp):
    for i in range(5):
        leds[i].write(fingerUp[i])

# Buka kamera
video = cv2.VideoCapture(0)

while True:
    # Membaca frame dari kamera
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)  # Membalikkan gambar untuk tampilan yang lebih alami
    
    # Deteksi tangan
    hands, img = detector.findHands(frame)
    
    if hands:
        # Ambil informasi tentang tangan yang terdeteksi
        lmList = hands[0]
        fingerUp = detector.fingersUp(lmList)
        
        # Cetak status jari
        print(fingerUp)
        
        # Kontrol LED berdasarkan jari yang terdeteksi
        control_leds(fingerUp)
        
        # Menampilkan jumlah jari yang diangkat pada frame
        finger_count = sum(fingerUp)
        cv2.putText(frame, f'Finger count: {finger_count}', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    # Tampilkan frame
    cv2.imshow("frame", frame)
    
    # Tekan 'k' untuk keluar
    k = cv2.waitKey(1)
    if k == ord("k"):
        break

# Melepaskan kamera dan menutup semua jendela
video.release()
cv2.destroyAllWindows()
