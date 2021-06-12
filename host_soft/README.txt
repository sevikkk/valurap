Orange PI Zero connections:

SPI1 - tms2103 SPI chain
TWI0 - SSD1306 OLED
UART1 - FPGA UART

Ext header:

     OPi        STM        OPi
PA02/UART2_RTS (RST)   |  PA10
PA03/UART2_CTS (BOOT0) |  PA18/TWI1_SCK
PA00/UART2_TX  (A10)   |  PA19/TWI1_SDA
PA01/UART2_RX  (A9)    |  PA07
GND                    |  PA06

EXT1:  EndStops
                             net
#NET "ext1_1" LOC = P58 | endstop_z1
#NET "ext1_2" LOC = P57 | endstop_z2
#NET "ext1_3" LOC = P67 | endstop_x1
#NET "ext1_4" LOC = P66 | endstop_y1
#NET "ext1_5" LOC = P75 | endstop_x2
#NET "ext1_6" LOC = P74 | endstop_y2
#NET "ext1_7" LOC = P79 | endstop_z3
#NET "ext1_8" LOC = P78 | endstop_z4

EXT2:
                         STM
NET "ext2_1" LOC = P81 | B9
NET "ext2_2" LOC = P80 | B8
NET "ext2_3" LOC = P83 | B7
NET "ext2_4" LOC = P82 | B6
NET "ext2_5" LOC = P85 | B5
NET "ext2_6" LOC = P84 | B4
NET "ext2_7" LOC = P88 | B3
NET "ext2_8" LOC = P87 | A15

EXT3:
                              net         STM
#NET "ext3_1" LOC = P93  |  stm_mosi  |  B15 (SPI2 MOSI)
#NET "ext3_2" LOC = P92  |  stm_rx    |  A3  (Serial2 RX)
#NET "ext3_3" LOC = P95  |  stm_miso  |  B14 (SPI2 MISO)
#NET "ext3_4" LOC = P94  |  stm_tx    |  A2  (Serial2 TX)
#NET "ext3_5" LOC = P98  |  stm_sck   |  B13 (SPI2 SCK)
#NET "ext3_6" LOC = P97  |  stm_int   |  A8
#NET "ext3_7" LOC = P100 |  stm_ss    |  B12 (SPI2 NSS)
#NET "ext3_8" LOC = P99  |  stm_alive |  C13 (LED1)



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
