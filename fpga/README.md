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
| 15 | APG_X_ABORT_A_VAL | 31..0 | X channel abort acceleration value
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


Utilization for single full channel
===================================

```
Device Utilization Summary:

Slice Logic Utilization:
  Number of Slice Registers:                 1,395 out of  11,440   12%
    Number used as Flip Flops:               1,395
    Number used as Latches:                      0
    Number used as Latch-thrus:                  0
    Number used as AND/OR logics:                0
  Number of Slice LUTs:                      2,315 out of   5,720   40%
    Number used as logic:                    2,303 out of   5,720   40%
      Number using O6 output only:           1,690
      Number using O5 output only:             122
      Number using O5 and O6:                  491
      Number used as ROM:                        0
    Number used as Memory:                       2 out of   1,440    1%
      Number used as Dual Port RAM:              0
      Number used as Single Port RAM:            0
      Number used as Shift Register:             2
        Number using O6 output only:             2
        Number using O5 output only:             0
        Number using O5 and O6:                  0
    Number used exclusively as route-thrus:     10
      Number with same-slice register load:      5
      Number with same-slice carry load:         5
      Number with other load:                    0

Slice Logic Distribution:
  Number of occupied Slices:                   712 out of   1,430   49%
  Nummber of MUXCYs used:                      764 out of   2,860   26%
  Number of LUT Flip Flop pairs used:        2,524
    Number with an unused Flip Flop:         1,180 out of   2,524   46%
    Number with an unused LUT:                 209 out of   2,524    8%
    Number of fully used LUT-FF pairs:       1,135 out of   2,524   44%
    Number of slice register sites lost
      to control set restrictions:               0 out of  11,440    0%

  A LUT Flip Flop pair for this architecture represents one LUT paired with
  one Flip Flop within a slice.  A control set is a unique combination of
  clock, reset, set, and enable signals for a registered element.
  The Slice Logic Distribution report is not meaningful if the design is
  over-mapped for a non-slice resource or if Placement fails.

IO Utilization:
  Number of bonded IOBs:                        23 out of     102   22%
    Number of LOCed IOBs:                       20 out of      23   86%
    IOB Flip Flops:                              1

Specific Feature Utilization:
  Number of RAMB16BWERs:                        21 out of      32   65%
  Number of RAMB8BWERs:                          0 out of      64    0%
  Number of BUFIO2/BUFIO2_2CLKs:                 0 out of      32    0%
  Number of BUFIO2FB/BUFIO2FB_2CLKs:             0 out of      32    0%
  Number of BUFG/BUFGMUXs:                       1 out of      16    6%
    Number used as BUFGs:                        1
    Number used as BUFGMUX:                      0
  Number of DCM/DCM_CLKGENs:                     0 out of       4    0%
  Number of ILOGIC2/ISERDES2s:                   0 out of     200    0%
  Number of IODELAY2/IODRP2/IODRP2_MCBs:         0 out of     200    0%
  Number of OLOGIC2/OSERDES2s:                   1 out of     200    1%
    Number used as OLOGIC2s:                     1
    Number used as OSERDES2s:                    0
  Number of BSCANs:                              0 out of       4    0%
  Number of BUFHs:                               0 out of     128    0%
  Number of BUFPLLs:                             0 out of       8    0%
  Number of BUFPLL_MCBs:                         0 out of       4    0%
  Number of DSP48A1s:                            0 out of      16    0%
  Number of ICAPs:                               0 out of       1    0%
  Number of MCBs:                                0 out of       2    0%
  Number of PCILOGICSEs:                         0 out of       2    0%
  Number of PLL_ADVs:                            0 out of       2    0%
  Number of PMVs:                                0 out of       1    0%
  Number of STARTUPs:                            0 out of       1    0%
  Number of SUSPEND_SYNCs:                       0 out of       1    0%
```

Utilization for two full channels
===================================

```
Device Utilization Summary:

Slice Logic Utilization:
  Number of Slice Registers:                 1,856 out of  11,440   16%
    Number used as Flip Flops:               1,856
    Number used as Latches:                      0
    Number used as Latch-thrus:                  0
    Number used as AND/OR logics:                0
  Number of Slice LUTs:                      3,304 out of   5,720   57%
    Number used as logic:                    3,291 out of   5,720   57%
      Number using O6 output only:           2,336
      Number using O5 output only:             152
      Number using O5 and O6:                  803
      Number used as ROM:                        0
    Number used as Memory:                       2 out of   1,440    1%
      Number used as Dual Port RAM:              0
      Number used as Single Port RAM:            0
      Number used as Shift Register:             2
        Number using O6 output only:             2
        Number using O5 output only:             0
        Number using O5 and O6:                  0
    Number used exclusively as route-thrus:     11
      Number with same-slice register load:      5
      Number with same-slice carry load:         6
      Number with other load:                    0

Slice Logic Distribution:
  Number of occupied Slices:                 1,010 out of   1,430   70%
  Nummber of MUXCYs used:                    1,272 out of   2,860   44%
  Number of LUT Flip Flop pairs used:        3,508
    Number with an unused Flip Flop:         1,779 out of   3,508   50%
    Number with an unused LUT:                 204 out of   3,508    5%
    Number of fully used LUT-FF pairs:       1,525 out of   3,508   43%
    Number of slice register sites lost
      to control set restrictions:               0 out of  11,440    0%

  A LUT Flip Flop pair for this architecture represents one LUT paired with
  one Flip Flop within a slice.  A control set is a unique combination of
  clock, reset, set, and enable signals for a registered element.
  The Slice Logic Distribution report is not meaningful if the design is
  over-mapped for a non-slice resource or if Placement fails.

IO Utilization:
  Number of bonded IOBs:                        26 out of     102   25%
    Number of LOCed IOBs:                       20 out of      26   76%
    IOB Flip Flops:                              2

Specific Feature Utilization:
  Number of RAMB16BWERs:                        21 out of      32   65%
  Number of RAMB8BWERs:                          0 out of      64    0%
  Number of BUFIO2/BUFIO2_2CLKs:                 0 out of      32    0%
  Number of BUFIO2FB/BUFIO2FB_2CLKs:             0 out of      32    0%
  Number of BUFG/BUFGMUXs:                       1 out of      16    6%
    Number used as BUFGs:                        1
    Number used as BUFGMUX:                      0
  Number of DCM/DCM_CLKGENs:                     0 out of       4    0%
  Number of ILOGIC2/ISERDES2s:                   0 out of     200    0%
  Number of IODELAY2/IODRP2/IODRP2_MCBs:         0 out of     200    0%
  Number of OLOGIC2/OSERDES2s:                   2 out of     200    1%
    Number used as OLOGIC2s:                     2
    Number used as OSERDES2s:                    0
  Number of BSCANs:                              0 out of       4    0%
  Number of BUFHs:                               0 out of     128    0%
  Number of BUFPLLs:                             0 out of       8    0%
  Number of BUFPLL_MCBs:                         0 out of       4    0%
  Number of DSP48A1s:                            0 out of      16    0%
  Number of ICAPs:                               0 out of       1    0%
  Number of MCBs:                                0 out of       2    0%
  Number of PCILOGICSEs:                         0 out of       2    0%
  Number of PLL_ADVs:                            0 out of       2    0%
  Number of PMVs:                                0 out of       1    0%
  Number of STARTUPs:                            0 out of       1    0%
  Number of SUSPEND_SYNCs:                       0 out of       1    0%
```
