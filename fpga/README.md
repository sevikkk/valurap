Abbrevs
=======

* ASG - Acceleration step generator
* APG - Acceleration profile generator
* MSG - Motor step generator
* BE - buffer commands executor
* SE - S3G commands executor

Outputs
=======

|Number | Name | Bits | Description
|------ | ---- | ---- | -----------
|0  |  LEDS | 7..0 | On-board LEDs
|  |        | 31..8 | Unused
|1  |  ASG_STEPS_VAL | 31..0 | Number of steps in current acceleration cycle
|2  | ASG_DT_VAL | 31..0 | Length of each step in current cycle in clocks
|3  | ASG_CONTROL | 0 | Set steps limit
|   |             | 1 | Set DT limit
|   |             | 2 | Reset steps
|   |             | 3 | Reset DT
|   |             | 4..7 | Unused
|   |             | 8 | APG_X set X
|   |             | 9 | APG_X set V
|   |             | 10 | APG_X set A
|   |             | 11 | APG_X set J
|   |             | 12 | APG_X set JJ
|   |             | 13 | APG_X set target V
| 4 | MSG_ALL_PRE_N | 31..0 | Length of pre-pulse (after potential direction switch)
| 5 | MSG_ALL_PULSE_N | 31..0 | Length of pulse
| 6 | MSG_ALL_POST_N | 31..0 | Length of post-pulse
| 7 | MSG_CONTROL | 0 | X-motor enable (inverted output, 0 - disabled, 1 - enabled)
|   |             | 31..1 | Unused
| 8 | APG_X_X_VAL_LO | 31..0 | X channel X value (lower half)
| 9 | APG_X_X_VAL_HI | 31..0 | X channel X value (higher half)
| 10 | APG_X_V_VAL | 31..0 | X channel V value
| 11 | APG_X_A_VAL | 31..0 | X channel A value
| 12 | APG_X_J_VAL | 31..0 | X channel J value
| 13 | APG_X_JJ_VAL | 31..0 | X channel JJ value
| 14 | APG_X_TARGET_V_VAL | 31..0 | X channel target velocity value
| 15 | APG_X_ABORT_A | 31..0 | X channel abort acceleration value
|16..61| Unused
|62 | BE_START_ADDR | 15..0 | Start address for buf_exec
|63 | SE_REG_LB | 31..0| Looped back to Input 63
 
Inputs
======

| Number | Name | Bits | Description
| ------ | ---- | ---- | -----------
|  0 | ASG_DT | 31..0 | Current accel step clock number
|  1 | ASG_STEP | 31..0 | Current step in accel cycle
|  2..61 | Unused
|  62 | BE_CONTROL | 31 | BE_BUSY - buf_exec is executing
|      |          | 30 | BE_WAITING - buf_exec is waiting for interrupt
|      |          |29..24| Unused
|      |          | 23..16 | BE_ERROR - current error code
|      |          | 15..0 | BE_PC - current PC of buf_exec
|   63 | SE_REG_LB | 31..0 | Loopback from output 63


Interrupts
==========

|Number | Name | Description
|------ | ---- | -----------
| 0 | ASG_DONE | Current accel cycle is done, load required
| 1 | ASG_ABORT | Aborting current activity as new params were not loaded in time
| 2..29| Unused
| 30 | BE_COMPLETE | buf_exec done executing
| 31 | SE_INT_LB | Looped back to Strobe 0


Strobes
=======

|Number | Name | Description
|------ | ---- | -----------
| 0 | ASG_LOAD | Load parameters of current accel cycle
| 1..28| Unused
| 29 | BE_START | Start execution for buf_exec
| 30 | BE_ABORT | Abort buf_exec execution
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
|  65    | WRITE_BUFFER | Write buf_exec memory| 0: Word count 1..2: Offset 3..3+N*5: Data| {OK, BufError} 0..1: Addr 2: Curent Error 3..4: PC

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
|1 0 4:6 masK:32 | CLEAR | Clear INTs
|1 0 5-62:6 X:32 | Unused
|1 0 63:6 X:32 | DONE | Halt and report
|1 1 X:6 X:32 | Unused

