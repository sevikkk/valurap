#!/usr/bin/env python

import time

from valurap.oled import OLED
from valurap.spi import SPIPort
from valurap.commands import S3GPort


def home_x1():
    spi = SPIPort()
    spi.setup_tmc2130()

    oled = OLED()

    with oled.draw() as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "Start", fill="white")

    bot = S3GPort()
    bot.S3G_CLEAR(-1)
    bot.S3G_CLEAR(-1)
    bot.S3G_OUTPUT(bot.OUT_LEDS, 0x55)
    bot.S3G_OUTPUT(bot.OUT_MSG_CONTROL,
                   bot.OUT_MSG_CONTROL_ENABLE_3 |
                   bot.OUT_MSG_CONTROL_MUX_3_X
                   )
    bot.S3G_OUTPUT(bot.OUT_ENDSTOPS_OPTIONS,
                   bot.OUT_ENDSTOPS_OPTIONS_MUX_2_X |
                   bot.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_2 |
                   bot.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_2
                   )
    bot.S3G_STB(bot.STB_ENDSTOPS_UNLOCK)
    time.sleep(0.5)
    bot.S3G_WRITE_BUFFER(
        0,
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1),

        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PRE_N, 100), # 10 ms on step cycle - 2-6-2 ms
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PULSE_N, 500),
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_POST_N, 600),

        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 50000), # 1 kHz acceleration steps
        bot.BUF_OUTPUT(bot.OUT_APG_X_ABORT_A_VAL, 20000),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_ABORT_A_VAL, 20000),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_ABORT_A_VAL, 20000),

        bot.BUF_OUTPUT(bot.OUT_ENDSTOPS_TIMEOUT, 50000),

        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x2),

        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 50000), # 5 seconds
        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                       bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                       bot.OUT_ASG_CONTROL_SET_DT_LIMIT,
                       bot.OUT_ASG_CONTROL_RESET_STEPS,
                       bot.OUT_ASG_CONTROL_RESET_DT,

                       bot.OUT_ASG_CONTROL_APG_X_SET_JJ,
                       bot.OUT_ASG_CONTROL_APG_X_SET_J,
                       bot.OUT_ASG_CONTROL_APG_X_SET_A,
                       bot.OUT_ASG_CONTROL_APG_X_SET_V,
                       bot.OUT_ASG_CONTROL_APG_X_SET_X,
                       bot.OUT_ASG_CONTROL_APG_X_SET_TARGET_V,
                       ),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_LO, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_HI, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_V_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 5000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_J_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_JJ_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL, 500000),

        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_DONE()
    )
    bot.S3G_OUTPUT(bot.OUT_BE_START_ADDR, 0)
    bot.S3G_MASK(0)
    bot.S3G_STB(bot.STB_BE_START)
    prev_cycles = [0, 0, 0]
    try:
        while 1:
            new_cycles = []
            dump = []
            for i, (addr_s, addr_p) in enumerate([
                (bot.IN_ENDSTOPS_STATUS_1, bot.IN_ENDSTOPS_POS_HI_1),
                (bot.IN_ENDSTOPS_STATUS_2, bot.IN_ENDSTOPS_POS_HI_2),
                (bot.IN_ENDSTOPS_STATUS_3, bot.IN_ENDSTOPS_POS_HI_3),
            ]):
                status = bot.S3G_INPUT(addr_s)
                pos = bot.S3G_INPUT(addr_p)
                cycles = (status & 0xff00) >> 8
                value = status & 0x1
                dump.append((cycles, value, pos))
                new_cycles.append(cycles)

            print(dump)
            if new_cycles != prev_cycles:
                print("Send Unlock")
                bot.S3G_STB(bot.STB_ENDSTOPS_UNLOCK)
                prev_cycles = new_cycles

    except KeyboardInterrupt:
        pass

    bot.S3G_STB(bot.STB_BE_ABORT)
    bot.S3G_CLEAR(-1)
    bot.S3G_OUTPUT(bot.OUT_MSG_CONTROL, 0)

def home_x2():
    spi = SPIPort()
    spi.setup_tmc2130()

    oled = OLED()

    with oled.draw() as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "Start", fill="white")

    bot = S3GPort()
    bot.S3G_CLEAR(-1)
    bot.S3G_CLEAR(-1)
    bot.S3G_OUTPUT(bot.OUT_LEDS, 0x55)
    bot.S3G_OUTPUT(bot.OUT_MSG_CONTROL,
                   bot.OUT_MSG_CONTROL_ENABLE_4 |
                   bot.OUT_MSG_CONTROL_MUX_4_X |
                   bot.OUT_MSG_CONTROL_INVERT_DIR_4
                   )
    bot.S3G_OUTPUT(bot.OUT_ENDSTOPS_OPTIONS,
                   bot.OUT_ENDSTOPS_OPTIONS_MUX_1_X |
                   bot.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_1 |
                   bot.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_1
                   )
    bot.S3G_STB(bot.STB_ENDSTOPS_UNLOCK)
    time.sleep(0.5)
    bot.S3G_WRITE_BUFFER(
        0,
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1),

        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PRE_N, 100), # 10 ms on step cycle - 2-6-2 ms
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PULSE_N, 500),
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_POST_N, 600),

        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 50000), # 1 kHz acceleration steps
        bot.BUF_OUTPUT(bot.OUT_APG_X_ABORT_A_VAL, 20000),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_ABORT_A_VAL, 20000),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_ABORT_A_VAL, 20000),

        bot.BUF_OUTPUT(bot.OUT_ENDSTOPS_TIMEOUT, 50000),

        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x2),

        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 50000), # 5 seconds
        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                       bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                       bot.OUT_ASG_CONTROL_SET_DT_LIMIT,
                       bot.OUT_ASG_CONTROL_RESET_STEPS,
                       bot.OUT_ASG_CONTROL_RESET_DT,

                       bot.OUT_ASG_CONTROL_APG_X_SET_JJ,
                       bot.OUT_ASG_CONTROL_APG_X_SET_J,
                       bot.OUT_ASG_CONTROL_APG_X_SET_A,
                       bot.OUT_ASG_CONTROL_APG_X_SET_V,
                       bot.OUT_ASG_CONTROL_APG_X_SET_X,
                       bot.OUT_ASG_CONTROL_APG_X_SET_TARGET_V,
                       ),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_LO, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_HI, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_V_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 5000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_J_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_JJ_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL, 500000),

        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_DONE()
    )
    bot.S3G_OUTPUT(bot.OUT_BE_START_ADDR, 0)
    bot.S3G_MASK(0)
    bot.S3G_STB(bot.STB_BE_START)
    prev_cycles = [0, 0, 0]
    try:
        while 1:
            new_cycles = []
            dump = []
            for i, (addr_s, addr_p) in enumerate([
                (bot.IN_ENDSTOPS_STATUS_1, bot.IN_ENDSTOPS_POS_HI_1),
                (bot.IN_ENDSTOPS_STATUS_2, bot.IN_ENDSTOPS_POS_HI_2),
                (bot.IN_ENDSTOPS_STATUS_3, bot.IN_ENDSTOPS_POS_HI_3),
            ]):
                status = bot.S3G_INPUT(addr_s)
                pos = bot.S3G_INPUT(addr_p)
                cycles = (status & 0xff00) >> 8
                value = status & 0x1
                dump.append((cycles, value, pos))
                new_cycles.append(cycles)

            print(dump)
            if new_cycles != prev_cycles:
                print("Send Unlock")
                bot.S3G_STB(bot.STB_ENDSTOPS_UNLOCK)
                prev_cycles = new_cycles

    except KeyboardInterrupt:
        pass

    bot.S3G_STB(bot.STB_BE_ABORT)
    bot.S3G_CLEAR(-1)
    bot.S3G_OUTPUT(bot.OUT_MSG_CONTROL, 0)


def home_y():
    spi = SPIPort()
    spi.setup_tmc2130()

    oled = OLED()

    with oled.draw() as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "Start", fill="white")

    bot = S3GPort()
    bot.S3G_CLEAR(-1)
    bot.S3G_CLEAR(-1)
    bot.S3G_OUTPUT(bot.OUT_LEDS, 0x55)
    bot.S3G_OUTPUT(bot.OUT_MSG_CONTROL,
                   bot.OUT_MSG_CONTROL_ENABLE_1 |
                   bot.OUT_MSG_CONTROL_MUX_1_X |
                   bot.OUT_MSG_CONTROL_INVERT_DIR_1 |
                   bot.OUT_MSG_CONTROL_ENABLE_2 |
                   bot.OUT_MSG_CONTROL_MUX_2_X
                   )
    bot.S3G_OUTPUT(bot.OUT_ENDSTOPS_OPTIONS,
                   bot.OUT_ENDSTOPS_OPTIONS_MUX_3_X |
                   bot.OUT_ENDSTOPS_OPTIONS_ABORT_ENABLED_3 |
                   bot.OUT_ENDSTOPS_OPTIONS_ABORT_POLARITY_3
                   )
    bot.S3G_STB(bot.STB_ENDSTOPS_UNLOCK)
    time.sleep(0.5)
    bot.S3G_WRITE_BUFFER(
        0,
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1),

        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PRE_N, 100), # 10 ms on step cycle - 2-6-2 ms
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PULSE_N, 500),
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_POST_N, 600),

        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 50000), # 1 kHz acceleration steps
        bot.BUF_OUTPUT(bot.OUT_APG_X_ABORT_A_VAL, 20000),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_ABORT_A_VAL, 20000),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_ABORT_A_VAL, 20000),

        bot.BUF_OUTPUT(bot.OUT_ENDSTOPS_TIMEOUT, 50000),

        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x2),

        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 50000), # 5 seconds
        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                       bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                       bot.OUT_ASG_CONTROL_SET_DT_LIMIT,
                       bot.OUT_ASG_CONTROL_RESET_STEPS,
                       bot.OUT_ASG_CONTROL_RESET_DT,

                       bot.OUT_ASG_CONTROL_APG_X_SET_JJ,
                       bot.OUT_ASG_CONTROL_APG_X_SET_J,
                       bot.OUT_ASG_CONTROL_APG_X_SET_A,
                       bot.OUT_ASG_CONTROL_APG_X_SET_V,
                       bot.OUT_ASG_CONTROL_APG_X_SET_X,
                       bot.OUT_ASG_CONTROL_APG_X_SET_TARGET_V,
                       ),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_LO, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_HI, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_V_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 5000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_J_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_JJ_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL, 500000),

        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_DONE()
    )
    bot.S3G_OUTPUT(bot.OUT_BE_START_ADDR, 0)
    bot.S3G_MASK(0)
    bot.S3G_STB(bot.STB_BE_START)
    prev_cycles = [0, 0, 0]
    try:
        while 1:
            new_cycles = []
            dump = []
            for i, (addr_s, addr_p) in enumerate([
                (bot.IN_ENDSTOPS_STATUS_1, bot.IN_ENDSTOPS_POS_HI_1),
                (bot.IN_ENDSTOPS_STATUS_2, bot.IN_ENDSTOPS_POS_HI_2),
                (bot.IN_ENDSTOPS_STATUS_3, bot.IN_ENDSTOPS_POS_HI_3),
            ]):
                status = bot.S3G_INPUT(addr_s)
                pos = bot.S3G_INPUT(addr_p)
                cycles = (status & 0xff00) >> 8
                value = status & 0x1
                dump.append((cycles, value, pos))
                new_cycles.append(cycles)

            print(dump)
            if new_cycles != prev_cycles:
                print("Send Unlock")
                bot.S3G_STB(bot.STB_ENDSTOPS_UNLOCK)
                prev_cycles = new_cycles

    except KeyboardInterrupt:
        pass

    bot.S3G_STB(bot.STB_BE_ABORT)
    bot.S3G_CLEAR(-1)
    bot.S3G_OUTPUT(bot.OUT_MSG_CONTROL, 0)


if __name__ == "__main__":
    home_y()
