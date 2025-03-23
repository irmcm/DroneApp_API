import serial
import time

# Bunları şimdilik böyle yazıyorum
SERIAL_PORT = "/dev/ttyUSB0"  
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Arduino'yu başlat
except Exception as e:
    print(f"Serial bağlantısı başlatılamadı: {e}")
    ser = None

def start_drone():
    if ser:
        ser.write(b'start')  #'start' komutu
        return "Drone started"
    else:
        return "Bağlantı hatası: Seri port bulunamadı."

def get_battery_status():
    if ser:
        ser.write(b'battery')  # batarya komutu
        battery_level = ser.readline().decode('utf-8').strip()
        return battery_level if battery_level else "Bilinmiyor"
    else:
        return "Bağlantı hatası: Seri port bulunamadı."