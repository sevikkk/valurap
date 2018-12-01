`include "../src/mojo_top.v"
`include "../src/buf_executor.v"
`include "../src/s3g_executor.v"
`include "../src/s3g_rx.v"
`include "../src/s3g_tx.v"
`include "../src/cclk_detector.v"
`include "../src/dds_uart_clock.v"
`include "../src/uart_transceiver.v"

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
        .EXT_BAUD_RATE(BR)
    ) dut (
           .clk(clk),
           .rst_n(rst_n),
           .cclk(cclk),
           .avr_tx(avr_tx),
           .avr_rx(avr_rx)
       );

`define assert_rx(value) \
    begin if (rx_buffer != value) begin \
            $display("ASSERTION FAILED in %m at %0d: actual rx_buffer %h != expected %h", cycle, rx_buffer, value); \
        end \
        rx_buffer = 0; \
    end

initial
    begin
        $dumpfile("test.vcd");
        $dumpvars;

        rst_n = 0;
        cclk = 0;
        clk = 0;
        tx_wr = 0;
        #5;
        clk = 1;
        #5;
        clk = 0;
        #5;
        clk = 1;
        #5;
        clk = 0;
        #3;
        rst_n = 1;
        #2;
        clk = 1;
        #5;
        clk = 0;
        #5;
        clk = 1;
        #5;
        clk = 0;
        #5;
        clk = 1;
        #5;
        clk = 0;
        #3;
        cclk = 1;
        #2;
        clk = 1;
        #5;
        clk = 0;
        #5;
        clk = 1;
        #5;
        clk = 0;
        #5;
        cycle = 0;
        forever
            begin
                clk = 1;
                #3;

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
                            tx_data = 8'h01;
                            tx_wr = 1;
                        end
                    3700:
                        begin
                            tx_data = 8'h00;
                            tx_wr = 1;
                        end
                    4800:
                        begin
                            tx_data = 8'h00;
                            tx_wr = 1;
                        end
                    8500: `assert_rx(48'hD50381BACEF9)

                    15000:
                        begin
                            // Version request
                            packet = 24'hD50100;
                            send_packet = 1;
                        end
                    20500: `assert_rx(48'hD50381BACEF9)

                    25000:
                        begin
                            // Invalid command
                            packet = {8'hD5, 8'd5, 40'h1213141516};
                            send_packet = 1;
                        end
                    32000: `assert_rx(32'hD50185B3)
                endcase

                #2;
                clk = 0;
                #5;
                cycle = cycle + 1;
                // $display(cycle);
                if (cycle == 40000) $finish();
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
                                #6000;
                            end
                    end
                else
                    begin
                        tx_data = packet[ppos-:8];
                        tx_wr = 1;
                        $display("time: %0d send %h", cycle, tx_data);
                        #6000;
                    end
            end
            tx_data = dut.s3g_rx.crc;
            tx_wr = 1;
            $display("time: %0d send crc %h", $time, tx_data);
            #6000;

        end
    end

endmodule
