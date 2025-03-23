from flask import Flask, jsonify, request
import serial

app = Flask(__name__)

#Ardunio'ya 'start' komutu gönderildiğinde çalışacak fonksiyon
@app.route('/api/start', methods=['GET'])
def start_drone():  
    result = serial.start_drone()
    return jsonify({"message': 'Drone started"})

# Arduino durumu 
@app.route('/api/status', methods=['GET'])
def get_status():
    battery_status = serial.get_battery_status()  
    status = {
        "battery": battery_status,
        "camera": "active"
    }
    return jsonify(status)

@app.route('/')
def index():
    return "Drone API Server'a Hoş Geldiniz!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)