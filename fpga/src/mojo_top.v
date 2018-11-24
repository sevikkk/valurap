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
    input avr_rx_busy // AVR Rx buffer full
    );

wire rst = ~rst_n; // make reset active high

// these signals should be high-z when not used
assign spi_miso = 1'bz;
assign avr_rx = 1'bz;
assign spi_channel = 4'bzzzz;

wire ready;
wire n_rdy = !ready;

reg [27:0] cnt;
assign led[7:0] = cnt[27:20];

cclk_detector #(.CLK_RATE(CLK_RATE)) cclk_detector (
    .clk(clk),
    .rst(rst),
    .cclk(cclk),
    .ready(ready)
);

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
                     .tx_data(8'b0),
                     .tx_wr(1'b0),
                     .tx_done()
                 );

always @(posedge clk)
   if (!new_rx_data)
       begin
	   cnt <= cnt + 1;
       end
   else
       begin
	   cnt[27:20] <= rx_data;
	   cnt[19:0] <= 20'b0;
       end;

endmodule
