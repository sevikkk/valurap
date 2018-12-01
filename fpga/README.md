Outputs
=======

Number | Name | Bits | Description
------ | ---- | ---- | -----------
  0  |  LEDS | 7..0 | On-board LEDs
  1  |  ASG_STEPS_VAL | 31..0 | Number of steps in current acceleration cycle
  2  | ASG_DT_VAL | 31..0 | Length of each step in current cycle in clocks
  3  | ASG_CONTROL | 0 | Set steps limit
     |  |             | 1 | Set DT limit
     |  |             | 2 | Reset steps
     |  |             | 3 | Reset DT
  ...| Unused
  62 | BE_START_ADDR | 15..0 | Start address for buf_exec
  63 | SE_REG_LB | 31..0| Looped back to Input 63
 
Inputs
======

Number | Name | Bits | Description
------ | ---- | ---- | -----------
 0 | ASG_DT | 31..0 | Current accel step clock number
 1 | ASG_STEP | 31..0 | Current step in accel cycle
 ... |
 62 | BE_CONTROL | 31 | BE_BUSY - buf_exec is eecuting
     | |         | 30 | BE_WAITING - buf_exec is waiting for int
     | |         |...|
     | |         | 23..16 | BE_ERROR - current error code
     | |         | 15..0 | BE_PC - current PC of bef_exec
  63 | SE_REG_LB | 31..0 | Loopback from output 63


Interrupts
==========

Number | Name | Description
------ | ---- | -----------
 0 | ASG_DONE | Current accel cycle is done, load required
 1 | ASG_ABORT | Aborting current activity as new params are not loaded in time
 ..| |
 30 | BE_COMPLETE | buf_exec done executing
 31 | SE_INT_LB | Looped back to Strobe 0


Strobes
==========

Number | Name | Description
------ | ---- | -----------
 0 | ASG_LOAD | Load parameters of current accel cycle
 ..|
 29 | BE_START | Start execution for buf_exec
 30 | BE_ABORT | Abort buf_exec execution
 31 | SE_INT_LB | Looped back to Int 31

