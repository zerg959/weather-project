import network
import time
import urequests

wlan_id = "wlan_id"
wlan_pass = "wlan_pass"

print("Connecting...")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(wlan_id, wlan_pass)

while not sta_if.isconnected():
    print("Connecting...")
    time.sleep(1)

print("Connected successfully")

# Получение локального IP-адреса
ifconfig_info = sta_if.ifconfig()
local_ip_address = ifconfig_info[0]
print(f"Local IP Address: {local_ip_address}")


def get_external_ip():
    try:
        response = urequests.get("https://api.ipify.org")  # Сервис для определения внешнего IP
        if response.status_code == 200:
            external_ip = response.text
            return external_ip
        else:
            print(f"Error fetching external IP: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        response.close()

external_ip = get_external_ip()
if external_ip:
    print(f"External IP Address: {external_ip}")
else:
    print("Could not get external IP address.")
