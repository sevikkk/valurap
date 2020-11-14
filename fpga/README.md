Abbrevs
=======

* ASG - Acceleration step generator
* APG - Acceleration profile generator
* SP - SPeed integrator
* MSG - Motor step generator
* BE - buffer commands executor
* SE - S3G commands executor
* ES - EndStop debouncer

Outputs
=======

|Number | Name | Bits | Description
|------ | ---- | ---- | -----------
|0  | ASG_DT_VAL | 31..0 | Length of each step in current cycle in clocks
|1  |  ASG_STEPS_VAL | 31..0 | Number of steps in current acceleration cycle
|2  | SP_CONFIG | | |
| 3 | MSG_ALL_PRE_N | 31..0 | Length of pre-pulse (after potential direction switch)
| 4 | MSG_ALL_PULSE_N | 31..0 | Length of pulse
| 5 | MSG_ALL_POST_N | 31..0 | Length of post-pulse
| 6  | MSG_X_VAL| 31..0 | Value to set X to
| 7 | MSG_CONFIG0 | 2..0 | ES mux select
|  |              | 3 | Enable steps
|  |              | 6..4 | SP mux select
|  |              | 7 | Enable abort on ES change
|  |              | 8 | Invert Direction
|  |              | 9 | Set X value by stb[6]
|  |              | 14..10 | Unused
|  |              | 15 | Set enable output
| 8 | MSG_CONFIG1 | |
| 9 | MSG_CONFIG2 | |
| 10 | MSG_CONFIG3 | |
| 11 | MSG_CONFIG4 | |
| 12 | MSG_CONFIG5 | |
| 13 | ES_TIMEOUT | |
|14..62| Unused
|63 | SE_REG_LB | 31..0| Looped back to Input 63
 
Inputs
======

| Number | Name | Bits | Description
| ------ | ---- | ---- | -----------
|  0 | BE_STATUS
|  1 | APG_STATUS
|  2 | ES_STATUS
|  3 | FIFO_FREE_SPACE
|  4 | FIFO_DATA_COUNT
|  5 | MOTOR1_HOLD_X
|  6 | MOTOR2_HOLD_X
|  7 | MOTOR3_HOLD_X
|  8 | MOTOR4_HOLD_X
|  9 | MOTOR5_HOLD_X
|  10 | MOTOR6_HOLD_X
|  11 | MOTOR7_HOLD_X
|  12 | MOTOR8_HOLD_X
|  13 | MOTOR9_HOLD_X
|  14 | MOTOR10_HOLD_X
|  15 | MOTOR11_HOLD_X
|  16 | MOTOR12_HOLD_X
|  17..62 | Unused
|   63 | SE_REG_LB | 31..0 | Loopback from output 63


Interrupts
==========

|Number | Name | Description
|------ | ---- | -----------
| 0 | BE_DONE | Buf Executor done (due to BUF_DONE)
| 1 | ASG_LOAD | Current accel cycle is almost done, load of next cycle params required
| 2 | ASG_DONE | Last cycle is done
| 3 | ASG_ABORT | ASG requested abort due to buffer underflow/etc
| 2..7| Unused
| 8..15 | APG_ABORTS_DONE | Aborts for corresponding channel are done
| 16..30| Unused
| 31 | SE_INT_LB | Looped back to Strobe 31


Strobes
=======

|Number | Name | Description
|------ | ---- | -----------
| 0| BE start
| 1| BE abort
| 2| ASG start
| 3| ASG abort
| 4| ASG load done
| 5| SP zero | set x=0 for all SPs
| 6| MSG set X | set x=MSG_X_VAL for selected by MSG_CONFIG channels
| 7| ES unlock
| 8..15| Abort APG channel 0..7
| 8..30| Unused
| 31 | SE_INT_LB | Looped back to Int 31


S3G proto
============

Request
-------

| Offset | Size | Description
|-------|------|-------------
|   0   |    1 |  0xD5 - header
|   1   |    1 |  Payload length (N)
|   2   |    2     |  Tag - will be copied to reply
|   4   |    1     |  Command Code
|   5   |    N - 3 |  Arguments
|  N + 1|   1      | CRC

Reply
-----

| Offset | Size | Description
|-------|------|-------------
|   0   |    1 |  0xD5 - header
|   1   |    1 |  Payload length (N)
|   2   |    2     |  Tag - copied from request or 0xFFFF
|   4   |    1     |  Reply Code
|   5   |    N - 3 |  Arguments
|  N + 1|   1      | CRC

Reply Codes
-----------
|Code | Name | Description
|-----|------|------------
|  80 | Interrupt | Interrupt report (originated by device)
| 0x80  | Error   | Error
| 0x81  | OK   | Success, can be followed by reply args
| 0x82  | BufError   | Error writing to buf_exec memory because of new command arrival
| 0x85  | Unknown | Unknown command

Command Codes
-------------

|Command | CMD | Name | Args | Reply
|--------|-----|------|------|-------
|  0     | VERSION  | Version | -- |  OK 0xBA 0xCE
|  27    | EXT_VER  | Extended Version | -- | OK 0x01 0x00 0x01 0x00 0xCE 0x00 0x00 0x00
|  60    | OUTPUT  | Write output | 0: reg num 1..4: value | OK
|  61    | INPUT  | Read input | 0: input num | OK 0..3: Value
|  62    | STB   | Send Strobes | 0..3: Mask | OK
|  63    | CLEAR  | Clear pending interrupts| 0..3: Mask
|  64    | MASK  | Mask interrupts| 0..3: Mask
|  65    | Unused (was WRITE_BUFFER in old version)
|  66    | WRITE_BUFFER | Write buf_exec memory| 0: Word count 1..1+N*5: Data| {OK, BufError} 0..3: Fifo free space

Buf Executor Commands
=====================

|Format | Name | Description
|-------|------|-------------
|0 0 X:6 X:32 | Unused
|0 1 reg_num:6 value:32 | OUTPUT | Write value to output
|1 0 0:6 X:32 | NOP | Nop
|1 0 1:6 mask:32 | STB | Send STBs
|1 0 2:6 mask:32 | WAIT_ALL | Wait for all Ints
|1 0 3:6 mask:32 | WAIT_ANY | Wait for any of Ints
|1 0 4:6 mask:32 | CLEAR | Clear INTs
|1 0 5:6 int_ext:1 value:31 | WAIT_FIFO | Wait while local or external fifo has enough data inside
|1 0 6:6 X:24 addr:8 | PARAM_ADDR | Set address pointer for APG param store
|1 0 7:6 value:32 | PARAM_WRITE_HI | Write to high 32 bits of current address
|1 0 8:6 value:32 | PARAM_WRITE_LO | Write to low 32 bits of current address, and keep it as is
|1 0 9-14:6 value:32 | PARAM_WRITE_LO_{N} | Increment current address for {N} and write to low 32 bits
|1 0 15:6 value:32 | PARAM_WRITE_LO_NC | Increment current address to 0 of next channel(32 values block) and write to low 32 bits
|1 0 5-62:6 X:32 | Unused
|1 0 63:6 X:32 | DONE | Halt and report
|1 1 X:6 X:32 | Unused

