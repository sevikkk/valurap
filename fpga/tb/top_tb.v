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
        .EXT_BAUD_RATE(BR)
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
                        end

                        100000:
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
