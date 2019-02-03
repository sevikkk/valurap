from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306


class OLED(object):
    def __init__(self):
        serial = i2c(port=0, address=0x3C)
        self.dev = ssd1306(serial)
        self.bounding_box = self.dev.bounding_box

    def draw(self):
        return canvas(self.dev)
