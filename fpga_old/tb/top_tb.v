`timescale 1ns/100ps

`include "../src/crc8.v"
`include "../src/mojo_top.v"
`include "../src/buf_executor.v"
`include "../src/s3g_executor.v"
`include "../src/s3g_rx.v"
`include "../src/s3g_tx.v"
`include "../src/cclk_detector.v"
`include "../src/dds_uart_clock.v"
`include "../src/uart_transceiver.v"
`include "../src/acc_step_gen.v"
`include "../src/motor_step_gen.v"
`include "../src/acc_profile_gen.v"
`include "../src/motor_mux.v"
`include "../src/debounce.v"
`include "../src/endstop_with_mux.v"
`include "../src/buf_cmds.v"

module top_tb;

reg clk;
reg rst_n;
reg cclk;
wire avr_tx;
wire avr_rx;

reg [63:0] cycle;

wire enable_16;
reg [7:0] tx_data;
reg tx_wr;
wire tx_done;
wire [7:0] avr_rx_data;
wire avr_rx_done;

reg [2047:0] packet = 512'hD50123456789;
reg send_packet = 0;

reg [8*256:0] rx_buffer = 0;

reg assertions_failed = 0;

reg stop_x1 = 0;
reg stop_x2 = 0;
reg stop_y = 0;

localparam BR=1000000;

dds_uart_clock uclock1(
                   .clk(clk),
                   .baudrate(BR/100),
                   .enable_16(enable_16)
               );

uart_transceiver uart1(
                     .sys_clk(clk),
                     .sys_rst(~rst_n),
                     .uart_rx(avr_rx),
                     .uart_tx(avr_tx),
                     .enable_16(enable_16),
                     .tx_data(tx_data),
                     .tx_wr(tx_wr),
                     .tx_done(tx_done),
                     .rx_data(avr_rx_data),
                     .rx_done(avr_rx_done)
                 );

always @(posedge clk)
    if (avr_rx_done) begin
        rx_buffer <= {rx_buffer , avr_rx_data};
        $display("time: %0d received %h", cycle, avr_rx_data);
    end

mojo_top #(
        .AVR_BAUD_RATE(BR),
        .EXT_BAUD_RATE(BR),
        .INTS_TIMER(15000)
    ) dut (
           .clk(clk),
           .rst_n(rst_n),
           .cclk(cclk),
           .avr_tx(avr_tx),
           .avr_rx(avr_rx),
           .endstop_x1(stop_x1),
           .endstop_x2(stop_x2),
           .endstop_y(stop_y)
       );

`define assert_rx(value) \
    begin if (rx_buffer != value) begin \
            $display("ASSERTION FAILED in %m at %0d: actual rx_buffer %h != expected %h", cycle, rx_buffer, value); \
            assertions_failed = 1; \
        end \
        rx_buffer = 0; \
    end

`define assert_signal(name, signal, value) \
    begin if (signal != value) begin \
            $display("ASSERTION FAILED in %m at %0d: actual %s %h != expected %h", cycle, name, signal, value); \
            assertions_failed = 1; \
        end \
    end


initial
    begin
        $dumpfile("test.vcd");
        $dumpvars;

        rst_n = 0;
        cclk = 0;
        clk = 0;
        tx_wr = 0;
        #10;
        clk = 1;
        #10;
        clk = 0;
        #10;
        clk = 1;
        #10;
        clk = 0;
        #6;
        rst_n = 1;
        #4;
        clk = 1;
        #10;
        clk = 0;
        #10;
        clk = 1;
        #10;
        clk = 0;
        #10;
        clk = 1;
        #10;
        clk = 0;
        #6;
        cclk = 1;
        #4;
        clk = 1;
        #10;
        clk = 0;
        #10;
        clk = 1;
        #10;
        clk = 0;
        #10;
        cycle = 0;
        forever
            begin
                clk = 1;
                #6;

                if (tx_wr == 1)
                    tx_wr = 0;

                case (cycle)
                    1500:
                        begin
                            tx_data = 8'hD5;
                            tx_wr = 1;
                        end
                    2600:
                        begin
                            tx_data = 8'h03;
                            tx_wr = 1;
                        end
                    3700:
                        begin
                            tx_data = 8'h80;
                            tx_wr = 1;
                        end
                    4800:
                        begin
                            tx_data = 8'h81;
                            tx_wr = 1;
                        end
                    5900:
                        begin
                            tx_data = 8'h00;
                            tx_wr = 1;
                        end
                    7000:
                        begin
                            tx_data = 8'h89;
                            tx_wr = 1;
                        end
                    12000: `assert_rx(128'hd505808181bace64)

                    15000:
                        begin
                            // Version request
                            packet = 128'hD503808100;
                            send_packet = 1;
                        end
                    23000: `assert_rx(128'hd505808181bace64)

                    25000:
                        begin
                            // Invalid command
                            packet = {8'hD5, 8'd7, 16'h1234, 40'h1213141516};
                            send_packet = 1;
                        end
                    34000: `assert_rx(128'hd503123485a0)

                    35000:
                        begin
                            // Write register 0 (Leds)
                            packet = buf_cmds.S3G_OUTPUT_T(0, 32'h78563412, 16'h2345);
                            send_packet = 1;
                        end
                    44500:
                        begin
                            `assert_rx(128'hd503234581c6)
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h12)
                        end

                    45000:
                        begin
                            // Write register 63 (Loop-back)
                            packet = {8'hD5, 8'd8, 16'h2716, 8'd60, 8'd63, 32'h13579BDF};
                            send_packet = 1;
                        end
                    54500:
                        begin
                            `assert_rx(128'hd5032716817a)
                            `assert_signal("Loop-back", dut.se_reg_lb, 32'hDF9B5713)
                        end

                    55000:
                        begin
                            // Read input 63 (Loop-back)
                            packet = {8'hD5, 8'd4, 16'h3355, 8'd61, 8'd63};
                            send_packet = 1;
                        end
                    64500:
                        begin
                            `assert_rx(128'hd50733558113579bdfd7)
                        end

                    65000:
                        begin
                            // Generate STB (looped back to int31, so it triggers interrupt report)
                            packet = {8'hD5, 8'd7, 16'h3223, 8'd62, 32'h00000080};
                            send_packet = 1;
                        end
                    74000:
                        begin
                            `assert_rx(128'hd503322381d7)
                        end

                    79000:
                        begin
                            // interrupt report
                            `assert_rx(128'hd507ffff500000008049)
                        end

                    94000:
                        begin
                            // interrupt re-report every 10k cycles
                            `assert_rx(128'hd507ffff500000008049)
                            `assert_signal("Pending ints", dut.s3g_executor.ints_pending, 32'h80000000)
                            `assert_signal("Mask ints", dut.s3g_executor.ints_mask, 32'hffffffff)
                        end
                    94500:
                        begin
                            // Mask ints
                            packet = {8'hD5, 8'd7, 16'h5645, 8'd64, 32'hffffff7f};
                            send_packet = 1;
                        end
                    105000:
                        begin
                            // assert mask is right
                            `assert_rx(128'hd5035645811c)
                            `assert_signal("Pending ints", dut.s3g_executor.ints_pending, 32'h80000000)
                            `assert_signal("Mask ints", dut.s3g_executor.ints_mask, 32'h7fffffff)
                        end
                    125000:
                        begin
                            // assert no new interrupts
                            `assert_rx(64'h0)
                        end
                    126000:
                        begin
                            // unMask ints
                            packet = {8'hD5, 8'd7, 16'h3233, 8'd64, 32'hffffffff};
                            send_packet = 1;
                        end
                    135000:
                        begin
                            // assert mask is right
                            `assert_rx(128'hd5033233813b)
                            `assert_signal("Pending ints", dut.s3g_executor.ints_pending, 32'h80000000)
                            `assert_signal("Mask ints", dut.s3g_executor.ints_mask, 32'hffffffff)
                        end
                    140000:
                        begin
                            // interrupt report
                            `assert_rx(128'hd507ffff500000008049)
                        end
                    155000:
                        begin
                            // interrupt report
                            `assert_rx(128'hd507ffff500000008049)
                        end
                    156000:
                        begin
                            // Clear ints
                            packet = {8'hD5, 8'd7, 16'h7654, 8'd63, 32'h00000080};
                            send_packet = 1;
                        end
                    165000:
                        begin
                            // assert no pending interrupts
                            `assert_rx(64'hd503765481a0)
                            `assert_signal("Pending ints", dut.s3g_executor.ints_pending, 32'h00000000)
                        end
                    190000:
                        begin
                            // assert no new interrupts
                            `assert_rx(64'h0)
                        end
                    200000:
                        begin
                            // Load simple prog:
                            //    0x88776655 -> reg0
                            //    DONE
                            packet = {
                                        buf_cmds.S3G_WRITE_BUFFER_HDR(0, 2),
                                        buf_cmds.OUTPUT(0, 32'h88776655),
                                        buf_cmds.DONE(0)
                            };
                            send_packet = 1;
                        end
                    217000:
                        begin
                            `assert_rx(128'hd508765481000000000033)
                        end
                    220000:
                        begin
                            // Set start addr for buf_exec
                            packet = buf_cmds.S3G_OUTPUT(62, 0);
                            send_packet = 1;
                        end
                    229500:
                        begin
                            `assert_rx(128'hd503765481a0)
                        end
                    230000:
                        begin
                            // Send be_start strobe
                            packet = buf_cmds.S3G_STB(32'h20000000);
                            send_packet = 1;
                        end
                    239000:
                        begin
                            `assert_rx(128'hd503765481a0)
                        end
                    244000:
                        begin
                            // Complete interrupt, check leds are changed
                            `assert_rx(128'hd507ffff500000004083)
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h55)
                        end
                    245000:
                        begin
                            // Clear be_complete interrupt
                            packet = buf_cmds.S3G_CLEAR(32'h40000000);
                            send_packet = 1;
                        end
                    254000:
                        begin
                            `assert_rx(128'hd503765481a0)
                        end
                    290000:
                        begin
                            `assert_rx(64'h0)
                        end

                    300000:
                        begin
                            // Load simple prog:
                            //    0x01 -> reg0 (leds)
                            //    10 -> reg1 (asg_steps_val), 10 steps
                            //    1000 -> reg2 (asg_dt_val), 1ms step
                            //    0x000F -> reg3 (asg_control), set_steps_limit, set_dt_limit, reset_steps, reset_dt
                            //    STB 1 - asg_load
                            //    WAIT_ALL 1 (wait for asg_done)
                            //    CLEAR 1 (avoid triggering of too much interrupts)
                            //    0 -> reg2 (asg_dt_val), go to idle
                            //    STB 1 - asg_load
                            //    0x02 -> reg0 (leds)
                            //    DONE
                            packet = {
                                        buf_cmds.S3G_WRITE_BUFFER_HDR(0, 11),

                                        buf_cmds.OUTPUT(0, 1),
                                        buf_cmds.OUTPUT(1, 10),
                                        buf_cmds.OUTPUT(2, 1000),
                                        buf_cmds.OUTPUT(3, 32'h0000000F),
                                        buf_cmds.STB(32'h00000001),
                                        buf_cmds.WAIT_ALL(32'h00000001),
                                        buf_cmds.CLEAR(32'h00000001),
                                        buf_cmds.OUTPUT(2, 0),
                                        buf_cmds.STB(32'h00000001),
                                        buf_cmds.OUTPUT(0, 2),
                                        buf_cmds.DONE(0)
                            };
                            send_packet = 1;
                        end
                    344000:
                        begin
                            `assert_rx(128'hd5087654810000000100f7)
                            // Send be_start stb
                            packet = buf_cmds.S3G_STB(32'h20000000);
                            send_packet = 1;
                        end
                    353000:
                        begin
                            // Execution started, leds -> 01
                            `assert_rx(128'hd503765481a0)
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h01)
                        end
                    365000:
                        begin
                            // Execution done, leds -> 02
                            `assert_rx(128'hd507ffff50010000004a)
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h02)
                        end
                    380000:
                        begin
                            // Interrupt retriggered
                            `assert_rx(128'hd507ffff500000004083)
                        end
                    395000:
                        begin
                            // Interrupt retriggered
                            `assert_rx(128'hd507ffff500000004083)
                            // Retrigger execution
                            packet = buf_cmds.S3G_STB(32'h20000000);
                            send_packet = 1;
                        end
                    404000:
                        begin
                            // Second execution started, leds -> 01
                            `assert_rx(128'hd503765481a0)
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h01)
                        end
                    410000:
                        begin
                            // Retrigger interrupt
                            `assert_rx(128'hd507ffff500000004083)
                        end
                    413000:
                        begin
                            // Execution done, leds -> 02
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h02)
                        end
                    425000:
                        begin
                            // Interrupt retriggered
                            `assert_rx(128'hd507ffff500000004083)
                            // Clear interrupts
                            packet = buf_cmds.S3G_CLEAR(32'h40000000);
                            send_packet = 1;
                        end
                    434000:
                        begin
                            // Retrigger interrupt
                            `assert_rx(128'hd503765481a0)
                        end

                    450000:
                        begin
                            // Load simple prog:
                            //    0x01 -> reg0 (leds)
                            //    10 -> reg1 (asg_steps_val), 10 steps
                            //    1000 -> reg2 (asg_dt_val), 1ms step
                            //    0x000F -> reg3 (asg_control), set_steps_limit, set_dt_limit, reset_steps, reset_dt
                            //    STB 1 - asg_load
                            //    WAIT_ALL 1 (wait for asg_done)
                            //    CLEAR 1 (avoid triggering of too much interrupts)
                            //    0 -> reg2 (asg_dt_val), go to idle
                            //    STB 1 - asg_load
                            //    0x02 -> reg0 (leds)
                            //    DONE
                            packet = {
                                        buf_cmds.S3G_WRITE_BUFFER_HDR(0, 36),

                                        // LEDS 0x1
                                        buf_cmds.OUTPUT(buf_cmds.LEDS, 1),
                                        // Step 1 - constant acceleration speed up to V = 5050
                                        buf_cmds.OUTPUT(buf_cmds.ASG_STEPS_VAL, 70),
                                        buf_cmds.OUTPUT(buf_cmds.ASG_DT_VAL, 1000),
                                        buf_cmds.OUTPUT(buf_cmds.ASG_CONTROL,
                                                            buf_cmds.ASG_CONTROL_SET_STEPS_LIMIT |
                                                            buf_cmds.ASG_CONTROL_SET_DT_LIMIT |
                                                            buf_cmds.ASG_CONTROL_RESET_STEPS |
                                                            buf_cmds.ASG_CONTROL_RESET_DT |
                                                            buf_cmds.ASG_CONTROL_APG_X_SET_A |
                                                            buf_cmds.ASG_CONTROL_APG_X_SET_TARGET_V
                                                       ),
                                        buf_cmds.OUTPUT(buf_cmds.MSG_ALL_PRE_N, 10),
                                        buf_cmds.OUTPUT(buf_cmds.MSG_ALL_PULSE_N, 20),
                                        buf_cmds.OUTPUT(buf_cmds.MSG_ALL_POST_N, 30),
                                        buf_cmds.OUTPUT(buf_cmds.MSG_CONTROL,
                                                            buf_cmds.MSG_CONTROL_ENABLE_X
                                                       ),
                                        buf_cmds.OUTPUT(buf_cmds.APG_X_A_VAL, 100),
                                        buf_cmds.OUTPUT(buf_cmds.APG_X_ABORT_A_VAL, 200),
                                        buf_cmds.OUTPUT(buf_cmds.APG_X_TARGET_V_VAL, 5050),
                                        buf_cmds.OUTPUT(buf_cmds.BE_START_ADDR, 0),
                                        // Load params
                                        buf_cmds.STB(buf_cmds.STB_ASG_LOAD),
                                        // Step 2 - constant acceleration speed down and reverse to V = -5050
                                        buf_cmds.OUTPUT(buf_cmds.ASG_CONTROL,
                                                            buf_cmds.ASG_CONTROL_SET_STEPS_LIMIT |
                                                            buf_cmds.ASG_CONTROL_RESET_STEPS |
                                                            buf_cmds.ASG_CONTROL_APG_X_SET_A |
                                                            buf_cmds.ASG_CONTROL_APG_X_SET_TARGET_V
                                                       ),
                                        buf_cmds.OUTPUT(buf_cmds.ASG_STEPS_VAL, 140),
                                        buf_cmds.OUTPUT(buf_cmds.APG_X_A_VAL, -100),
                                        buf_cmds.OUTPUT(buf_cmds.APG_X_TARGET_V_VAL, -5050),
                                        // Wait for prev step completion
                                        buf_cmds.WAIT_ALL(buf_cmds.INT_ASG_DONE),
                                        // Clear int and load
                                        buf_cmds.CLEAR(buf_cmds.INT_ASG_DONE),
                                        buf_cmds.STB(buf_cmds.STB_ASG_LOAD),
                                        buf_cmds.OUTPUT(buf_cmds.LEDS, 3),
                                        // Step 3 - constant acceleration speed down to V = 0
                                        buf_cmds.OUTPUT(buf_cmds.ASG_CONTROL,
                                                            buf_cmds.ASG_CONTROL_SET_STEPS_LIMIT |
                                                            buf_cmds.ASG_CONTROL_RESET_STEPS |
                                                            buf_cmds.ASG_CONTROL_APG_X_SET_A |
                                                            buf_cmds.ASG_CONTROL_APG_X_SET_TARGET_V
                                                       ),
                                        buf_cmds.OUTPUT(buf_cmds.ASG_STEPS_VAL, 70),
                                        buf_cmds.OUTPUT(buf_cmds.APG_X_A_VAL, 100),
                                        buf_cmds.OUTPUT(buf_cmds.APG_X_TARGET_V_VAL, 0),
                                        // Wait for prev step completion
                                        buf_cmds.WAIT_ALL(buf_cmds.INT_ASG_DONE),
                                        // Clear int and load
                                        buf_cmds.CLEAR(buf_cmds.INT_ASG_DONE),
                                        buf_cmds.STB(buf_cmds.STB_ASG_LOAD),
                                        buf_cmds.OUTPUT(buf_cmds.LEDS, 7),
                                        // Params for shutdown
                                        buf_cmds.OUTPUT(buf_cmds.ASG_CONTROL,
                                                            buf_cmds.ASG_CONTROL_SET_DT_LIMIT
                                                       ),
                                        // Wait for step 3 completion
                                        buf_cmds.WAIT_ALL(buf_cmds.INT_ASG_DONE),
                                        buf_cmds.CLEAR(buf_cmds.INT_ASG_DONE),
                                        buf_cmds.OUTPUT(buf_cmds.ASG_DT_VAL, 0),
                                        buf_cmds.STB(buf_cmds.STB_ASG_LOAD),
                                        buf_cmds.OUTPUT(buf_cmds.LEDS, 15),
                                        buf_cmds.DONE(0)
                            };
                            send_packet = 1;
                        end
                    580000:
                        begin
                            `assert_rx(128'hd5087654810000000a00d4)
                            // Send be_start stb
                            packet = buf_cmds.S3G_STB(buf_cmds.STB_BE_START);
                            send_packet = 1;
                        end
                    590000:
                        begin
                            // Execution started, leds -> 01
                            `assert_rx(128'hd503765481a0)
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h01)
                        end
                    620000:
                        begin
                            `assert_signal("A", dut.apg_x.a, 100)
                        end
                    645000:
                        begin
                            `assert_signal("V", dut.apg_x.v, 5050)
                            `assert_signal("A", dut.apg_x.a, 0)
                        end
                    690000:
                        begin
                            // Step 2 started, leds -> 03
                            `assert_rx(128'hd507ffff50010000004a)
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h03)
                            `assert_signal("A", dut.apg_x.a, -100)
                        end
                    770000:
                        begin
                            `assert_signal("V", dut.apg_x.v, -5050)
                            `assert_signal("A", dut.apg_x.a, 0)
                        end
                    820000:
                        begin
                            // Step 2 started, leds -> 03
                            `assert_rx(128'hd507ffff50010000004a)
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h07)
                            `assert_signal("A", dut.apg_x.a, 100)
                        end
                    860000:
                        begin
                            `assert_signal("V", dut.apg_x.v, 0)
                            `assert_signal("A", dut.apg_x.a, 0)
                        end
                    875000:
                        begin
                            // Execution done, leds -> 02
                            `assert_signal("LEDS", dut.out_reg0[7:0], 8'h0f)
                            // Interrupt retriggered
                            `assert_rx(128'hd507ffff50010000004a)
                            // Clear interrupts
                            packet = buf_cmds.S3G_CLEAR(32'h40000000);
                            send_packet = 1;
                        end
                    890000:
                        begin
                            // Execution started, leds -> 01
                            `assert_rx(128'hd503765481a0)
                        end

                    900000:
                        begin
                            packet = {
                                buf_cmds.S3G_WRITE_BUFFER_HDR(0, 14),

                                // LEDS 0x1
                                buf_cmds.OUTPUT(buf_cmds.LEDS, 1),
                                // Step 1 - constant acceleration speed up to V = 5050
                                buf_cmds.OUTPUT(buf_cmds.ASG_STEPS_VAL, 70),
                                buf_cmds.OUTPUT(buf_cmds.ASG_DT_VAL, 1000),
                                buf_cmds.OUTPUT(buf_cmds.ASG_CONTROL,
                                                    buf_cmds.ASG_CONTROL_SET_STEPS_LIMIT |
                                                    buf_cmds.ASG_CONTROL_SET_DT_LIMIT |
                                                    buf_cmds.ASG_CONTROL_RESET_STEPS |
                                                    buf_cmds.ASG_CONTROL_RESET_DT |
                                                    buf_cmds.ASG_CONTROL_APG_X_SET_A |
                                                    buf_cmds.ASG_CONTROL_APG_X_SET_TARGET_V
                                               ),
                                buf_cmds.OUTPUT(buf_cmds.MSG_ALL_PRE_N, 10),
                                buf_cmds.OUTPUT(buf_cmds.MSG_ALL_PULSE_N, 20),
                                buf_cmds.OUTPUT(buf_cmds.MSG_ALL_POST_N, 30),
                                buf_cmds.OUTPUT(buf_cmds.MSG_CONTROL,
                                                    buf_cmds.MSG_CONTROL_ENABLE_X
                                               ),
                                buf_cmds.OUTPUT(buf_cmds.APG_X_A_VAL, -100),
                                buf_cmds.OUTPUT(buf_cmds.APG_X_ABORT_A_VAL, 200),
                                buf_cmds.OUTPUT(buf_cmds.APG_X_TARGET_V_VAL, -5050),
                                buf_cmds.OUTPUT(buf_cmds.BE_START_ADDR, 0),
                                // Load params
                                buf_cmds.STB(buf_cmds.STB_ASG_LOAD),
                                // Step 2 - constant acceleration speed down and reverse to V = -5050
                                buf_cmds.DONE(0)
                            };
                            send_packet = 1;
                        end
                    955000:
                        begin
                            `assert_rx(128'hd5087654810000002300a7)
                            // Send be_start stb
                            packet = buf_cmds.S3G_STB(buf_cmds.STB_BE_START);
                            send_packet = 1;
                        end
                    970000:
                        begin
                            // Execution started, leds -> 01
                            `assert_rx(128'hd503765481a0d507ffff500000004083)
                            packet = buf_cmds.S3G_CLEAR(32'h40000000);
                            send_packet = 1;
                        end
                    979000:
                        begin
                            `assert_rx(128'hd503765481a0)
                            // Send be_start stb
                        end
                    1036000:
                        begin
                            `assert_rx(128'hd507ffff50010000004a)
                            // Send be_start stb
                            packet = buf_cmds.S3G_CLEAR(1);
                            send_packet = 1;
                        end
                    1050000:
                        begin
                            `assert_rx(128'hd503765481a0d507ffff5002000000c2)
                            // Send be_start stb
                            packet = buf_cmds.S3G_OUTPUT(buf_cmds.ASG_CONTROL,
                                buf_cmds.ASG_CONTROL_SET_DT_LIMIT | buf_cmds.ASG_CONTROL_RESET_DT | buf_cmds.ASG_CONTROL_RESET_STEPS);
                            send_packet = 1;
                        end
                    1066000:
                        begin
                            `assert_rx(128'hdd503765481a0d507ffff5002000000c2)
                            // Send be_start stb
                            packet = buf_cmds.S3G_OUTPUT(buf_cmds.ASG_DT_VAL, 0);
                            send_packet = 1;
                        end
                    1082000:
                        begin
                            `assert_rx(128'hd503765481a0d507ffff5002000000c2)
                            // Send be_start stb
                            packet = buf_cmds.S3G_STB(buf_cmds.STB_ASG_LOAD);
                            send_packet = 1;
                        end
                    1097000:
                        begin
                            `assert_rx(128'hd503765481a0d507ffff5002000000c2)
                            packet = buf_cmds.S3G_CLEAR(2);
                            send_packet = 1;
                        end
                    1111000:
                        begin
                            `assert_rx(128'hd503765481a0)
                            // Send be_start stb
                        end
                    1200000:
                        begin
                            dut.s3g_executor.out_reg32 = 32'd1000;
                            dut.s3g_executor.out_reg33 = 32'h00000010;
                        end
                    1201000:
                        begin
                            stop_x2 = 1;
                        end
                    1400000:
                        begin
                            `assert_rx(128'h0)
                            if (assertions_failed)
                                begin
                                    $display("ERROR: Some assertions failed");
                                end
                            else
                                begin
                                    $display("All passed");
                                end
                            $finish();
                        end
                endcase

                #4;
                clk = 0;
                #10;
                cycle = cycle + 1;
                // $display(cycle);
            end
    end

integer ppos, first;
always @(negedge clk)
    begin
        if (send_packet)
        begin
            $display("send %0h at %0d", packet, cycle);
            send_packet <= 0;
            first = 1;
            for (ppos = 2047; ppos>0; ppos = ppos - 8)
            begin
                if (first)
                    begin
                        if (packet[ppos-:8] != 0)
                            begin
                                first = 0;
                                tx_data = packet[ppos-:8];
                                tx_wr = 1;
                                $display("time: %0d send %h", cycle, tx_data);
                                #12000;
                            end
                    end
                else
                    begin
                        tx_data = packet[ppos-:8];
                        tx_wr = 1;
                        $display("time: %0d send %h", cycle, tx_data);
                        #12000;
                    end
            end
            tx_data = dut.s3g_rx.crc;
            tx_wr = 1;
            $display("time: %0d send crc %h", cycle, tx_data);
            #12000;

        end
    end

endmodule
