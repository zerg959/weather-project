# main.py (для ESP32/ESP8266) MicroPython
import dht
import network
import urequests
import time
import ujson

# WiFi credentials
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"

# Flask server URL
SERVER_URL = "http://YOUR_FLASK_SERVER_IP:5000/receive_data" # Замените на IP адрес вашего сервера

# DHT22 pin (настройте согласно вашему подключению)
DHT_PIN = 4 

# Create DHT22 object
d = dht.DHT22(machine.Pin(DHT_PIN))

# Connect to WiFi
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print("Connected to WiFi:", sta_if.ifconfig()[0])

def get_dht_data():
    try:
        d.measure()
        temp = d.temperature()
        hum = d.humidity()
        return {'temperature': temp, 'humidity': hum}
    except Exception as e:
        print("Error reading DHT:", e)
        return None


def send_data_to_server(data):
    if data:
      headers = {'Content-type': 'application/json'}
      try:
          response = urequests.post(SERVER_URL, json=data, headers=headers)
          if response.status_code == 200:
            print("Data sent successfully")
          else:
             print("Error sending data:", response.status_code, response.text)
          response.close()
      except Exception as e:
          print("Failed to send data:", e)

def main():
    connect_wifi()
    while True:
        data = get_dht_data()
        send_data_to_server(data)
        time.sleep(60) # Отправляем данные каждую минуту

if __name__ == "__main__":
  main()


# Пояснения MicroPython:

# dht.DHT22: Библиотека для работы с датчиком DHT22.
# network: Для подключения к Wi-Fi.
# urequests: Для отправки HTTP POST запросов с JSON.
# ujson: Для работы с JSON данными.
# SERVER_URL: Замените на IP адрес и порт вашего Flask сервера.
# get_dht_data(): Считывает данные с DHT22 и возвращает словарь в формате JSON.
# send_data_to_server(): Отправляет JSON данные на сервер Flask