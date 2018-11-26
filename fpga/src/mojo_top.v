module mojo_top #(
    parameter CLK_RATE = 50000000,
    parameter SERIAL_BAUD_RATE = 500000
)(
    // 50MHz clock input
    input clk,
    // Input from reset button (active low)
    input rst_n,
    // cclk input from AVR, high when AVR is ready
    input cclk,
    // Outputs to the 8 onboard LEDs
    output[7:0]led,
    // AVR SPI connections
    output spi_miso,
    input spi_ss,
    input spi_mosi,
    input spi_sck,
    // AVR ADC channel select
    output [3:0] spi_channel,
    // Serial connections
    input avr_tx, // AVR Tx => FPGA Rx
    output avr_rx, // AVR Rx => FPGA Tx
    input avr_rx_busy, // AVR Rx buffer full
    input ext_tx, // Ext Tx => FPGA Rx
    output ext_rx, // Ext Rx => FPGA Tx
    input ext_rx_busy // Ext Rx buffer full
    );

wire rst = ~rst_n; // make reset active high

// these signals should be high-z when not used
assign spi_miso = 1'bz;
assign avr_rx = 1'bz;
assign spi_channel = 4'bzzzz;

wire ready;
wire n_rdy = !ready;

reg [27:0] cnt;

cclk_detector #(.CLK_RATE(CLK_RATE)) cclk_detector (
    .clk(clk),
    .rst(rst),
    .cclk(cclk),
    .ready(ready)
);

wire [7:0] tx_data;
wire tx_wr;
wire tx1_done;
wire tx2_done;

wire [7:0] rx_data;
wire new_rx_data;
wire enable_16;

dds_uart_clock uclock1(
                   .clk(clk),
                   .baudrate(16'd5000),
                   .enable_16(enable_16)
               );

uart_transceiver uart1(
                     .sys_clk(clk),
                     .sys_rst(n_rdy),
                     .uart_rx(avr_tx),
                     .uart_tx(avr_rx),
                     .enable_16(enable_16),
                     .rx_data(rx_data),
                     .rx_done(new_rx_data),
                     .tx_data(tx_data),
                     .tx_wr(tx_wr),
                     .tx_done(tx1_done)
                 );

wire [7:0] rx2_data;
wire new_rx2_data;
wire enable_16_2;

dds_uart_clock uclock2(
                   .clk(clk),
                   .baudrate(16'd1152),
                   .enable_16(enable_16_2)
               );

uart_transceiver uart2(
                     .sys_clk(clk),
                     .sys_rst(n_rdy),
                     .uart_rx(ext_tx),
                     .uart_tx(ext_rx),
                     .enable_16(enable_16_2),
                     .rx_data(rx2_data),
                     .rx_done(new_rx2_data),
                     .tx_data(tx_data),
                     .tx_wr(tx_wr),
                     .tx_done(tx2_done)
                 );


wire rx_packet_done;
wire rx_packet_error;
wire rx_buffer_valid;

wire [7:0] rx_buffer_addr;
wire [7:0] rx_buffer_data;

wire [7:0] rx_payload_len;
wire [7:0] rx_buf0;
wire [7:0] rx_buf1;
wire [7:0] rx_buf2;
wire [7:0] rx_buf3;
wire [7:0] rx_buf4;
wire [7:0] rx_buf5;
wire [7:0] rx_buf6;
wire [7:0] rx_buf7;
wire [7:0] rx_buf8;
wire [7:0] rx_buf9;
wire [7:0] rx_buf10;
wire [7:0] rx_buf11;
wire [7:0] rx_buf12;
wire [7:0] rx_buf13;
wire [7:0] rx_buf14;
wire [7:0] rx_buf15;

wire tx_packet_wr;
wire tx_busy;

wire [7:0] tx_payload_len;
wire [7:0] tx_buf0;
wire [7:0] tx_buf1;
wire [7:0] tx_buf2;
wire [7:0] tx_buf3;
wire [7:0] tx_buf4;
wire [7:0] tx_buf5;
wire [7:0] tx_buf6;
wire [7:0] tx_buf7;
wire [7:0] tx_buf8;
wire [7:0] tx_buf9;
wire [7:0] tx_buf10;
wire [7:0] tx_buf11;
wire [7:0] tx_buf12;
wire [7:0] tx_buf13;
wire [7:0] tx_buf14;
wire [7:0] tx_buf15;

wire [31:0] out_reg0;

s3g_rx s3g_rx(
    .clk(clk),
    .rst(n_rdy),
    .rx1_data(rx_data),
    .rx1_done(new_rx_data),
    .rx2_data(rx2_data),
    .rx2_done(new_rx2_data),
    .packet_done(rx_packet_done),
    .packet_error(rx_packet_error),
    .payload_len(rx_payload_len),
    .buffer_valid(rx_buffer_valid),
    .buf0(rx_buf0),
    .buf1(rx_buf1),
    .buf2(rx_buf2),
    .buf3(rx_buf3),
    .buf4(rx_buf4),
    .buf5(rx_buf5),
    .buf6(rx_buf6),
    .buf7(rx_buf7),
    .buf8(rx_buf8),
    .buf9(rx_buf9),
    .buf10(rx_buf10),
    .buf11(rx_buf11),
    .buf12(rx_buf12),
    .buf13(rx_buf13),
    .buf14(rx_buf14),
    .buf15(rx_buf15),
    .buffer_addr(rx_buffer_addr),
    .buffer_data(rx_buffer_data)
);

s3g_executor s3g_executor(
    .clk(clk),
    .rst(n_rdy),
    .rx_packet_done(rx_packet_done),
    .rx_packet_error(rx_packet_error),
    .rx_buffer_valid(rx_buffer_valid),
    .rx_payload_len(rx_payload_len),
    .rx_buf0(rx_buf0),
    .rx_buf1(rx_buf1),
    .rx_buf2(rx_buf2),
    .rx_buf3(rx_buf3),
    .rx_buf4(rx_buf4),
    .rx_buf5(rx_buf5),
    .rx_buf6(rx_buf6),
    .rx_buf7(rx_buf7),
    .rx_buf8(rx_buf8),
    .rx_buf9(rx_buf9),
    .rx_buf10(rx_buf10),
    .rx_buf11(rx_buf11),
    .rx_buf12(rx_buf12),
    .rx_buf13(rx_buf13),
    .rx_buf14(rx_buf14),
    .rx_buf15(rx_buf15),
    .next_rx_buffer_addr(rx_buffer_addr),
    .rx_buffer_data(rx_buffer_data),
    .tx_busy(tx_busy),
    .tx_packet_wr(tx_packet_wr),
    .tx_payload_len(tx_payload_len),
    .tx_buf0(tx_buf0),
    .tx_buf1(tx_buf1),
    .tx_buf2(tx_buf2),
    .tx_buf3(tx_buf3),
    .tx_buf4(tx_buf4),
    .tx_buf5(tx_buf5),
    .tx_buf6(tx_buf6),
    .tx_buf7(tx_buf7),
    .tx_buf8(tx_buf8),
    .tx_buf9(tx_buf9),
    .tx_buf10(tx_buf10),
    .tx_buf11(tx_buf11),
    .tx_buf12(tx_buf12),
    .tx_buf13(tx_buf13),
    .tx_buf14(tx_buf14),
    .tx_buf15(tx_buf15),

    .out_reg0(out_reg0)
);

s3g_tx s3g_tx1(
           .clk(clk),
           .rst(n_rdy),
           .tx_data(tx_data),
           .tx_wr(tx_wr),
           .tx1_done(tx1_done),
           .tx2_done(tx2_done),
           .busy(tx_busy),
           .payload_len(tx_payload_len),
           .packet_wr(tx_packet_wr),
           .buf0(tx_buf0),
           .buf1(tx_buf1),
           .buf2(tx_buf2),
           .buf3(tx_buf3),
           .buf4(tx_buf4),
           .buf5(tx_buf5),
           .buf6(tx_buf6),
           .buf7(tx_buf7),
           .buf8(tx_buf8),
           .buf9(tx_buf9),
           .buf10(tx_buf10),
           .buf11(tx_buf11),
           .buf12(tx_buf12),
           .buf13(tx_buf13),
           .buf14(tx_buf14),
           .buf15(tx_buf15)
       );

assign led = out_reg0;

always @(posedge clk)
   if (rx_packet_done)
       begin
           cnt[27:20] <= rx_buf0;
           cnt[19:0] <= 20'b0;
       end
   else if (new_rx_data)
       begin
           // cnt[27:20] <= rx_data;
           // cnt[19:0] <= 20'b0;
           cnt <= cnt;
       end
   else
       cnt <= cnt;

endmodule
