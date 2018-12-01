module mojo_top #(
    parameter CLK_RATE = 50000000,
    parameter AVR_BAUD_RATE = 500000,
    parameter EXT_BAUD_RATE = 115200,
    parameter INTS_TIMER = 1000000
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
                   .baudrate(AVR_BAUD_RATE/100),
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
                   .baudrate(EXT_BAUD_RATE/100),
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
wire [31:0] out_reg3;
wire [31:0] out_reg4;
wire [31:0] out_reg5;
wire [31:0] out_reg6;
wire [31:0] out_reg7;
wire [31:0] out_reg8;
wire [31:0] out_reg9;
wire [31:0] out_reg10;
wire [31:0] out_reg11;
wire [31:0] out_reg12;
wire [31:0] out_reg13;
wire [31:0] out_reg14;
wire [31:0] out_reg15;
wire [31:0] out_reg16;
wire [31:0] out_reg17;
wire [31:0] out_reg18;
wire [31:0] out_reg19;

wire [31:0] stbs;

wire [15:0] ext_buffer_addr;
wire [39:0] ext_buffer_data;
wire ext_buffer_wr;

wire [7:0] ext_buffer_error;
wire [15:0] ext_buffer_pc;

wire [31:0] ext_out_reg_data;
wire [5:0] ext_out_reg_addr;
wire ext_out_reg_stb;
wire ext_out_reg_busy;

wire [31:0] ext_out_stbs;
wire [31:0] ext_pending_ints;
wire [31:0] ext_clear_ints;

wire be_start;
wire [31:0] be_start_addr;
wire be_abort;
wire be_complete;
wire be_busy;
wire be_waiting;

wire se_int_lb;
wire [31:0] se_reg_lb;

wire [31:0] asg_dt_val;
wire [31:0] asg_steps_val;
wire [31:0] asg_dt;
wire [31:0] asg_steps;
wire asg_load;
wire asg_set_steps_limit;
wire asg_set_dt_limit;
wire asg_reset_steps;
wire asg_reset_dt;
wire asg_abort;
wire asg_step;
wire asg_done;

assign asg_set_steps_limit = out_reg3[0];
assign asg_set_dt_limit = out_reg3[1];
assign asg_reset_steps = out_reg3[2];
assign asg_reset_dt = out_reg3[3];

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

s3g_executor #(.INTS_TIMER(INTS_TIMER)) s3g_executor(
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

    .in_reg0(asg_dt),
    .in_reg1(asg_steps),

    .in_reg62({be_busy, be_waiting, 6'b0, ext_buffer_error, ext_buffer_pc}),
    .in_reg63(se_reg_lb),

    .out_reg0(out_reg0), // leds
    .out_reg1(asg_steps_val),
    .out_reg2(asg_dt_val),
    .out_reg3(out_reg3), // asg_control
    .out_reg4(out_reg4),
    .out_reg5(out_reg5),
    .out_reg6(out_reg6),
    .out_reg7(out_reg7),
    .out_reg8(out_reg8),
    .out_reg9(out_reg9),
    .out_reg10(out_reg10),
    .out_reg11(out_reg11),
    .out_reg12(out_reg12),
    .out_reg13(out_reg13),
    .out_reg14(out_reg14),
    .out_reg15(out_reg15),
    .out_reg16(out_reg16),
    .out_reg17(out_reg17),
    .out_reg18(out_reg18),
    .out_reg19(out_reg19),

    .out_reg62(be_start_addr),
    .out_reg63(se_reg_lb),

    .out_stbs(stbs),

    .int0(asg_done),
    .int1(asg_abort),
    .int2(1'b0),
    .int3(1'b0),
    .int4(1'b0),
    .int5(1'b0),
    .int6(1'b0),
    .int7(1'b0),
    .int8(1'b0),
    .int9(1'b0),
    .int10(1'b0),
    .int11(1'b0),
    .int12(1'b0),
    .int13(1'b0),
    .int14(1'b0),
    .int15(1'b0),
    .int16(1'b0),
    .int17(1'b0),
    .int18(1'b0),
    .int19(1'b0),
    .int20(1'b0),
    .int21(1'b0),
    .int22(1'b0),
    .int23(1'b0),
    .int24(1'b0),
    .int25(1'b0),
    .int26(1'b0),
    .int27(1'b0),
    .int28(1'b0),
    .int29(1'b0),
    .int30(be_complete),
    .int31(se_int_lb),

    .ext_out_reg_busy(ext_out_reg_busy),
    .ext_out_reg_data(ext_out_reg_data),
    .ext_out_reg_addr(ext_out_reg_addr),
    .ext_out_reg_stb(ext_out_reg_stb),

    .ext_buffer_addr(ext_buffer_addr),
    .ext_buffer_data(ext_buffer_data),
    .ext_buffer_wr(ext_buffer_wr),
    .ext_buffer_pc(ext_buffer_pc),
    .ext_buffer_error(ext_buffer_error),
    .ext_pending_ints(ext_pending_ints),
    .ext_clear_ints(ext_clear_ints),
    .ext_out_stbs(ext_out_stbs)
);

assign asg_load = stbs[0];

assign be_start = stbs[29];
assign be_abort = stbs[30];
assign se_int_lb = stbs[31];

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

buf_executor buf_exec(
           .clk(clk),
           .rst(n_rdy),

           .ext_out_reg_addr(ext_out_reg_addr),
           .ext_out_reg_data(ext_out_reg_data),
           .ext_out_reg_stb(ext_out_reg_stb),
           .ext_out_reg_busy(ext_out_reg_busy),

           .ext_buffer_addr(ext_buffer_addr),
           .ext_buffer_data(ext_buffer_data),
           .ext_buffer_wr(ext_buffer_wr),
           .pc(ext_buffer_pc),
           .error(ext_buffer_error),

           .start(be_start),
           .start_addr(be_start_addr[15:0]),
           .abort(be_abort),
           .complete(be_complete),
           .busy(be_busy),
           .waiting(be_waiting),
           .ext_pending_ints(ext_pending_ints),
           .ext_clear_ints(ext_clear_ints),
           .ext_out_stbs(ext_out_stbs)
);

assign led = out_reg0;

acc_step_gen asg(
           .clk(clk),
           .reset(n_rdy),
           .dt_val(asg_dt_val),
           .steps_val(asg_steps_val),
           .load(asg_load),
           .set_steps_limit(asg_set_steps_limit),
           .set_dt_limit(asg_set_dt_limit),
           .reset_steps(asg_reset_steps),
           .reset_dt(asg_reset_dt),
           .steps(asg_steps),
           .dt(asg_dt),
           .abort(asg_abort),
           .step_stb(asg_step),
           .done(asg_done)
       );

endmodule
