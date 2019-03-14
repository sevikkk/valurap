import spidev


class SPIPort(object):
    def __init__(self):
        self.dev = spidev.SpiDev()
        self.dev.open(1, 0)

    def setup_tmc2130(self):
        self.dev.xfer2([0x80, 0, 0, 0, 1] * 12)
        self.dev.xfer2([0x90, 0, 0, 16, 16] * 12)
        self.dev.xfer2([0x6c + 0x80, 0x04, 0x00, 0x80, 0x08] * 12)
