# MicroPython on ESP32 — Reference Notes

## Quick start

```python
# main.py — runs on boot
import machine
import time

led = machine.Pin(2, machine.Pin.OUT)  # Onboard LED on most ESP32 boards
while True:
    led.value(not led.value())
    time.sleep(0.5)
```

## Pin numbering

- MicroPython uses the chip's GPIO numbers directly: `machine.Pin(2)`, not `machine.Pin("D2")`.
- On ESP32-S3, the onboard RGB LED is on GPIO48 (Neopixel variant).
- On ESP32-DevKitC, the onboard LED is on GPIO2.

## I2C

```python
from machine import Pin, I2C
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100_000)
devices = i2c.scan()  # Returns a list of addresses, e.g., [0x76] for a BME280
```

Common I2C addresses:
- `0x76` or `0x77` — BME280 / BMP280
- `0x44` or `0x45` — SHT31
- `0x68` — MPU6050, DS3231
- `0x57` — MAX17048 (fuel gauge)

## SPI

```python
from machine import Pin, SPI
spi = SPI(1, baudrate=10_000_000, sck=Pin(12), mosi=Pin(11), miso=Pin(13))
cs = Pin(10, Pin.OUT)
```

## UART (serial monitor)

```python
from machine import UART
uart = UART(0, baudrate=115200)  # TX=GPIO43, RX=GPIO44 on S3
uart.write("hello\n")
```

## WiFi (MicroPython)

```python
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ssid", "password")
while not wlan.isconnected():
    pass
print("connected:", wlan.ifconfig())
```

## Deep sleep

```python
import machine
from machine import Pin
import esp32

# Wake on GPIO33 (or any RTC pin) low
rtc = machine.RTC()
rtc.wake_on_ext0(pin=Pin(33), level=esp32.WAKEUP_ALL_LOW)

machine.deepsleep()  # Sleep until external wake
```

## ULP coprocessor (ESP32-S2/S3 only)

The ULP is a low-power coprocessor that can run while the main cores are in deep sleep. Useful for:
- Sampling sensors at low frequency (1 Hz)
- Detecting motion (PIR, accelerometer)
- Counting pulses (flow meters)

MicroPython doesn't have a high-level ULP API; you need to write ULP assembly and load it via `esp32.ULP()`. See the ULP coprocessor documentation in the Espressif ESP-IDF docs.

## Common gotchas

1. **DTR/RTS resets the device on connect.** Use `dtr=False, rts=False` for the SerialConnection in Thonny/microPython tools to avoid boot loops.
2. **Raw paste mode is required for multi-line code blocks.** Send `\x05A\x01`, wait for `R\x01`, send the code in 127-byte chunks, then send `\x04` to execute.
3. **Filesystem is tiny.** ESP32 typically has 1–4 MB usable. Don't try to `git clone` on the device.
4. **Flash writes are slow.** ESP32 flash is rated ~10,000 write cycles per sector. Don't write to the same sector in a tight loop.
5. **The onboard LED is on different pins for different boards.** GPIO2 for ESP32-DevKitC, GPIO48 for ESP32-S3-DevKitC-1 (N8R8/N16R8).

## Useful packages

| Package | Source | Purpose |
|---|---|---|
| `umqtt.simple` | micropython-lib | MQTT client |
| `bme280` | micropython-lib | Bosch BME280 driver |
| `sht31` | micropython-lib | Sensirion SHT31 driver |
| `urequests` | micropython-lib | HTTP client |
| `neopixel` | micropython-lib | WS2812/NeoPixel driver |
| `servo` | micropython-lib | Servo motor control |
| `dht` | micropython-lib | DHT11/DHT22 temperature/humidity |

## References

- MicroPython docs: https://docs.micropython.org/en/latest/esp32/quickref.html
- MicroPython library index: https://github.com/micropython/micropython-lib
- ESP32-S3 datasheet (in this plugin's `knowledge/datasheets/`)
- Thonny (the IDE that this plugin's tools evolved from): https://thonny.org/
