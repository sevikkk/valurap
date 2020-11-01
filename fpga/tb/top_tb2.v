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
`include "../src/motor_mux.v"
`include "../src/debounce.v"
`include "../src/dp_ram.v"
`include "../src/profile_gen.v"
`include "../src/speed_integrator.v"
`include "../src/fifo.v"
`include "../tb/buf_cmds.v"

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
    reg stop_y1 = 0;
    reg stop_y2 = 0;

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
            rx_buffer <= {rx_buffer, avr_rx_data};
            $display("time: %0d received %h", cycle, avr_rx_data);
        end

    mojo_top#(
        .EXT_BAUD_RATE(BR),
        .FIFO_ADDRESS_WIDTH(10)
    ) dut(
        .clk(clk),
        .rst_n(rst_n),
        .cclk(cclk),
        .ext_tx(avr_tx),
        .ext_rx(avr_rx),
        .endstop_x1(stop_x1),
        .endstop_x2(stop_x2),
        .endstop_y1(stop_y1),
        .endstop_y2(stop_y2)
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
                        2000:
                            begin
                                // Load simple prog:
                                //    0x88776655 -> reg0
                                //    DONE
                                packet = {
                                    buf_cmds.S3G_WRITE_FIFO_HDR(38),
                                    /* 0 */
                                    buf_cmds.OUTPUT(0, 32'd1000),    // dt_val = 1000
                                    buf_cmds.OUTPUT(1, 32'd100),     // steps_val = 100
                                    buf_cmds.OUTPUT(2, 32'd16),       // step_bit = 16
                                    buf_cmds.OUTPUT(3, 32'd16),       // pre_n
                                    buf_cmds.OUTPUT(4, 32'd32),       // pulse_n
                                    buf_cmds.OUTPUT(5, 32'd48),       // post_n
                                    buf_cmds.OUTPUT(7, 32'h888888),       // post_n
                                    buf_cmds.PARAM_ADDR(0),
                                    buf_cmds.PARAM_WRITE_LO(0, 1),   // CH0.STATUS=1
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    /* 10 */
                                    buf_cmds.PARAM_WRITE_LO(3, 0),   // CH0.V_OUT=0
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO(1, 5),   // CH0.A=5
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO(1, 0),   // CH0.J=0
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO(1, 0),   // CH0.JJ=0
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO(1, 0),   // CH0.TARGET_V=0
                                    buf_cmds.PARAM_WRITE_HI(0),

                                    buf_cmds.PARAM_WRITE_LO(1, 10),   // CH0.ABORT_A=10
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO_NC(0),   // CH1.STATUS=0
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO_NC(0),   // CH2
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO_NC(0),   // CH3
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO_NC(0),   // CH4
                                    buf_cmds.PARAM_WRITE_HI(0),

                                    buf_cmds.PARAM_WRITE_LO_NC(0),   // CH5
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO_NC(0),   // CH6
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.PARAM_WRITE_LO_NC(0),   // CH7
                                    buf_cmds.PARAM_WRITE_HI(0),
                                    buf_cmds.STB(4),
                                    buf_cmds.DONE(0)
                                    };
                                send_packet = 1;
                            end

                        126000:
                            begin
                                `assert_rx(128'hd507765481da03000057)
                                packet = buf_cmds.S3G_STB(1);
                                send_packet = 1;
                            end

                        135000:
                        begin
                            `assert_rx(128'hd503765481a0)
                        end

                        500000:
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
                    cycle = cycle+1;
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
                    for (ppos = 2047; ppos > 0; ppos = ppos-8)
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
