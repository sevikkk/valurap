#!/usr/bin/env python

import time


from valurap.oled import OLED
from valurap.spi import SPIPort
from valurap.commands import S3GPort


def test_leds():
    bot = S3GPort()
    oled = OLED()

    bot.S3G_CLEAR(-1)

    i = 0
    while 1:
        bot.S3G_OUTPUT(bot.OUT_LEDS, i)
        bot.S3G_OUTPUT(bot.OUT_SE_REG_LB, i)
        r = bot.S3G_INPUT(bot.IN_SE_REG_LB)
        if i != r:
            print(i, r)
        i = (i + 1) % 256
        with oled.draw() as draw:
            draw.rectangle(oled.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "i: {:3d}".format(i), fill="white")


def test_executor():
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
    bot.S3G_WRITE_BUFFER(
        0,
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1),

        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PRE_N, 100), # 10 ms on step cycle - 2-6-2 ms
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PULSE_N, 500),
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_POST_N, 600),

        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 50000), # 1 kHz acceleration steps
        bot.BUF_OUTPUT(bot.OUT_APG_X_ABORT_A_VAL, 100),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_ABORT_A_VAL, 100),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_ABORT_A_VAL, 100),

        bot.BUF_OUTPUT(bot.OUT_MSG_CONTROL,
                       bot.OUT_MSG_CONTROL_ENABLE_1,
                       bot.OUT_MSG_CONTROL_MUX_1_X,
                       bot.OUT_MSG_CONTROL_ENABLE_2,
                       bot.OUT_MSG_CONTROL_MUX_2_Y,
                       bot.OUT_MSG_CONTROL_ENABLE_3,
                       bot.OUT_MSG_CONTROL_MUX_3_Z,
                       bot.OUT_MSG_CONTROL_ENABLE_6,
                       bot.OUT_MSG_CONTROL_MUX_6_X,
                       bot.OUT_MSG_CONTROL_ENABLE_5,
                       bot.OUT_MSG_CONTROL_MUX_5_Y,
                       bot.OUT_MSG_CONTROL_ENABLE_4,
                       bot.OUT_MSG_CONTROL_MUX_4_Z,
                       ),

        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 10000), # 0.5 seconds
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

                        bot.OUT_ASG_CONTROL_APG_Y_SET_JJ,
                        bot.OUT_ASG_CONTROL_APG_Y_SET_J,
                        bot.OUT_ASG_CONTROL_APG_Y_SET_A,
                        bot.OUT_ASG_CONTROL_APG_Y_SET_V,
                        bot.OUT_ASG_CONTROL_APG_Y_SET_X,
                        bot.OUT_ASG_CONTROL_APG_Y_SET_TARGET_V,

                        bot.OUT_ASG_CONTROL_APG_Z_SET_JJ,
                        bot.OUT_ASG_CONTROL_APG_Z_SET_J,
                        bot.OUT_ASG_CONTROL_APG_Z_SET_A,
                        bot.OUT_ASG_CONTROL_APG_Z_SET_V,
                        bot.OUT_ASG_CONTROL_APG_Z_SET_X,
                        bot.OUT_ASG_CONTROL_APG_Z_SET_TARGET_V
                       ),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_LO, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_X_VAL_HI, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_V_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 200),
        bot.BUF_OUTPUT(bot.OUT_APG_X_J_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_JJ_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL,2000000),

        bot.BUF_OUTPUT(bot.OUT_APG_Y_X_VAL_LO, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_X_VAL_HI, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_V_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_A_VAL, 200),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_J_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_JJ_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_TARGET_V_VAL,1000000),

        bot.BUF_OUTPUT(bot.OUT_APG_Z_X_VAL_LO, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_X_VAL_HI, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_V_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_A_VAL, 200),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_J_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_JJ_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_TARGET_V_VAL,1500000),

        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                         bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                         bot.OUT_ASG_CONTROL_RESET_STEPS,
                         bot.OUT_ASG_CONTROL_APG_X_SET_A,
                         bot.OUT_ASG_CONTROL_APG_Y_SET_A,
                         bot.OUT_ASG_CONTROL_APG_Z_SET_A
                        ),
        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 3000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_A_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_A_VAL, 0),

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x3),

        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                       bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT |
                       bot.OUT_ASG_CONTROL_RESET_STEPS |
                       bot.OUT_ASG_CONTROL_APG_X_SET_A |
                       bot.OUT_ASG_CONTROL_APG_X_SET_TARGET_V |
                       bot.OUT_ASG_CONTROL_APG_Y_SET_A |
                       bot.OUT_ASG_CONTROL_APG_Y_SET_TARGET_V |
                       bot.OUT_ASG_CONTROL_APG_Z_SET_A |
                       bot.OUT_ASG_CONTROL_APG_Z_SET_TARGET_V
                       ),
        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 10000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, -600),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL, -1000000),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_A_VAL, -600),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_TARGET_V_VAL, -2000000),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_A_VAL, -600),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_TARGET_V_VAL, -1500000),

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x7),

        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                       bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT |
                       bot.OUT_ASG_CONTROL_RESET_STEPS |
                       bot.OUT_ASG_CONTROL_APG_X_SET_A |
                       bot.OUT_ASG_CONTROL_APG_X_SET_TARGET_V |
                       bot.OUT_ASG_CONTROL_APG_Y_SET_A |
                       bot.OUT_ASG_CONTROL_APG_Y_SET_TARGET_V |
                       bot.OUT_ASG_CONTROL_APG_Z_SET_A |
                       bot.OUT_ASG_CONTROL_APG_Z_SET_TARGET_V
                       ),
        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 10000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 300),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_A_VAL, 300),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_TARGET_V_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_A_VAL, 300),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_TARGET_V_VAL, 0),

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0xF),

        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                        bot.OUT_ASG_CONTROL_SET_DT_LIMIT
                        ),
        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 0), # 1 kHz acceleration steps

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1F),
        bot.BUF_OUTPUT(bot.OUT_MSG_CONTROL, 0),
        bot.BUF_DONE()
    )
    bot.S3G_OUTPUT(bot.OUT_BE_START_ADDR, 0)
    bot.S3G_MASK(0)
    bot.S3G_STB(bot.STB_BE_START)
    while 1:
        status = bot.S3G_INPUT(62)
        busy = (status & 0x80000000) >> 31
        waiting = (status & 0x40000000) >> 30
        error = (status & 0x00FF0000)>>16
        pc = status & 0x0000FFFF
        print("%8X" % status)
        with oled.draw() as draw:
            draw.rectangle(oled.bounding_box, outline="white", fill="black")
            draw.multiline_text((10, 10), "Busy: {} Wait: {}\nError: {} \nPC: {}".format(busy, waiting, error, pc), fill="white")
        time.sleep(0.1)
        if status > 0:
            break

    bot.S3G_CLEAR(-1)
    time.sleep(1)
    with oled.draw() as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "Done", fill="white")


def test_spi():
    spi = SPIPort()
    a = spi.dev.xfer2([0x0,0,0,0,0]*6)
    print(a)
    a = spi.dev.xfer2([0x0,0,0,0,0]*6)
    print(a)


def test_real_y():
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
    bot.S3G_WRITE_BUFFER(
        0,
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1),

        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PRE_N, 100), # 10 ms on step cycle - 2-6-2 ms
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PULSE_N, 500),
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_POST_N, 600),

        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 50000), # 1 kHz acceleration steps
        bot.BUF_OUTPUT(bot.OUT_APG_X_ABORT_A_VAL, 100),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_ABORT_A_VAL, 100),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_ABORT_A_VAL, 100),

        bot.BUF_OUTPUT(bot.OUT_MSG_CONTROL,
                       bot.OUT_MSG_CONTROL_ENABLE_1,
                       bot.OUT_MSG_CONTROL_MUX_1_X,
                       bot.OUT_MSG_CONTROL_ENABLE_2,
                       bot.OUT_MSG_CONTROL_MUX_2_X,
                       bot.OUT_MSG_CONTROL_INVERT_DIR_2
                       ),

        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 500), # 1 second
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
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 15000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_J_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_JJ_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL,2500000),

        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                         bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                         bot.OUT_ASG_CONTROL_RESET_STEPS,
                         bot.OUT_ASG_CONTROL_APG_X_SET_A,
                        ),
        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 1000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 0),

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x3),

        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                       bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                       bot.OUT_ASG_CONTROL_RESET_STEPS,
                       bot.OUT_ASG_CONTROL_APG_X_SET_A,
                       bot.OUT_ASG_CONTROL_APG_X_SET_TARGET_V,
                       ),
        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 1000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, -60000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL, 0),

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x7),

        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                        bot.OUT_ASG_CONTROL_SET_DT_LIMIT
                        ),
        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 0), # 1 kHz acceleration steps

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1F),
        bot.BUF_OUTPUT(bot.OUT_MSG_CONTROL, 0),
        bot.BUF_DONE()
    )
    bot.S3G_OUTPUT(bot.OUT_BE_START_ADDR, 0)
    bot.S3G_MASK(0)
    bot.S3G_STB(bot.STB_BE_START)
    spi.dev.xfer2([0x6f, 0x0, 0x0, 0x0, 0x0] * 6)
    idx = 0
    while 1:
        res = spi.dev.xfer2([0x6f, 0x0, 0x0, 0x0, 0x0] * 6)
        stats = (res[25:30], res[20:25])
        ss = ["%3d" % idx]
        idx += 1
        for s,a,b,c,d in stats:
            status = []
            if a & 0x80: status.append("stand")
            if a & 0x4: status.append("otpw")
            if a & 0x2: status.append("ot")
            if a & 0x1: status.append("sg")
            if c & 0x80: status.append("fs")
            n = (c & 0x3) * 256 + d
            status.append("*" * (n/5))
 
            ss.append("%40s" % " ".join(status))
        print(" | ".join(ss))
        status = bot.S3G_INPUT(62)
        busy = (status & 0x80000000) >> 31
        waiting = (status & 0x40000000) >> 30
        error = (status & 0x00FF0000)>>16
        pc = status & 0x0000FFFF
        if 0:
            print("%8X" % status)
            with oled.draw() as draw:
                draw.rectangle(oled.bounding_box, outline="white", fill="black")
                draw.multiline_text((10, 10), "Busy: {} Wait: {}\nError: {} \nPC: {}".format(busy, waiting, error, pc), fill="white")
            time.sleep(0.1)
        if status > 0:
            break

    bot.S3G_CLEAR(-1)
    time.sleep(1)
    with oled.draw() as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "Done", fill="white")


def test_real_x():
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
    bot.S3G_WRITE_BUFFER(
        0,
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1),

        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PRE_N, 100), # 10 ms on step cycle - 2-6-2 ms
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_PULSE_N, 500),
        bot.BUF_OUTPUT(bot.OUT_MSG_ALL_POST_N, 600),

        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 50000), # 1 kHz acceleration steps
        bot.BUF_OUTPUT(bot.OUT_APG_X_ABORT_A_VAL, 100),
        bot.BUF_OUTPUT(bot.OUT_APG_Y_ABORT_A_VAL, 100),
        bot.BUF_OUTPUT(bot.OUT_APG_Z_ABORT_A_VAL, 100),

        bot.BUF_OUTPUT(bot.OUT_MSG_CONTROL,
                       bot.OUT_MSG_CONTROL_ENABLE_3,
                       bot.OUT_MSG_CONTROL_MUX_3_X,
                       #bot.OUT_MSG_CONTROL_INVERT_DIR_3,
                       #bot.OUT_MSG_CONTROL_ENABLE_4,
                       bot.OUT_MSG_CONTROL_MUX_4_X,
                       #bot.OUT_MSG_CONTROL_INVERT_DIR_4,
                       ),

        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 500), # 1 second
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
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 15000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_J_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_JJ_VAL, 0),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL,2000000),

        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                         bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                         bot.OUT_ASG_CONTROL_RESET_STEPS,
                         bot.OUT_ASG_CONTROL_APG_X_SET_A,
                        ),
        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 100),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, 0),

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x3),

        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                       bot.OUT_ASG_CONTROL_SET_STEPS_LIMIT,
                       bot.OUT_ASG_CONTROL_RESET_STEPS,
                       bot.OUT_ASG_CONTROL_APG_X_SET_A,
                       bot.OUT_ASG_CONTROL_APG_X_SET_TARGET_V,
                       ),
        bot.BUF_OUTPUT(bot.OUT_ASG_STEPS_VAL, 1000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_A_VAL, -60000),
        bot.BUF_OUTPUT(bot.OUT_APG_X_TARGET_V_VAL, 0),

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x7),

        bot.BUF_OUTPUT(bot.OUT_ASG_CONTROL,
                        bot.OUT_ASG_CONTROL_SET_DT_LIMIT
                        ),
        bot.BUF_OUTPUT(bot.OUT_ASG_DT_VAL, 0), # 1 kHz acceleration steps

        bot.BUF_WAIT_ALL(bot.INT_ASG_DONE),
        bot.BUF_CLEAR(bot.INT_ASG_DONE),
        bot.BUF_STB(bot.STB_ASG_LOAD),
        bot.BUF_OUTPUT(bot.OUT_LEDS, 0x1F),
        bot.BUF_OUTPUT(bot.OUT_MSG_CONTROL, 0),
        bot.BUF_DONE()
    )
    bot.S3G_OUTPUT(bot.OUT_BE_START_ADDR, 0)
    bot.S3G_MASK(0)
    bot.S3G_STB(bot.STB_BE_START)
    spi.dev.xfer2([0x6f, 0x0, 0x0, 0x0, 0x0] * 6)
    idx = 0
    while 1:
        res = spi.dev.xfer2([0x6f, 0x0, 0x0, 0x0, 0x0] * 6)
        stats = (res[25:30], res[20:25])
        ss = ["%3d" % idx]
        idx += 1
        for s,a,b,c,d in stats:
            status = []
            if a & 0x80: status.append("stand")
            if a & 0x4: status.append("otpw")
            if a & 0x2: status.append("ot")
            if a & 0x1: status.append("sg")
            if c & 0x80: status.append("fs")
            n = (c & 0x3) * 256 + d
            status.append("*" * (n/5))
 
            ss.append("%40s" % " ".join(status))
        print(" | ".join(ss))
        status = bot.S3G_INPUT(62)
        busy = (status & 0x80000000) >> 31
        waiting = (status & 0x40000000) >> 30
        error = (status & 0x00FF0000)>>16
        pc = status & 0x0000FFFF
        if 0:
            print("%8X" % status)
            with oled.draw() as draw:
                draw.rectangle(oled.bounding_box, outline="white", fill="black")
                draw.multiline_text((10, 10), "Busy: {} Wait: {}\nError: {} \nPC: {}".format(busy, waiting, error, pc), fill="white")
            time.sleep(0.1)
        if status > 0:
            break

    bot.S3G_CLEAR(-1)
    time.sleep(1)
    with oled.draw() as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "Done", fill="white")


if __name__ == "__main__":
    #test_leds()
    #test_executor()
    #test_spi()
    #test_real_y()
    test_real_x()
