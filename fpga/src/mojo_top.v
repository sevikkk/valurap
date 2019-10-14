module mojo_top #(
    parameter CLK_RATE = 50000000
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
    input ext_rx_busy, // Ext Rx buffer full

    output mot_1_step,
    output mot_1_dir,
    output mot_1_enable,

    output mot_2_step,
    output mot_2_dir,
    output mot_2_enable,

    output mot_3_step,
    output mot_3_dir,
    output mot_3_enable,

    output mot_4_step,
    output mot_4_dir,
    output mot_4_enable,

    output mot_5_step,
    output mot_5_dir,
    output mot_5_enable,

    output mot_6_step,
    output mot_6_dir,
    output mot_6_enable,

    output mot_7_step,
    output mot_7_dir,
    output mot_7_enable,

    output mot_8_step,
    output mot_8_dir,
    output mot_8_enable,

    output mot_9_step,
    output mot_9_dir,
    output mot_9_enable,

    output mot_10_step,
    output mot_10_dir,
    output mot_10_enable,

    output mot_11_step,
    output mot_11_dir,
    output mot_11_enable,

    output mot_12_step,
    output mot_12_dir,
    output mot_12_enable,

    output ext1_1,
    output ext1_2,
    output ext1_3,
    output ext1_4,
    output ext1_5,
    output ext1_6,
    output ext1_7,
    output ext1_8,

    output ext2_1,
    output ext2_2,
    output ext2_3,
    output ext2_4,
    output ext2_5,
    output ext2_6,
    output ext2_7,
    output ext2_8,

    output ext3_1,
    output ext3_2,
    output ext3_3,
    output ext3_4,
    output ext3_5,
    output ext3_6,
    output ext3_7,
    output ext3_8
    );

wire rst = ~rst_n; // make reset active high

// these signals should be high-z when not used
assign spi_miso = 1'bz;
assign avr_rx = 1'bz;
assign spi_channel = 4'bzzzz;

wire ready;
wire n_rdy = !ready;

cclk_detector #(.CLK_RATE(CLK_RATE)) cclk_detector (
    .clk(clk),
    .rst(rst),
    .cclk(cclk),
    .ready(ready)
);

reg [23:0] blink_cnt = 0;

always @(posedge clk)
    blink_cnt <= blink_cnt + 1;

assign led[7:0] = blink_cnt[23:16];

assign avr_rx = 1'b1;
assign ext_rx = 1'b1;

assign mot_1_step = 1'b0;
assign mot_1_dir = 1'b0;
assign mot_1_enable = 1'b1;

assign mot_2_step = 1'b0;
assign mot_2_dir = 1'b0;
assign mot_2_enable = 1'b1;

assign mot_3_step = 1'b0;
assign mot_3_dir = 1'b0;
assign mot_3_enable = 1'b1;

assign mot_4_step = 1'b0;
assign mot_4_dir = 1'b0;
assign mot_4_enable = 1'b1;

assign mot_5_step = 1'b0;
assign mot_5_dir = 1'b0;
assign mot_5_enable = 1'b1;

assign mot_6_step = 1'b0;
assign mot_6_dir = 1'b0;
assign mot_6_enable = 1'b1;

assign mot_7_step = 1'b0;
assign mot_7_dir = 1'b0;
assign mot_7_enable = 1'b1;

assign mot_8_step = 1'b0;
assign mot_8_dir = 1'b0;
assign mot_8_enable = 1'b1;

assign mot_9_step = 1'b0;
assign mot_9_dir = 1'b0;
assign mot_9_enable = 1'b1;

assign mot_10_step = 1'b0;
assign mot_10_dir = 1'b0;
assign mot_10_enable = 1'b1;

assign mot_11_step = 1'b0;
assign mot_11_dir = 1'b0;
assign mot_11_enable = 1'b1;

assign mot_12_step = 1'b0;
assign mot_12_dir = 1'b0;
assign mot_12_enable = 1'b1;

assign ext1_1 = blink_cnt[20];
assign ext1_2 = blink_cnt[19];
assign ext1_3 = blink_cnt[18];
assign ext1_4 = blink_cnt[17];
assign ext1_5 = blink_cnt[16];
assign ext1_6 = blink_cnt[15];
assign ext1_7 = blink_cnt[14];
assign ext1_8 = blink_cnt[13];

assign ext2_1 = blink_cnt[17];
assign ext2_2 = blink_cnt[16];
assign ext2_3 = blink_cnt[15];
assign ext2_4 = blink_cnt[14];
assign ext2_5 = blink_cnt[13];
assign ext2_6 = blink_cnt[12];
assign ext2_7 = blink_cnt[11];
assign ext2_8 = blink_cnt[10];

assign ext3_1 = blink_cnt[14];
assign ext3_2 = blink_cnt[13];
assign ext3_3 = blink_cnt[12];
assign ext3_4 = blink_cnt[11];
assign ext3_5 = blink_cnt[10];
assign ext3_6 = blink_cnt[9];
assign ext3_7 = blink_cnt[8];
assign ext3_8 = blink_cnt[7];

endmodule
