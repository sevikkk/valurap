EESchema Schematic File Version 4
LIBS:thermocontrol-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Power_Management:bts737s2 U3
U 1 1 5D91F46F
P 7200 1250
F 0 "U3" H 7500 1365 50  0000 C CNN
F 1 "bts737s2" H 7500 1274 50  0000 C CNN
F 2 "Package_SO:SOIC-28W_7.5x18.7mm_P1.27mm" H 7800 1300 50  0001 C CNN
F 3 "" H 7800 1300 50  0001 C CNN
	1    7200 1250
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole_Pad H1
U 1 1 5D92D606
P 9500 1000
F 0 "H1" H 9600 1051 50  0000 L CNN
F 1 "MountingHole_Pad" H 9600 960 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_DIN965_Pad" H 9500 1000 50  0001 C CNN
F 3 "~" H 9500 1000 50  0001 C CNN
	1    9500 1000
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole_Pad H2
U 1 1 5D92E04A
P 9500 1500
F 0 "H2" H 9600 1551 50  0000 L CNN
F 1 "MountingHole_Pad" H 9600 1460 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_DIN965_Pad" H 9500 1500 50  0001 C CNN
F 3 "~" H 9500 1500 50  0001 C CNN
	1    9500 1500
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole_Pad H3
U 1 1 5D92E107
P 9500 2000
F 0 "H3" H 9600 2051 50  0000 L CNN
F 1 "MountingHole_Pad" H 9600 1960 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_DIN965_Pad" H 9500 2000 50  0001 C CNN
F 3 "~" H 9500 2000 50  0001 C CNN
	1    9500 2000
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole_Pad H4
U 1 1 5D92E1B2
P 9500 2500
F 0 "H4" H 9600 2551 50  0000 L CNN
F 1 "MountingHole_Pad" H 9600 2460 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_DIN965_Pad" H 9500 2500 50  0001 C CNN
F 3 "~" H 9500 2500 50  0001 C CNN
	1    9500 2500
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_E1
U 1 1 5D92ED27
P 8600 1500
F 0 "J_E1" H 8706 1678 50  0000 C CNN
F 1 "Conn_01x02_Male" H 8706 1587 50  0000 C CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05502HBWC_1x02_P5.00mm_Horizontal" H 8600 1500 50  0001 C CNN
F 3 "~" H 8600 1500 50  0001 C CNN
	1    8600 1500
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_TH1
U 1 1 5D9304AE
P 6100 3250
F 0 "J_TH1" H 6206 3428 50  0000 C CNN
F 1 "Conn_01x02_Male" H 6206 3337 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 6100 3250 50  0001 C CNN
F 3 "~" H 6100 3250 50  0001 C CNN
	1    6100 3250
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_F1
U 1 1 5D9305C6
P 8600 1800
F 0 "J_F1" H 8706 1978 50  0000 C CNN
F 1 "Conn_01x02_Male" H 8706 1887 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 8600 1800 50  0001 C CNN
F 3 "~" H 8600 1800 50  0001 C CNN
	1    8600 1800
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_E2
U 1 1 5D930A41
P 8600 2100
F 0 "J_E2" H 8706 2278 50  0000 C CNN
F 1 "Conn_01x02_Male" H 8706 2187 50  0000 C CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05502HBWC_1x02_P5.00mm_Horizontal" H 8600 2100 50  0001 C CNN
F 3 "~" H 8600 2100 50  0001 C CNN
	1    8600 2100
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_F2
U 1 1 5D930A4F
P 8600 2400
F 0 "J_F2" H 8706 2578 50  0000 C CNN
F 1 "Conn_01x02_Male" H 8706 2487 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 8600 2400 50  0001 C CNN
F 3 "~" H 8600 2400 50  0001 C CNN
	1    8600 2400
	-1   0    0    -1  
$EndComp
$Comp
L bluepill:BP U2
U 1 1 5D9E531E
P 4050 4600
F 0 "U2" H 4050 3456 60  0000 C CNN
F 1 "BP" H 4050 3350 60  0000 C CNN
F 2 "Module:BLUEPILL1" H 3950 5350 60  0001 C CNN
F 3 "" H 3950 5350 60  0001 C CNN
	1    4050 4600
	1    0    0    -1  
$EndComp
$Comp
L Interface_UART:MAX485E U1
U 1 1 5D9ECCFB
P 3750 2550
F 0 "U1" H 3750 3228 50  0000 C CNN
F 1 "MAX485E" H 3750 3150 50  0000 C CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 3750 1850 50  0001 C CNN
F 3 "https://datasheets.maximintegrated.com/en/ds/MAX1487E-MAX491E.pdf" H 3750 2600 50  0001 C CNN
	1    3750 2550
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Male J_SIN1
U 1 1 5D9ED844
P 3400 1250
F 0 "J_SIN1" H 3373 1273 50  0000 R CNN
F 1 "Conn_01x01_Male" H 3373 1182 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 3400 1250 50  0001 C CNN
F 3 "~" H 3400 1250 50  0001 C CNN
	1    3400 1250
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Male J_SG1
U 1 1 5D9EDFB8
P 3400 1500
F 0 "J_SG1" H 3373 1523 50  0000 R CNN
F 1 "Conn_01x01_Male" H 3373 1432 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 3400 1500 50  0001 C CNN
F 3 "~" H 3400 1500 50  0001 C CNN
	1    3400 1500
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Male J_SOUT1
U 1 1 5D9EE0A4
P 3600 1250
F 0 "J_SOUT1" H 3706 1428 50  0000 C CNN
F 1 "Conn_01x01_Male" H 3706 1337 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 3600 1250 50  0001 C CNN
F 3 "~" H 3600 1250 50  0001 C CNN
	1    3600 1250
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Male J_SG2
U 1 1 5D9EE1E2
P 3600 1500
F 0 "J_SG2" H 3706 1678 50  0000 C CNN
F 1 "Conn_01x01_Male" H 3706 1587 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 3600 1500 50  0001 C CNN
F 3 "~" H 3600 1500 50  0001 C CNN
	1    3600 1500
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Male J_OLED1
U 1 1 5D9EF1F0
P 2000 3650
F 0 "J_OLED1" H 2106 3928 50  0000 C CNN
F 1 "Conn_01x04_Male" H 2106 3837 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Vertical" H 2000 3650 50  0001 C CNN
F 3 "~" H 2000 3650 50  0001 C CNN
	1    2000 3650
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D_5V1
U 1 1 5D9EF787
P 5350 1400
F 0 "D_5V1" H 5341 1616 50  0000 C CNN
F 1 "LED" H 5341 1525 50  0000 C CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 5350 1400 50  0001 C CNN
F 3 "~" H 5350 1400 50  0001 C CNN
	1    5350 1400
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D1
U 1 1 5D9EFF0A
P 5350 1700
F 0 "D1" H 5341 1916 50  0000 C CNN
F 1 "D_24V" H 5341 1825 50  0000 C CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 5350 1700 50  0001 C CNN
F 3 "~" H 5350 1700 50  0001 C CNN
	1    5350 1700
	1    0    0    -1  
$EndComp
$Comp
L Device:R R5
U 1 1 5D9F0FDE
P 5700 1700
F 0 "R5" V 5493 1700 50  0000 C CNN
F 1 "R" V 5584 1700 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5630 1700 50  0001 C CNN
F 3 "~" H 5700 1700 50  0001 C CNN
	1    5700 1700
	0    1    1    0   
$EndComp
$Comp
L Device:R R4
U 1 1 5D9F18C9
P 5700 1400
F 0 "R4" V 5493 1400 50  0000 C CNN
F 1 "R" V 5584 1400 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5630 1400 50  0001 C CNN
F 3 "~" H 5700 1400 50  0001 C CNN
	1    5700 1400
	0    1    1    0   
$EndComp
$Comp
L Device:R R1
U 1 1 5D9F26DE
P 5600 3050
F 0 "R1" H 5670 3096 50  0000 L CNN
F 1 "R" H 5670 3005 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5530 3050 50  0001 C CNN
F 3 "~" H 5600 3050 50  0001 C CNN
	1    5600 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:C C1
U 1 1 5D9F38B5
P 5600 3450
F 0 "C1" H 5715 3496 50  0000 L CNN
F 1 "C" H 5715 3405 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 5638 3300 50  0001 C CNN
F 3 "~" H 5600 3450 50  0001 C CNN
	1    5600 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 3200 5600 3250
Wire Wire Line
	5900 3250 5600 3250
Connection ~ 5600 3250
Wire Wire Line
	5600 3250 5600 3300
$Comp
L power:GND #PWR016
U 1 1 5D9FE662
P 5600 3650
F 0 "#PWR016" H 5600 3400 50  0001 C CNN
F 1 "GND" H 5605 3477 50  0000 C CNN
F 2 "" H 5600 3650 50  0001 C CNN
F 3 "" H 5600 3650 50  0001 C CNN
	1    5600 3650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR014
U 1 1 5DA010D7
P 5050 2150
F 0 "#PWR014" H 5050 1900 50  0001 C CNN
F 1 "GND" H 5055 1977 50  0000 C CNN
F 2 "" H 5050 2150 50  0001 C CNN
F 3 "" H 5050 2150 50  0001 C CNN
	1    5050 2150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5200 1400 5050 1400
Wire Wire Line
	5050 1400 5050 1700
Wire Wire Line
	5200 1700 5050 1700
Connection ~ 5050 1700
Wire Wire Line
	5550 1400 5500 1400
Wire Wire Line
	5550 1700 5500 1700
$Comp
L power:+5V #PWR024
U 1 1 5DA058CC
P 5950 1400
F 0 "#PWR024" H 5950 1250 50  0001 C CNN
F 1 "+5V" H 5965 1573 50  0000 C CNN
F 2 "" H 5950 1400 50  0001 C CNN
F 3 "" H 5950 1400 50  0001 C CNN
	1    5950 1400
	1    0    0    -1  
$EndComp
$Comp
L power:+24V #PWR025
U 1 1 5DA06247
P 5950 1700
F 0 "#PWR025" H 5950 1550 50  0001 C CNN
F 1 "+24V" H 5965 1873 50  0000 C CNN
F 2 "" H 5950 1700 50  0001 C CNN
F 3 "" H 5950 1700 50  0001 C CNN
	1    5950 1700
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR015
U 1 1 5DA06F1C
P 5600 2850
F 0 "#PWR015" H 5600 2700 50  0001 C CNN
F 1 "+3V3" H 5615 3023 50  0000 C CNN
F 2 "" H 5600 2850 50  0001 C CNN
F 3 "" H 5600 2850 50  0001 C CNN
	1    5600 2850
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR011
U 1 1 5DA08A57
P 4050 3500
F 0 "#PWR011" H 4050 3350 50  0001 C CNN
F 1 "+3V3" H 4065 3673 50  0000 C CNN
F 2 "" H 4050 3500 50  0001 C CNN
F 3 "" H 4050 3500 50  0001 C CNN
	1    4050 3500
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR012
U 1 1 5DA096DD
P 4200 3500
F 0 "#PWR012" H 4200 3350 50  0001 C CNN
F 1 "+5V" H 4215 3673 50  0000 C CNN
F 2 "" H 4200 3500 50  0001 C CNN
F 3 "" H 4200 3500 50  0001 C CNN
	1    4200 3500
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR09
U 1 1 5DA0AAD5
P 3800 1150
F 0 "#PWR09" H 3800 1000 50  0001 C CNN
F 1 "+5V" H 3815 1323 50  0000 C CNN
F 2 "" H 3800 1150 50  0001 C CNN
F 3 "" H 3800 1150 50  0001 C CNN
	1    3800 1150
	1    0    0    -1  
$EndComp
$Comp
L power:+24V #PWR05
U 1 1 5DA0B143
P 3200 1150
F 0 "#PWR05" H 3200 1000 50  0001 C CNN
F 1 "+24V" H 3215 1323 50  0000 C CNN
F 2 "" H 3200 1150 50  0001 C CNN
F 3 "" H 3200 1150 50  0001 C CNN
	1    3200 1150
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR07
U 1 1 5DA0BDC5
P 3750 2000
F 0 "#PWR07" H 3750 1850 50  0001 C CNN
F 1 "+3V3" H 3765 2173 50  0000 C CNN
F 2 "" H 3750 2000 50  0001 C CNN
F 3 "" H 3750 2000 50  0001 C CNN
	1    3750 2000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR08
U 1 1 5DA0CAD4
P 3750 3200
F 0 "#PWR08" H 3750 2950 50  0001 C CNN
F 1 "GND" H 3755 3027 50  0000 C CNN
F 2 "" H 3750 3200 50  0001 C CNN
F 3 "" H 3750 3200 50  0001 C CNN
	1    3750 3200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR013
U 1 1 5DA0D0A1
P 4200 5750
F 0 "#PWR013" H 4200 5500 50  0001 C CNN
F 1 "GND" H 4205 5577 50  0000 C CNN
F 2 "" H 4200 5750 50  0001 C CNN
F 3 "" H 4200 5750 50  0001 C CNN
	1    4200 5750
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR03
U 1 1 5DA0D695
P 2550 1950
F 0 "#PWR03" H 2550 1700 50  0001 C CNN
F 1 "GND" H 2555 1777 50  0000 C CNN
F 2 "" H 2550 1950 50  0001 C CNN
F 3 "" H 2550 1950 50  0001 C CNN
	1    2550 1950
	1    0    0    -1  
$EndComp
$Comp
L power:+24V #PWR04
U 1 1 5DA0E31B
P 2550 1800
F 0 "#PWR04" H 2550 1650 50  0001 C CNN
F 1 "+24V" H 2565 1973 50  0000 C CNN
F 2 "" H 2550 1800 50  0001 C CNN
F 3 "" H 2550 1800 50  0001 C CNN
	1    2550 1800
	1    0    0    -1  
$EndComp
$Comp
L power:+24V #PWR030
U 1 1 5DA0EE16
P 8100 1250
F 0 "#PWR030" H 8100 1100 50  0001 C CNN
F 1 "+24V" H 8115 1423 50  0000 C CNN
F 2 "" H 8100 1250 50  0001 C CNN
F 3 "" H 8100 1250 50  0001 C CNN
	1    8100 1250
	1    0    0    -1  
$EndComp
$Comp
L power:+24V #PWR028
U 1 1 5DA0F062
P 6950 1250
F 0 "#PWR028" H 6950 1100 50  0001 C CNN
F 1 "+24V" H 6965 1423 50  0000 C CNN
F 2 "" H 6950 1250 50  0001 C CNN
F 3 "" H 6950 1250 50  0001 C CNN
	1    6950 1250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR026
U 1 1 5DA10291
P 6900 2750
F 0 "#PWR026" H 6900 2500 50  0001 C CNN
F 1 "GND" H 6905 2577 50  0000 C CNN
F 2 "" H 6900 2750 50  0001 C CNN
F 3 "" H 6900 2750 50  0001 C CNN
	1    6900 2750
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR021
U 1 1 5DA10C09
P 5900 3500
F 0 "#PWR021" H 5900 3250 50  0001 C CNN
F 1 "GND" H 5900 3350 50  0000 C CNN
F 2 "" H 5900 3500 50  0001 C CNN
F 3 "" H 5900 3500 50  0001 C CNN
	1    5900 3500
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR01
U 1 1 5DA1312F
P 2300 3850
F 0 "#PWR01" H 2300 3600 50  0001 C CNN
F 1 "GND" H 2305 3677 50  0000 C CNN
F 2 "" H 2300 3850 50  0001 C CNN
F 3 "" H 2300 3850 50  0001 C CNN
	1    2300 3850
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR02
U 1 1 5DA13E78
P 2450 3750
F 0 "#PWR02" H 2450 3600 50  0001 C CNN
F 1 "+3V3" H 2465 3923 50  0000 C CNN
F 2 "" H 2450 3750 50  0001 C CNN
F 3 "" H 2450 3750 50  0001 C CNN
	1    2450 3750
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR034
U 1 1 5DA148DE
P 9500 1150
F 0 "#PWR034" H 9500 900 50  0001 C CNN
F 1 "GND" H 9505 977 50  0000 C CNN
F 2 "" H 9500 1150 50  0001 C CNN
F 3 "" H 9500 1150 50  0001 C CNN
	1    9500 1150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR035
U 1 1 5DA14B2A
P 9500 1650
F 0 "#PWR035" H 9500 1400 50  0001 C CNN
F 1 "GND" H 9505 1477 50  0000 C CNN
F 2 "" H 9500 1650 50  0001 C CNN
F 3 "" H 9500 1650 50  0001 C CNN
	1    9500 1650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR036
U 1 1 5DA14CDA
P 9500 2150
F 0 "#PWR036" H 9500 1900 50  0001 C CNN
F 1 "GND" H 9505 1977 50  0000 C CNN
F 2 "" H 9500 2150 50  0001 C CNN
F 3 "" H 9500 2150 50  0001 C CNN
	1    9500 2150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR037
U 1 1 5DA14F26
P 9500 2700
F 0 "#PWR037" H 9500 2450 50  0001 C CNN
F 1 "GND" H 9505 2527 50  0000 C CNN
F 2 "" H 9500 2700 50  0001 C CNN
F 3 "" H 9500 2700 50  0001 C CNN
	1    9500 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	9500 1100 9500 1150
Wire Wire Line
	9500 1600 9500 1650
Wire Wire Line
	9500 2100 9500 2150
Wire Wire Line
	9500 2600 9500 2700
Wire Wire Line
	8100 1250 8100 1400
Wire Wire Line
	8100 1400 7950 1400
Wire Wire Line
	7950 2700 8100 2700
Wire Wire Line
	8100 2700 8100 1400
Connection ~ 8100 1400
$Comp
L power:GND #PWR06
U 1 1 5DA30237
P 3200 1600
F 0 "#PWR06" H 3200 1350 50  0001 C CNN
F 1 "GND" H 3205 1427 50  0000 C CNN
F 2 "" H 3200 1600 50  0001 C CNN
F 3 "" H 3200 1600 50  0001 C CNN
	1    3200 1600
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR010
U 1 1 5DA305BA
P 3800 1600
F 0 "#PWR010" H 3800 1350 50  0001 C CNN
F 1 "GND" H 3805 1427 50  0000 C CNN
F 2 "" H 3800 1600 50  0001 C CNN
F 3 "" H 3800 1600 50  0001 C CNN
	1    3800 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 1150 3200 1250
Wire Wire Line
	3200 1500 3200 1600
Wire Wire Line
	3800 1500 3800 1600
Wire Wire Line
	3800 1150 3800 1250
Wire Wire Line
	3750 3150 3750 3200
Wire Wire Line
	3750 2000 3750 2050
Wire Wire Line
	5850 1400 5950 1400
Wire Wire Line
	5850 1700 5950 1700
Wire Wire Line
	6950 1250 6950 1400
Wire Wire Line
	6950 1400 7050 1400
Wire Wire Line
	7050 2000 6950 2000
Wire Wire Line
	6950 2000 6950 1400
Connection ~ 6950 1400
Wire Wire Line
	7050 2100 6950 2100
Wire Wire Line
	6950 2100 6950 2000
Connection ~ 6950 2000
Wire Wire Line
	7050 2700 6950 2700
Wire Wire Line
	6950 2700 6950 2100
Connection ~ 6950 2100
Wire Wire Line
	7050 1500 6900 1500
Wire Wire Line
	6900 1500 6900 2200
Wire Wire Line
	7050 2200 6900 2200
Connection ~ 6900 2200
Wire Wire Line
	6900 2200 6900 2750
Wire Wire Line
	7950 2400 8050 2400
Wire Wire Line
	7950 2500 8050 2500
Wire Wire Line
	8050 2500 8050 2400
Connection ~ 8050 2400
Wire Wire Line
	8050 2400 8400 2400
Wire Wire Line
	7950 2600 8050 2600
Wire Wire Line
	8050 2600 8050 2500
Connection ~ 8050 2500
Wire Wire Line
	7950 2100 8050 2100
Wire Wire Line
	7950 2200 8050 2200
Wire Wire Line
	8050 2200 8050 2100
Connection ~ 8050 2100
Wire Wire Line
	8050 2100 8400 2100
Wire Wire Line
	7950 2300 8050 2300
Wire Wire Line
	8050 2300 8050 2200
Connection ~ 8050 2200
Wire Wire Line
	7950 1800 8050 1800
Wire Wire Line
	7950 1900 8050 1900
Wire Wire Line
	8050 1900 8050 1800
Connection ~ 8050 1800
Wire Wire Line
	8050 1800 8400 1800
Wire Wire Line
	7950 2000 8050 2000
Wire Wire Line
	8050 2000 8050 1900
Connection ~ 8050 1900
Wire Wire Line
	7950 1500 8050 1500
Wire Wire Line
	7950 1600 8050 1600
Wire Wire Line
	8050 1600 8050 1500
Connection ~ 8050 1500
Wire Wire Line
	8050 1500 8400 1500
Wire Wire Line
	7950 1700 8050 1700
Wire Wire Line
	8050 1700 8050 1600
Connection ~ 8050 1600
$Comp
L power:GND #PWR032
U 1 1 5DA5507E
P 8300 2600
F 0 "#PWR032" H 8300 2350 50  0001 C CNN
F 1 "GND" H 8305 2427 50  0000 C CNN
F 2 "" H 8300 2600 50  0001 C CNN
F 3 "" H 8300 2600 50  0001 C CNN
	1    8300 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	8400 1600 8300 1600
Wire Wire Line
	8300 1600 8300 1900
Wire Wire Line
	8400 2500 8300 2500
Connection ~ 8300 2500
Wire Wire Line
	8300 2500 8300 2600
Wire Wire Line
	8400 2200 8300 2200
Connection ~ 8300 2200
Wire Wire Line
	8300 2200 8300 2500
Wire Wire Line
	8400 1900 8300 1900
Connection ~ 8300 1900
Wire Wire Line
	8300 1900 8300 2200
$Comp
L Power_Management:bts737s2 U4
U 1 1 5DA5F34F
P 7200 3250
F 0 "U4" H 7500 3365 50  0000 C CNN
F 1 "bts737s2" H 7500 3274 50  0000 C CNN
F 2 "Package_SO:SOIC-28W_7.5x18.7mm_P1.27mm" H 7800 3300 50  0001 C CNN
F 3 "" H 7800 3300 50  0001 C CNN
	1    7200 3250
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_E3
U 1 1 5DA5F356
P 8600 3500
F 0 "J_E3" H 8706 3678 50  0000 C CNN
F 1 "Conn_01x02_Male" H 8706 3587 50  0000 C CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05502HBWC_1x02_P5.00mm_Horizontal" H 8600 3500 50  0001 C CNN
F 3 "~" H 8600 3500 50  0001 C CNN
	1    8600 3500
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_F3
U 1 1 5DA5F35D
P 8600 3800
F 0 "J_F3" H 8706 3978 50  0000 C CNN
F 1 "Conn_01x02_Male" H 8706 3887 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 8600 3800 50  0001 C CNN
F 3 "~" H 8600 3800 50  0001 C CNN
	1    8600 3800
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_OUT1
U 1 1 5DA5F364
P 8600 4100
F 0 "J_OUT1" H 8706 4278 50  0000 C CNN
F 1 "Conn_01x02_Male" H 8706 4187 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 8600 4100 50  0001 C CNN
F 3 "~" H 8600 4100 50  0001 C CNN
	1    8600 4100
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_OUT2
U 1 1 5DA5F36B
P 8600 4400
F 0 "J_OUT2" H 8706 4578 50  0000 C CNN
F 1 "Conn_01x02_Male" H 8706 4487 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 8600 4400 50  0001 C CNN
F 3 "~" H 8600 4400 50  0001 C CNN
	1    8600 4400
	-1   0    0    -1  
$EndComp
$Comp
L power:+24V #PWR031
U 1 1 5DA5F372
P 8100 3250
F 0 "#PWR031" H 8100 3100 50  0001 C CNN
F 1 "+24V" H 8115 3423 50  0000 C CNN
F 2 "" H 8100 3250 50  0001 C CNN
F 3 "" H 8100 3250 50  0001 C CNN
	1    8100 3250
	1    0    0    -1  
$EndComp
$Comp
L power:+24V #PWR029
U 1 1 5DA5F378
P 6950 3250
F 0 "#PWR029" H 6950 3100 50  0001 C CNN
F 1 "+24V" H 6965 3423 50  0000 C CNN
F 2 "" H 6950 3250 50  0001 C CNN
F 3 "" H 6950 3250 50  0001 C CNN
	1    6950 3250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR027
U 1 1 5DA5F37E
P 6900 4750
F 0 "#PWR027" H 6900 4500 50  0001 C CNN
F 1 "GND" H 6905 4577 50  0000 C CNN
F 2 "" H 6900 4750 50  0001 C CNN
F 3 "" H 6900 4750 50  0001 C CNN
	1    6900 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	8100 3250 8100 3400
Wire Wire Line
	8100 3400 7950 3400
Wire Wire Line
	7950 4700 8100 4700
Wire Wire Line
	8100 4700 8100 3400
Connection ~ 8100 3400
Wire Wire Line
	6950 3250 6950 3400
Wire Wire Line
	6950 3400 7050 3400
Wire Wire Line
	7050 4000 6950 4000
Wire Wire Line
	6950 4000 6950 3400
Connection ~ 6950 3400
Wire Wire Line
	7050 4100 6950 4100
Wire Wire Line
	6950 4100 6950 4000
Connection ~ 6950 4000
Wire Wire Line
	7050 4700 6950 4700
Wire Wire Line
	6950 4700 6950 4100
Connection ~ 6950 4100
Wire Wire Line
	7050 3500 6900 3500
Wire Wire Line
	6900 3500 6900 4200
Wire Wire Line
	7050 4200 6900 4200
Connection ~ 6900 4200
Wire Wire Line
	6900 4200 6900 4750
Wire Wire Line
	7950 4400 8050 4400
Wire Wire Line
	7950 4500 8050 4500
Wire Wire Line
	8050 4500 8050 4400
Connection ~ 8050 4400
Wire Wire Line
	8050 4400 8400 4400
Wire Wire Line
	7950 4600 8050 4600
Wire Wire Line
	8050 4600 8050 4500
Connection ~ 8050 4500
Wire Wire Line
	7950 4100 8050 4100
Wire Wire Line
	7950 4200 8050 4200
Wire Wire Line
	8050 4200 8050 4100
Connection ~ 8050 4100
Wire Wire Line
	8050 4100 8400 4100
Wire Wire Line
	7950 4300 8050 4300
Wire Wire Line
	8050 4300 8050 4200
Connection ~ 8050 4200
Wire Wire Line
	7950 3800 8050 3800
Wire Wire Line
	7950 3900 8050 3900
Wire Wire Line
	8050 3900 8050 3800
Connection ~ 8050 3800
Wire Wire Line
	8050 3800 8400 3800
Wire Wire Line
	7950 4000 8050 4000
Wire Wire Line
	8050 4000 8050 3900
Connection ~ 8050 3900
Wire Wire Line
	7950 3500 8050 3500
Wire Wire Line
	7950 3600 8050 3600
Wire Wire Line
	8050 3600 8050 3500
Connection ~ 8050 3500
Wire Wire Line
	8050 3500 8400 3500
Wire Wire Line
	7950 3700 8050 3700
Wire Wire Line
	8050 3700 8050 3600
Connection ~ 8050 3600
$Comp
L power:GND #PWR033
U 1 1 5DA5F3B9
P 8300 4600
F 0 "#PWR033" H 8300 4350 50  0001 C CNN
F 1 "GND" H 8305 4427 50  0000 C CNN
F 2 "" H 8300 4600 50  0001 C CNN
F 3 "" H 8300 4600 50  0001 C CNN
	1    8300 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	8400 3600 8300 3600
Wire Wire Line
	8300 3600 8300 3900
Wire Wire Line
	8400 4500 8300 4500
Connection ~ 8300 4500
Wire Wire Line
	8300 4500 8300 4600
Wire Wire Line
	8400 4200 8300 4200
Connection ~ 8300 4200
Wire Wire Line
	8300 4200 8300 4500
Wire Wire Line
	8400 3900 8300 3900
Connection ~ 8300 3900
Wire Wire Line
	8300 3900 8300 4200
Wire Wire Line
	5600 3600 5600 3650
Wire Wire Line
	5600 3250 5400 3250
Wire Wire Line
	5900 3350 5900 3500
$Comp
L Connector:Conn_01x02_Male J_TH2
U 1 1 5DAA3171
P 6100 4500
F 0 "J_TH2" H 6206 4678 50  0000 C CNN
F 1 "Conn_01x02_Male" H 6206 4587 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 6100 4500 50  0001 C CNN
F 3 "~" H 6100 4500 50  0001 C CNN
	1    6100 4500
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5DAA3178
P 5600 4300
F 0 "R2" H 5670 4346 50  0000 L CNN
F 1 "R" H 5670 4255 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5530 4300 50  0001 C CNN
F 3 "~" H 5600 4300 50  0001 C CNN
	1    5600 4300
	1    0    0    -1  
$EndComp
$Comp
L Device:C C2
U 1 1 5DAA317F
P 5600 4700
F 0 "C2" H 5715 4746 50  0000 L CNN
F 1 "C" H 5715 4655 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 5638 4550 50  0001 C CNN
F 3 "~" H 5600 4700 50  0001 C CNN
	1    5600 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 4450 5600 4500
Wire Wire Line
	5900 4500 5600 4500
Connection ~ 5600 4500
Wire Wire Line
	5600 4500 5600 4550
$Comp
L power:GND #PWR018
U 1 1 5DAA318A
P 5600 4900
F 0 "#PWR018" H 5600 4650 50  0001 C CNN
F 1 "GND" H 5605 4727 50  0000 C CNN
F 2 "" H 5600 4900 50  0001 C CNN
F 3 "" H 5600 4900 50  0001 C CNN
	1    5600 4900
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR017
U 1 1 5DAA3190
P 5600 4100
F 0 "#PWR017" H 5600 3950 50  0001 C CNN
F 1 "+3V3" H 5615 4273 50  0000 C CNN
F 2 "" H 5600 4100 50  0001 C CNN
F 3 "" H 5600 4100 50  0001 C CNN
	1    5600 4100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR022
U 1 1 5DAA3196
P 5900 4750
F 0 "#PWR022" H 5900 4500 50  0001 C CNN
F 1 "GND" H 5900 4600 50  0000 C CNN
F 2 "" H 5900 4750 50  0001 C CNN
F 3 "" H 5900 4750 50  0001 C CNN
	1    5900 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 4850 5600 4900
Wire Wire Line
	5600 4500 5400 4500
Wire Wire Line
	5900 4600 5900 4750
$Comp
L Connector:Conn_01x02_Male J_TH3
U 1 1 5DAA81A2
P 6100 5750
F 0 "J_TH3" H 6206 5928 50  0000 C CNN
F 1 "Conn_01x02_Male" H 6206 5837 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 6100 5750 50  0001 C CNN
F 3 "~" H 6100 5750 50  0001 C CNN
	1    6100 5750
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 5DAA81A9
P 5600 5550
F 0 "R3" H 5670 5596 50  0000 L CNN
F 1 "R" H 5670 5505 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5530 5550 50  0001 C CNN
F 3 "~" H 5600 5550 50  0001 C CNN
	1    5600 5550
	1    0    0    -1  
$EndComp
$Comp
L Device:C C3
U 1 1 5DAA81B0
P 5600 5950
F 0 "C3" H 5715 5996 50  0000 L CNN
F 1 "C" H 5715 5905 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 5638 5800 50  0001 C CNN
F 3 "~" H 5600 5950 50  0001 C CNN
	1    5600 5950
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 5700 5600 5750
Wire Wire Line
	5900 5750 5600 5750
Connection ~ 5600 5750
Wire Wire Line
	5600 5750 5600 5800
$Comp
L power:GND #PWR020
U 1 1 5DAA81BB
P 5600 6150
F 0 "#PWR020" H 5600 5900 50  0001 C CNN
F 1 "GND" H 5605 5977 50  0000 C CNN
F 2 "" H 5600 6150 50  0001 C CNN
F 3 "" H 5600 6150 50  0001 C CNN
	1    5600 6150
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR019
U 1 1 5DAA81C1
P 5600 5350
F 0 "#PWR019" H 5600 5200 50  0001 C CNN
F 1 "+3V3" H 5615 5523 50  0000 C CNN
F 2 "" H 5600 5350 50  0001 C CNN
F 3 "" H 5600 5350 50  0001 C CNN
	1    5600 5350
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR023
U 1 1 5DAA81C7
P 5900 6000
F 0 "#PWR023" H 5900 5750 50  0001 C CNN
F 1 "GND" H 5900 5850 50  0000 C CNN
F 2 "" H 5900 6000 50  0001 C CNN
F 3 "" H 5900 6000 50  0001 C CNN
	1    5900 6000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 6100 5600 6150
Wire Wire Line
	5600 5750 5400 5750
Wire Wire Line
	5900 5850 5900 6000
Wire Wire Line
	7050 1600 6700 1600
Wire Wire Line
	7050 1700 6700 1700
Wire Wire Line
	7050 1800 6700 1800
Wire Wire Line
	7050 1900 6700 1900
Wire Wire Line
	7050 2300 6700 2300
Wire Wire Line
	7050 2400 6700 2400
Wire Wire Line
	7050 2500 6700 2500
Wire Wire Line
	7050 2600 6700 2600
Wire Wire Line
	7050 3600 6700 3600
Wire Wire Line
	7050 3700 6700 3700
Wire Wire Line
	7050 3800 6700 3800
Wire Wire Line
	7050 3900 6700 3900
Wire Wire Line
	7050 4300 6700 4300
Wire Wire Line
	7050 4400 6700 4400
Wire Wire Line
	7050 4500 6700 4500
Wire Wire Line
	7050 4600 6700 4600
Text Label 6700 1600 0    50   ~ 0
P_IN2
Text Label 6700 1700 0    50   ~ 0
P_IN1
Text Label 6700 1800 0    50   ~ 0
P_IS1
Text Label 6700 1900 0    50   ~ 0
P_IS2
Text Label 6700 2300 0    50   ~ 0
P_IN4
Text Label 6700 2400 0    50   ~ 0
P_IN3
Text Label 6700 2500 0    50   ~ 0
P_IS3
Text Label 6700 2600 0    50   ~ 0
P_IS4
Text Label 6700 3600 0    50   ~ 0
P_IN6
Text Label 6700 3700 0    50   ~ 0
P_IN5
Text Label 6700 3800 0    50   ~ 0
P_IS5
Text Label 6700 3900 0    50   ~ 0
P_IS6
Text Label 6700 4300 0    50   ~ 0
P_IN8
Text Label 6700 4400 0    50   ~ 0
P_IN7
Text Label 6700 4500 0    50   ~ 0
P_IS7
Text Label 6700 4600 0    50   ~ 0
P_IS8
Text Label 5400 3250 0    50   ~ 0
TH1
Text Label 5400 4500 0    50   ~ 0
TH2
Text Label 5400 5750 0    50   ~ 0
TH3
Wire Wire Line
	2200 3750 2450 3750
Wire Wire Line
	2200 3850 2300 3850
Wire Wire Line
	2200 3650 2350 3650
Wire Wire Line
	2200 3550 2350 3550
Text Label 2350 3650 0    50   ~ 0
SCL
Text Label 2350 3550 0    50   ~ 0
SDA
Wire Wire Line
	4200 3500 4200 3550
Wire Wire Line
	4050 3500 4050 3550
Wire Wire Line
	4200 5650 4200 5750
$Comp
L Connector:Conn_01x04_Male J_ISP1
U 1 1 5DB7B04B
P 2000 5200
F 0 "J_ISP1" H 2106 5478 50  0000 C CNN
F 1 "Conn_01x04_Male" H 2106 5387 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Vertical" H 2000 5200 50  0001 C CNN
F 3 "~" H 2000 5200 50  0001 C CNN
	1    2000 5200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5DB7B052
P 2300 5400
F 0 "#PWR0103" H 2300 5150 50  0001 C CNN
F 1 "GND" H 2305 5227 50  0000 C CNN
F 2 "" H 2300 5400 50  0001 C CNN
F 3 "" H 2300 5400 50  0001 C CNN
	1    2300 5400
	1    0    0    -1  
$EndComp
Wire Wire Line
	2200 5400 2300 5400
Wire Wire Line
	2200 5200 2350 5200
Wire Wire Line
	2200 5100 2350 5100
Text Label 2350 5200 0    50   ~ 0
RX
Text Label 2350 5100 0    50   ~ 0
RESET
Wire Wire Line
	2200 5300 2350 5300
Text Label 2350 5300 0    50   ~ 0
TX
$Comp
L Device:LED D_E1
U 1 1 5DB9C165
P 9800 3500
F 0 "D_E1" H 9791 3716 50  0000 C CNN
F 1 "LED" H 9791 3625 50  0000 C CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 9800 3500 50  0001 C CNN
F 3 "~" H 9800 3500 50  0001 C CNN
	1    9800 3500
	1    0    0    -1  
$EndComp
$Comp
L Device:R R7
U 1 1 5DB9C16C
P 10150 3500
F 0 "R7" V 9943 3500 50  0000 C CNN
F 1 "R" V 10034 3500 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 10080 3500 50  0001 C CNN
F 3 "~" H 10150 3500 50  0001 C CNN
	1    10150 3500
	0    1    1    0   
$EndComp
Wire Wire Line
	9650 3500 9600 3500
Wire Wire Line
	10000 3500 9950 3500
Wire Wire Line
	10300 3500 10400 3500
$Comp
L power:GND #PWR0104
U 1 1 5DBA5C0C
P 9500 3500
F 0 "#PWR0104" H 9500 3250 50  0001 C CNN
F 1 "GND" H 9505 3327 50  0000 C CNN
F 2 "" H 9500 3500 50  0001 C CNN
F 3 "" H 9500 3500 50  0001 C CNN
	1    9500 3500
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D_E2
U 1 1 5DBB0B72
P 9800 3650
F 0 "D_E2" H 9791 3866 50  0000 C CNN
F 1 "LED" H 9791 3775 50  0000 C CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 9800 3650 50  0001 C CNN
F 3 "~" H 9800 3650 50  0001 C CNN
	1    9800 3650
	1    0    0    -1  
$EndComp
$Comp
L Device:R R8
U 1 1 5DBB0B79
P 10150 3650
F 0 "R8" V 9943 3650 50  0000 C CNN
F 1 "R" V 10034 3650 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 10080 3650 50  0001 C CNN
F 3 "~" H 10150 3650 50  0001 C CNN
	1    10150 3650
	0    1    1    0   
$EndComp
Wire Wire Line
	10000 3650 9950 3650
Wire Wire Line
	10300 3650 10400 3650
$Comp
L Device:LED D_E3
U 1 1 5DBBA215
P 9800 3800
F 0 "D_E3" H 9791 4016 50  0000 C CNN
F 1 "LED" H 9791 3925 50  0000 C CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 9800 3800 50  0001 C CNN
F 3 "~" H 9800 3800 50  0001 C CNN
	1    9800 3800
	1    0    0    -1  
$EndComp
$Comp
L Device:R R9
U 1 1 5DBBA21C
P 10150 3800
F 0 "R9" V 9943 3800 50  0000 C CNN
F 1 "R" V 10034 3800 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 10080 3800 50  0001 C CNN
F 3 "~" H 10150 3800 50  0001 C CNN
	1    10150 3800
	0    1    1    0   
$EndComp
Wire Wire Line
	10000 3800 9950 3800
Wire Wire Line
	10300 3800 10400 3800
Wire Wire Line
	9650 3650 9600 3650
Wire Wire Line
	9600 3650 9600 3500
Connection ~ 9600 3500
Wire Wire Line
	9600 3500 9500 3500
Wire Wire Line
	9650 3800 9600 3800
Wire Wire Line
	9600 3800 9600 3650
Connection ~ 9600 3650
Text Label 10400 3500 0    50   ~ 0
OUT_E1
Text Label 10400 3650 0    50   ~ 0
OUT_E2
Text Label 10400 3800 0    50   ~ 0
OUT_E3
Text Label 8200 1500 0    50   ~ 0
OUT_E1
Text Label 8200 2100 0    50   ~ 0
OUT_E2
Text Label 8200 3500 0    50   ~ 0
OUT_E3
Wire Wire Line
	3300 3800 2850 3800
Text Label 2850 3800 0    50   ~ 0
DEBUG
Wire Wire Line
	3300 5400 2950 5400
Text Label 2950 5400 0    50   ~ 0
RESET
Wire Wire Line
	4800 4900 5100 4900
Wire Wire Line
	4800 4800 5100 4800
Text Label 5000 4900 0    50   ~ 0
TX
Wire Wire Line
	4800 4100 5150 4100
Wire Wire Line
	4800 4000 5150 4000
Text Label 5150 4100 0    50   ~ 0
SCL
Wire Wire Line
	4150 2750 4400 2750
Wire Wire Line
	4150 2650 4250 2650
Wire Wire Line
	4150 2550 4250 2550
Wire Wire Line
	4250 2550 4250 2650
Connection ~ 4250 2650
Wire Wire Line
	4250 2650 4400 2650
Wire Wire Line
	4150 2450 4400 2450
Wire Wire Line
	5050 1700 5050 2150
Wire Wire Line
	3300 4200 3000 4200
Wire Wire Line
	3300 4300 3000 4300
Wire Wire Line
	3300 4400 3000 4400
Text Label 4400 2450 0    50   ~ 0
RS485_RO
Text Label 4400 2650 0    50   ~ 0
RS485_DE
Text Label 4400 2750 0    50   ~ 0
RS485_DI
Text Label 3000 4200 0    50   ~ 0
RS485_DE
Text Label 3000 4300 0    50   ~ 0
RS485_DI
Text Label 3000 4400 0    50   ~ 0
RS485_RO
Wire Wire Line
	3300 4100 3000 4100
Wire Wire Line
	3300 4500 3000 4500
Wire Wire Line
	3300 4600 3000 4600
Text Label 3000 4100 0    50   ~ 0
TH1
Text Label 3000 4500 0    50   ~ 0
TH2
Text Label 3000 4600 0    50   ~ 0
TH3
Wire Wire Line
	3300 4700 3000 4700
Wire Wire Line
	3300 4800 3000 4800
Wire Wire Line
	3300 4900 3000 4900
Text Label 3000 4700 0    50   ~ 0
P_IN1
Text Label 3000 4800 0    50   ~ 0
P_IN3
Text Label 3000 4900 0    50   ~ 0
P_IN5
Wire Wire Line
	4800 5300 5100 5300
Wire Wire Line
	4800 5200 5100 5200
Wire Wire Line
	4800 5100 5100 5100
Text Label 5100 5100 0    50   ~ 0
P_IN2
Text Label 5100 5200 0    50   ~ 0
P_IN4
Text Label 5100 5300 0    50   ~ 0
P_IN6
Wire Wire Line
	3300 3900 3000 3900
Wire Wire Line
	3300 4000 3000 4000
Text Label 3000 3900 0    50   ~ 0
P_IN7
Text Label 3000 4000 0    50   ~ 0
P_IN8
Text Label 5100 4800 0    50   ~ 0
RX
Wire Wire Line
	5600 2850 5600 2900
Wire Wire Line
	5600 4100 5600 4150
Wire Wire Line
	5600 5350 5600 5400
$Comp
L Device:R R6
U 1 1 5E05E5C0
P 2850 4850
F 0 "R6" H 2920 4896 50  0000 L CNN
F 1 "R" H 2920 4805 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 2780 4850 50  0001 C CNN
F 3 "~" H 2850 4850 50  0001 C CNN
	1    2850 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 5000 3300 5000
Wire Wire Line
	2850 4700 2850 4500
Text Label 2850 4500 0    50   ~ 0
P_IS1
Wire Wire Line
	3300 5100 2950 5100
Wire Wire Line
	3300 5200 2950 5200
Text Label 2950 5100 0    50   ~ 0
EXT1
Text Label 2950 5200 0    50   ~ 0
EXT2
Text Label 5150 4000 0    50   ~ 0
SDA
$Comp
L Connector:Conn_01x02_Male J_IN24
U 1 1 5DABB56A
P 1950 1850
F 0 "J_IN24" H 2056 2028 50  0000 C CNN
F 1 "Conn_01x02_Male" H 2056 1937 50  0000 C CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05502HBWC_1x02_P5.00mm_Horizontal" H 1950 1850 50  0001 C CNN
F 3 "~" H 1950 1850 50  0001 C CNN
	1    1950 1850
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J_RS485
U 1 1 5DACA151
P 1900 2300
F 0 "J_RS485" H 2006 2478 50  0000 C CNN
F 1 "Conn_01x02_Male" H 2006 2387 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 1900 2300 50  0001 C CNN
F 3 "~" H 1900 2300 50  0001 C CNN
	1    1900 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 1950 2550 1950
Wire Wire Line
	2150 1850 2550 1850
Wire Wire Line
	2550 1850 2550 1800
Wire Wire Line
	2100 2300 3000 2300
Wire Wire Line
	3000 2300 3000 2450
Wire Wire Line
	3000 2450 3350 2450
Wire Wire Line
	3350 2750 2850 2750
Wire Wire Line
	2850 2750 2850 2400
Wire Wire Line
	2850 2400 2100 2400
$EndSCHEMATC
