module mojo_top #(
    parameter CLK_RATE = 50000000,
    parameter AVR_BAUD_RATE = 500000,
    parameter EXT_BAUD_RATE = 115200,
    parameter INTS_TIMER = 10000000
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

    input endstop_x1,
    input endstop_x2,
    input endstop_y
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

reg [23:0] blink_cnt = 0;

always @(posedge clk)
    blink_cnt <= blink_cnt + 1;

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
wire [31:0] out_reg20;
wire [31:0] out_reg21;
wire [31:0] out_reg22;
wire [31:0] out_reg23;
wire [31:0] out_reg24;
wire [31:0] out_reg25;
wire [31:0] out_reg26;
wire [31:0] out_reg27;
wire [31:0] out_reg28;
wire [31:0] out_reg29;
wire [31:0] out_reg30;
wire [31:0] out_reg31;
wire [31:0] out_reg32;
wire [31:0] out_reg33;
wire [31:0] out_reg34;
wire [31:0] out_reg35;
wire [31:0] out_reg36;
wire [31:0] out_reg37;
wire [31:0] out_reg38;
wire [31:0] out_reg39;

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
wire asg_step;
wire asg_done;

wire asg_abort;
wire asg_abort_chain_1;
wire asg_abort_chain_2;
wire asg_abort_chain_3;


assign asg_set_steps_limit = out_reg3[0];
assign asg_set_dt_limit = out_reg3[1];
assign asg_reset_steps = out_reg3[2];
assign asg_reset_dt = out_reg3[3];

wire [31:0] msg_all_pre_n;
wire [31:0] msg_all_pulse_n;
wire [31:0] msg_all_post_n;

assign msg_all_pre_n = out_reg4;
assign msg_all_pulse_n = out_reg5;
assign msg_all_post_n = out_reg6;

wire mot_x_step;
wire mot_x_dir;

wire mot_y_step;
wire mot_y_dir;

wire mot_z_step;
wire mot_z_dir;

assign mot_1_enable = ~out_reg7[0];

motor_mux mmux_1(
    .clk(clk),
    .step_x(mot_x_step),
    .dir_x(mot_x_dir),
    .step_y(mot_y_step),
    .dir_y(mot_y_dir),
    .step_z(mot_z_step),
    .dir_z(mot_z_dir),
    .mux_select(out_reg7[2:1]),
    .invert_dir(out_reg7[3]),
    .step(mot_1_step),
    .dir(mot_1_dir)
);

assign mot_2_enable = ~out_reg7[4];

motor_mux mmux_2(
    .clk(clk),
    .step_x(mot_x_step),
    .dir_x(mot_x_dir),
    .step_y(mot_y_step),
    .dir_y(mot_y_dir),
    .step_z(mot_z_step),
    .dir_z(mot_z_dir),
    .mux_select(out_reg7[6:5]),
    .invert_dir(out_reg7[7]),
    .step(mot_2_step),
    .dir(mot_2_dir)
);

assign mot_3_enable = ~out_reg7[8];

motor_mux mmux_3(
    .clk(clk),
    .step_x(mot_x_step),
    .dir_x(mot_x_dir),
    .step_y(mot_y_step),
    .dir_y(mot_y_dir),
    .step_z(mot_z_step),
    .dir_z(mot_z_dir),
    .mux_select(out_reg7[10:9]),
    .invert_dir(out_reg7[11]),
    .step(mot_3_step),
    .dir(mot_3_dir)
);

assign mot_4_enable = ~out_reg7[12];

motor_mux mmux_4(
    .clk(clk),
    .step_x(mot_x_step),
    .dir_x(mot_x_dir),
    .step_y(mot_y_step),
    .dir_y(mot_y_dir),
    .step_z(mot_z_step),
    .dir_z(mot_z_dir),
    .mux_select(out_reg7[14:13]),
    .invert_dir(out_reg7[15]),
    .step(mot_4_step),
    .dir(mot_4_dir)
);

assign mot_5_enable = ~out_reg7[16];

motor_mux mmux_5(
    .clk(clk),
    .step_x(mot_x_step),
    .dir_x(mot_x_dir),
    .step_y(mot_y_step),
    .dir_y(mot_y_dir),
    .step_z(mot_z_step),
    .dir_z(mot_z_dir),
    .mux_select(out_reg7[18:17]),
    .invert_dir(out_reg7[19]),
    .step(mot_5_step),
    .dir(mot_5_dir)
);

assign mot_6_enable = ~out_reg7[20];

motor_mux mmux_6(
    .clk(clk),
    .step_x(mot_x_step),
    .dir_x(mot_x_dir),
    .step_y(mot_y_step),
    .dir_y(mot_y_dir),
    .step_z(mot_z_step),
    .dir_z(mot_z_dir),
    .mux_select(out_reg7[22:21]),
    .invert_dir(out_reg7[23]),
    .step(mot_6_step),
    .dir(mot_6_dir)
);


wire apg_x_set_x;
wire apg_x_set_v;
wire apg_x_set_a;
wire apg_x_set_j;
wire apg_x_set_jj;
wire apg_x_set_target_v;

assign apg_x_set_x = out_reg3[8];
assign apg_x_set_v = out_reg3[9];
assign apg_x_set_a = out_reg3[10];
assign apg_x_set_j = out_reg3[11];
assign apg_x_set_jj = out_reg3[12];
assign apg_x_set_target_v = out_reg3[13];

wire signed [63:0] apg_x_x_val;
wire signed [31:0] apg_x_v_val;
wire signed [31:0] apg_x_a_val;
wire signed [31:0] apg_x_j_val;
wire signed [31:0] apg_x_jj_val;
wire signed [31:0] apg_x_target_v_val;
wire signed [31:0] apg_x_abort_a;
wire signed [63:0] apg_x_x;
wire signed [31:0] apg_x_v;

assign apg_x_x_val[31:0] = out_reg8;
assign apg_x_x_val[63:32] = out_reg9;
assign apg_x_v_val = out_reg10;
assign apg_x_a_val = out_reg11;
assign apg_x_j_val = out_reg12;
assign apg_x_jj_val = out_reg13;
assign apg_x_target_v_val = out_reg14;
assign apg_x_abort_a = out_reg15;

wire apg_x_step;
wire apg_x_dir;
wire apg_x_stopped;

wire apg_y_set_x;
wire apg_y_set_v;
wire apg_y_set_a;
wire apg_y_set_j;
wire apg_y_set_jj;
wire apg_y_set_target_v;

assign apg_y_set_x = out_reg3[16];
assign apg_y_set_v = out_reg3[17];
assign apg_y_set_a = out_reg3[18];
assign apg_y_set_j = out_reg3[19];
assign apg_y_set_jj = out_reg3[20];
assign apg_y_set_target_v = out_reg3[21];

wire signed [63:0] apg_y_x_val;
wire signed [31:0] apg_y_v_val;
wire signed [31:0] apg_y_a_val;
wire signed [31:0] apg_y_j_val;
wire signed [31:0] apg_y_jj_val;
wire signed [31:0] apg_y_target_v_val;
wire signed [31:0] apg_y_abort_a;
wire signed [63:0] apg_y_x;
wire signed [31:0] apg_y_v;

assign apg_y_x_val[31:0] = out_reg16;
assign apg_y_x_val[63:32] = out_reg17;
assign apg_y_v_val = out_reg18;
assign apg_y_a_val = out_reg19;
assign apg_y_j_val = out_reg20;
assign apg_y_jj_val = out_reg21;
assign apg_y_target_v_val = out_reg22;
assign apg_y_abort_a = out_reg23;

wire apg_y_step;
wire apg_y_dir;
wire apg_y_stopped;

wire apg_z_set_x;
wire apg_z_set_v;
wire apg_z_set_a;
wire apg_z_set_j;
wire apg_z_set_jj;
wire apg_z_set_target_v;

assign apg_z_set_x = out_reg3[24];
assign apg_z_set_v = out_reg3[25];
assign apg_z_set_a = out_reg3[26];
assign apg_z_set_j = out_reg3[27];
assign apg_z_set_jj = out_reg3[28];
assign apg_z_set_target_v = out_reg3[29];

wire signed [63:0] apg_z_x_val;
wire signed [31:0] apg_z_v_val;
wire signed [31:0] apg_z_a_val;
wire signed [31:0] apg_z_j_val;
wire signed [31:0] apg_z_jj_val;
wire signed [31:0] apg_z_target_v_val;
wire signed [31:0] apg_z_abort_a;
wire signed [63:0] apg_z_x;
wire signed [31:0] apg_z_v;

assign apg_z_x_val[31:0] = out_reg24;
assign apg_z_x_val[63:32] = out_reg25;
assign apg_z_v_val = out_reg26;
assign apg_z_a_val = out_reg27;
assign apg_z_j_val = out_reg28;
assign apg_z_jj_val = out_reg29;
assign apg_z_target_v_val = out_reg30;
assign apg_z_abort_a = out_reg31;

wire apg_z_step;
wire apg_z_dir;
wire apg_z_stopped;

wire endstops_unlock;

wire [31:0] es_1_pos;
wire [31:0] es_1_mb;
wire[7:0] es_1_cycles;
wire es_1_signal;
wire es_1_signal_changed;

wire [31:0] es_2_pos;
wire [31:0] es_2_mb;
wire[7:0] es_2_cycles;
wire es_2_signal;
wire es_2_signal_changed;

wire [31:0] es_3_pos;
wire [31:0] es_3_mb;
wire[7:0] es_3_cycles;
wire es_3_signal;
wire es_3_signal_changed;

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

    .in_reg2({16'h0, es_1_cycles, 7'h0, es_1_signal}),
    //.in_reg3(es_1_pos[31:0]),
    .in_reg4(es_1_pos),
    .in_reg5(es_1_mb),

    .in_reg6({16'h0, es_2_cycles, 7'h0, es_2_signal}),
    //.in_reg7(es_2_pos[31:0]),
    .in_reg8(es_2_pos),
    .in_reg9(es_2_mb),

    .in_reg10({16'h0, es_3_cycles, 7'h0, es_3_signal}),
    //.in_reg11(es_3_pos[31:0]),
    .in_reg12(es_3_pos),
    .in_reg13(es_3_mb),

    .in_reg14(apg_x_x[63:32]),
    .in_reg15(apg_x_v),
    .in_reg16(apg_y_x[63:32]),
    .in_reg17(apg_y_v),
    .in_reg18(apg_z_x[63:32]),
    .in_reg19(apg_z_v),

    .in_reg61(ext_pending_ints),
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
    .out_reg20(out_reg20),
    .out_reg21(out_reg21),
    .out_reg22(out_reg22),
    .out_reg23(out_reg23),
    .out_reg24(out_reg24),
    .out_reg25(out_reg25),
    .out_reg26(out_reg26),
    .out_reg27(out_reg27),
    .out_reg28(out_reg28),
    .out_reg29(out_reg29),
    .out_reg30(out_reg30),
    .out_reg31(out_reg31),
    .out_reg32(out_reg32),
    .out_reg33(out_reg33),
    .out_reg34(out_reg34),
    .out_reg35(out_reg35),
    .out_reg36(out_reg36),
    .out_reg37(out_reg37),
    .out_reg38(out_reg38),
    .out_reg39(out_reg39),

    .out_reg62(be_start_addr),
    .out_reg63(se_reg_lb),

    .out_stbs(stbs),

    .int0(asg_done),
    .int1(asg_abort),
    .int2(es_1_signal_changed),
    .int3(es_2_signal_changed),
    .int4(es_3_signal_changed),
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
assign endstops_unlock = stbs[1];

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

reg endstop_x1_buf;
reg endstop_x2_buf;
reg endstop_y_buf;

always @(posedge clk) begin
	endstop_x1_buf <= endstop_x1;
	endstop_x2_buf <= endstop_x2;
	endstop_y_buf <= endstop_y;
end

assign led[3:0] = out_reg0[3:0];
assign led[4] = endstop_x1_buf;
assign led[5] = endstop_x2_buf;
assign led[6] = endstop_y_buf;
assign led[7] = blink_cnt[23];

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
           .abort(asg_abort_chain_1),
           .step_stb(asg_step),
           .done(asg_done)
       );

acc_profile_gen apg_x(
           .clk(clk),
           .reset(n_rdy),
           .acc_step(asg_step),
           .load(asg_load),
           .set_x(apg_x_set_x),
           .set_v(apg_x_set_v),
           .set_a(apg_x_set_a),
           .set_j(apg_x_set_j),
           .set_jj(apg_x_set_jj),
           .set_target_v(apg_x_set_target_v),
           .x_val(apg_x_x_val),
           .v_val(apg_x_v_val),
           .a_val(apg_x_a_val),
           .j_val(apg_x_j_val),
           .jj_val(apg_x_jj_val),
           .target_v_val(apg_x_target_v_val),
           .abort_a_val(apg_x_abort_a),
           .step_bit(32),
           .abort(asg_abort),
           .x(apg_x_x),
           .v(apg_x_v),
           .a(),
           .j(),
           .jj(),
           .step_start_x(),
           .step_start_v(),
           .step(apg_x_step),
           .dir(apg_x_dir),
           .stopped(apg_x_stopped)
);

motor_step_gen msg_x(
           .clk(clk),
           .reset(n_rdy),
           .pre_n(msg_all_pre_n),
           .pulse_n(msg_all_pulse_n),
           .post_n(msg_all_post_n),
           .step_stb(apg_x_step),
           .step_dir(apg_x_dir),
           .step(mot_x_step),
           .dir(mot_x_dir),
           .missed()
);

acc_profile_gen apg_y(
           .clk(clk),
           .reset(n_rdy),
           .acc_step(asg_step),
           .load(asg_load),
           .set_x(apg_y_set_x),
           .set_v(apg_y_set_v),
           .set_a(apg_y_set_a),
           .set_j(apg_y_set_j),
           .set_jj(apg_y_set_jj),
           .set_target_v(apg_y_set_target_v),
           .x_val(apg_y_x_val),
           .v_val(apg_y_v_val),
           .a_val(apg_y_a_val),
           .j_val(apg_y_j_val),
           .jj_val(apg_y_jj_val),
           .target_v_val(apg_y_target_v_val),
           .abort_a_val(apg_y_abort_a),
           .step_bit(32),
           .abort(asg_abort),
           .x(apg_y_x),
           .v(apg_y_v),
           .a(),
           .j(),
           .jj(),
           .step_start_x(),
           .step_start_v(),
           .step(apg_y_step),
           .dir(apg_y_dir),
           .stopped(apg_y_stopped)
);

motor_step_gen msg_y(
           .clk(clk),
           .reset(n_rdy),
           .pre_n(msg_all_pre_n),
           .pulse_n(msg_all_pulse_n),
           .post_n(msg_all_post_n),
           .step_stb(apg_y_step),
           .step_dir(apg_y_dir),
           .step(mot_y_step),
           .dir(mot_y_dir),
           .missed()
);

acc_profile_gen apg_z(
           .clk(clk),
           .reset(n_rdy),
           .acc_step(asg_step),
           .load(asg_load),
           .set_x(apg_z_set_x),
           .set_v(apg_z_set_v),
           .set_a(apg_z_set_a),
           .set_j(apg_z_set_j),
           .set_jj(apg_z_set_jj),
           .set_target_v(apg_z_set_target_v),
           .x_val(apg_z_x_val),
           .v_val(apg_z_v_val),
           .a_val(apg_z_a_val),
           .j_val(apg_z_j_val),
           .jj_val(apg_z_jj_val),
           .target_v_val(apg_z_target_v_val),
           .abort_a_val(apg_z_abort_a),
           .step_bit(32),
           .abort(asg_abort),
           .x(apg_z_x),
           .v(apg_z_v),
           .a(),
           .j(),
           .jj(),
           .step_start_x(),
           .step_start_v(),
           .step(apg_z_step),
           .dir(apg_z_dir),
           .stopped(apg_z_stopped)
);

motor_step_gen msg_z(
           .clk(clk),
           .reset(n_rdy),
           .pre_n(msg_all_pre_n),
           .pulse_n(msg_all_pulse_n),
           .post_n(msg_all_post_n),
           .step_stb(apg_z_step),
           .step_dir(apg_z_dir),
           .step(mot_z_step),
           .dir(mot_z_dir),
           .missed()
);


wire [31:0] endstops_timeout;
wire [31:0] endstops_options;
assign endstops_timeout = out_reg32;
assign endstops_options = out_reg33;

endstop_with_mux es_1(
    .clk(clk),
    .reset(n_rdy),
    .x(apg_x_x[63:32]),
    .y(apg_y_x[63:32]),
    .z(apg_z_x[63:32]),
    .signal_in(endstop_x1),
    .abort_in(asg_abort_chain_1),
    .unlock(endstops_unlock),
    .mux_select(endstops_options[1:0]),
    .abort_polarity(endstops_options[2]),
    .abort_enabled(endstops_options[3]),
    .timeout(endstops_timeout),
    .pos_out(es_1_pos),
    .max_bounce(es_1_mb),
    .cycles(es_1_cycles),
    .signal(es_1_signal),
    .signal_changed(es_1_signal_changed),
    .abort_out(asg_abort_chain_2)
);

endstop_with_mux es_2(
    .clk(clk),
    .reset(n_rdy),
    .x(apg_x_x[63:32]),
    .y(apg_y_x[63:32]),
    .z(apg_z_x[63:32]),
    .signal_in(endstop_x2),
    .abort_in(asg_abort_chain_2),
    .unlock(endstops_unlock),
    .mux_select(endstops_options[5:4]),
    .abort_polarity(endstops_options[6]),
    .abort_enabled(endstops_options[7]),
    .timeout(endstops_timeout),
    .pos_out(es_2_pos),
    .max_bounce(es_2_mb),
    .cycles(es_2_cycles),
    .signal(es_2_signal),
    .signal_changed(es_2_signal_changed),
    .abort_out(asg_abort_chain_3)
);

endstop_with_mux es_3(
    .clk(clk),
    .reset(n_rdy),
    .x(apg_x_x[63:32]),
    .y(apg_y_x[63:32]),
    .z(apg_z_x[63:32]),
    .signal_in(endstop_y),
    .abort_in(asg_abort_chain_3),
    .unlock(endstops_unlock),
    .mux_select(endstops_options[9:8]),
    .abort_polarity(endstops_options[10]),
    .abort_enabled(endstops_options[11]),
    .timeout(endstops_timeout),
    .pos_out(es_3_pos),
    .max_bounce(es_3_mb),
    .cycles(es_3_cycles),
    .signal(es_3_signal),
    .signal_changed(es_3_signal_changed),
    .abort_out(asg_abort)
);

endmodule
