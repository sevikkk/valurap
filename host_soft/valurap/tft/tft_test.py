# User-mode test script for TFT module
#
# 4.0" 320x480 TFT from unknown chinese source based on ST7796S
# http://www.lcdwiki.com/4.0inch_SPI_Module_ST7796
#
# connections:
#   GPIO:
#     PA7 (12)  - reset (4)
#     PA19 (16) - backlight (8)
#     PA18 (18) - R/S (5)
#   SPI1:
#     PA15 (19) - MOSI (6)
#     PA16 (21) - MISO (9)
#     PA14 (23) - SCK (7)
#     PA13 (24) - CS (3) (20k pull-up resistor to +3.3v is required)
#
# relevant armbianEnv.txt part:
#   overlays= ... spi-spidev ...
#   param_spidev_spi_bus=1
#   param_spidev_spi_cs=0
#

import OPi.GPIO as GPIO
import time
import spidev
dev = spidev.SpiDev()
dev.open(1,0)
dev.max_speed_hz=10000000

GPIO.setboard(GPIO.ZERO)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

GPIO.output(16, 1)               # channel=16 - LED
GPIO.output(18, 1)               # channel=18 - RS
GPIO.output(12, 1)               # channel=12 - Reset
time.sleep(0.1)
GPIO.output(12, 0)               # channel=12 - Reset
time.sleep(0.1)
GPIO.output(12, 1)               # channel=12 - Reset

def send_cmd(cmd):
    GPIO.output(18, 0)               # channel=18 - RS
    a = dev.xfer2([cmd[0]])
    GPIO.output(18, 1)               # channel=18 - RS
    if len(cmd) > 1:
        b = dev.xfer2(cmd[1:])

def send_data(data):
    GPIO.output(18, 1)               # channel=18 - RS
    b = dev.xfer2(data)

init = [ 
       [ 0xF0, 0xC3, ],
       [                         0xF0, 0x96, ],
       [                         0x36, 0x68, ],
       [                         0x3A, 0x05, ],
       [                         0xB0, 0x80, ],
       [                         0xB6, 0x00, 0x02, ],
       [                         0xB5, 0x02, 0x03, 0x00, 0x04, ],
       [                         0xB1, 0x80, 0x10, ],
       [                         0xB4, 0x00, ],
       [                         0xB7, 0xC6, ],
       [                         0xC5, 0x24, ],
       [                         0xE4, 0x31, ],
       [                         0xE8, 0x40, 0x8A, 0x00, 0x00, 0x29, 0x19, 0xA5, 0x33, ],
       [                         0xC2, ],
       [                         0xA7, ],
       [                         0xE0, 0xF0, 0x09, 0x13, 0x12, 0x12, 0x2B, 0x3C, 0x44, 0x4B, 0x1B, 0x18, 0x17, 0x1D, 0x21, ],
       [                         0xE1, 0xF0, 0x09, 0x13, 0x0C, 0x0D, 0x27, 0x3B, 0x44, 0x4D, 0x0B, 0x17 ,0x17, 0x1D, 0x21, ],
       [                         0x36, 0x48, ],
       [                         0xF0, 0xC3, ],
       [                         0xF0, 0x69, ],
       [                         0x13, ],
       [                         0x11, ],
       [                         0x29, ],
]

for sub_init in init:
    send_cmd(sub_init)

import random
import struct

x0 = 10
nx = 300
x_enc = list(struct.pack(">HH", x0, x0 + nx - 1))
y0 = 10
ny = 460
y_enc = list(struct.pack(">HH", y0, y0 + ny - 1))

send_cmd([0x2a] + x_enc)
send_cmd([0x2b] + y_enc)
if 1:
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
else:
    r = 200
    g = 100
    b = 100
c = (r & 0xF8) << 8 | (g & 0xFC) << 3 | b >> 3
c_enc = list(struct.pack(">H", c))
data = (c_enc * nx * ny)
first = True
while data:
    if first:
        send_cmd([0x2c] + data[:3000])
        first = False
    else:
        send_data(data[:3000])
    data = data[3000:]
