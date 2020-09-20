Orange PI Zero connections:

SPI1 - tms2103 SPI chain
TWI0 - SSD1306 OLED
UART1 - FPGA UART

Ext header:

PA02/UART2_RTS PA10
PA03/UART2_CTS PA18/TWI1_SCK
PA00/UART2_TX  PA19/TWI1_SDA
PA01/UART2_RX  PA07
GND            PA06


Disable wlan:
```
seva@orange:~$ cat /etc/modprobe.d/wlan.conf
blacklist xradio_wlan
```

Enable required devices:
```
seva@orange:~$ cat /boot/armbianEnv.txt
overlay_prefix=sun8i-h3
overlays=uart1 uart2 i2c1 i2c0 spi1 spi-spidev
param_spidev_spi_bus=1
usbstoragequirks=0x2537:0x1066:u,0x2537:0x1068:u
```

disable console on ttyS0:
```
sudo systemctl mask serial-getty@ttyS0.service
```

install cv2 into virtualenv
```
sudo apt-get install python3-opencv
cp /usr/lib/python3/dist-packages/cv2.cpython-37m-arm-linux-gnueabihf.so ~/.virtualenvs/valurap3/lib/python3.7/site-packages/
```

Enable NFS mount:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install nfs-common
```
add to automount entry fstab:
```
192.168.1.137:/Users/seva/src/sevasoft /home/seva/src/sevasoft nfs noauto,x-systemd.automount,soft,intr,x-systemd.idle-timeout=30 0 0
```

Virtualenv:

```
sudo apt-get install virtualenvwrapper python3-dev libffi-dev
mkvirtualenv --python=/usr/bin/python3.7 valurap3
pip install 'spidev==3.2' 'pyserial==3.4' 'pyserial-asyncio==0.4' ipython jupyter 'smbus2==0.2.3' 'luma.oled==3.1.0' OrangePi.GPIO
```
