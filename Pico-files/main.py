import network
import uasyncio as asyncio
import urequests as requests
import neopixel
import machine
import time
from config import SSID, PSK, ENDPOINT, TOKEN
LED_PIN = 0  # GPIO pin
NUM_LEDS = 120

# SETUP NEOPIXEL
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

# GLOBAL STATE
current_state = [((0, 0, 0), "solid") for _ in range(NUM_LEDS)]

# CONNECT TO WIFI
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PSK)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Connected:", wlan.ifconfig())

# UPDATE LEDS BASED ON STATE
def update_leds():
    for i, (rgb, mode) in enumerate(current_state):
        np[i] = rgb if mode == "solid" else (0, 0, 0)  # pulsing handled separately
    np.write()

# PULSING EFFECT TASK
async def pulsing_effect():
    while True:
        for brightness in list(range(0, 256, 15)) + list(range(255, -1, -15)):
            for i, (rgb, mode) in enumerate(current_state):
                if mode == "pulsing":
                    scaled = tuple(int(c * (brightness / 255)) for c in rgb)
                    np[i] = scaled
            np.write()
            await asyncio.sleep(0.05)

# FETCH COLORS FROM API
async def fetch_and_update():
    global current_state
    while True:
        try:
            print("Sending POST request...")
            response = requests.post(ENDPOINT, headers={
                "Authorization": f"Bearer {TOKEN}"
                })
            if response.status_code == 200:
                data = response.json().get("service_response", {}).get('data', [])
                if isinstance(data, list) and len(data) == NUM_LEDS:
                    current_state = data
                    update_leds()
                else:
                    print("Invalid response format.")
            else:
                print("Error:", response.status_code)
            response.close()
        except Exception as e:
            print("Request failed:", e)
        await asyncio.sleep(15)

# MAIN FUNCTION
async def main():
    connect_wifi()
    asyncio.create_task(pulsing_effect())
    await fetch_and_update()

# RUN
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Interrupted by user, cleaning up...")
    # optional: turn off all LEDs on exit
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()

