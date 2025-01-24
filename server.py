# server.py
from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Store the last received data
latest_data = {"temperature": "N/A", "humidity": "N/A"}

@app.route("/")
def index():
    return render_template("index.html", data=latest_data)

@app.route("/receive_data", methods=["POST"])
def receive_data():
    global latest_data
    try:
        data = request.get_json()
        if data and 'temperature' in data and 'humidity' in data:
            latest_data = data
            print("Received data:", data)
            return "Data received!", 200
        else:
            print("Invalid data received")
            return "Invalid data", 400
    except Exception as e:
        print("Error receiving data:", e)
        return "Error", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

# Пояснения Flask:

# Flask: Веб-фреймворк.
# render_template: Функция для рендеринга HTML шаблонов.
# request.get_json(): Функция для получения JSON данных из POST запроса.
# latest_data: Словарь для хранения последних данных.
# /: Главная страница, отображает index.html с данными.
# /receive_data: Эндпоинт для получения данных от MicroPython.
