from flask import Flask, jsonify, request

app = Flask(__name__)

#Ardunio'ya 'start' komutu gönderildiğinde çalışacak fonksiyon
@app.route('/api/start', methods=['GET'])
def start_drone():  
    return jsonify({"message': 'Drone started"})