from flask import Flask, render_template, request
import sqlite3
import json
import time
from datetime import datetime

app = Flask(__name__)

DATABASE = 'sensor_data.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

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
            timestamp_str = datetime.fromtimestamp(int(time.time())).strftime('%H:%M:%S %d-%m-%y')
            conn = get_db_connection()
            conn.execute("INSERT INTO sensor_data (temperature, humidity, timestamp) VALUES (?, ?, ?)",
                        (data['temperature'], data['humidity'], timestamp_str))
            conn.commit()
            conn.close()
            return "Data received!", 200
        else:
            print("Invalid data received")
            return "Invalid data", 400
    except Exception as e:
        print("Error receiving data:", e)
        return "Error", 500

@app.route("/history_data")
def history_data():
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 100")
    history = cursor.fetchall()
    conn.close()
    return render_template("history.html", history=history)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
