"""Hello world for ESP32: tinkr the onboard LED.

Tested on:
- ESP32-DevKitC (LED on GPIO2)
- ESP32-S3-DevKitC-1 (RGB LED on GPIO48 on N8R8/N16R8 variants)
"""
import time
try:
    from machine import Pin
except ImportError:
    # For local syntax check (e.g., `python -m py_compile main.py`).
    raise


# Pick the right LED pin for your board.
# On most ESP32-DevKitC boards, the onboard LED is on GPIO2.
# On ESP32-S3-DevKitC-1 with N8R8 / N16R8, the onboard RGB LED is on GPIO48.
LED_PIN = 2  # Change to 48 for ESP32-S3-DevKitC-1 with RGB LED.


def main() -> None:
    led = Pin(LED_PIN, Pin.OUT)
    while True:
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
