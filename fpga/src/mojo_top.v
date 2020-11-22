module mojo_top#(
    parameter CLK_RATE=50000000,
    parameter EXT_BAUD_RATE=1500000,
    parameter FIFO_ADDRESS_WIDTH=13,
    parameter STEP_BIT=32,
    parameter X_BITS=20
)(
    // 50MHz clock input
    input clk,
    // Input from reset button (active low)
    input rst_n,
    // cclk input from AVR, high when AVR is ready
    input cclk,
    // Outputs to the 8 onboard LEDs
    output [7:0] led,
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

    input endstop_x1,  // ext1_3
    input endstop_x2,  // ext1_5
    input endstop_y1,  // ext1_4
    input endstop_y2,  // ext1_6
    input endstop_z1,  // ext1_1
    input endstop_z2,  // ext1_2
    input endstop_z3,  // ext1_7
    input endstop_z4,  // ext1_8

    output ext2_1,
    output ext2_2,
    output ext2_3,
    output ext2_4,
    output ext2_5,
    output ext2_6,
    output ext2_7,
    output ext2_8,

    output stm_rx,   // ext3_2
    input stm_tx,    // ext3_4
    output stm_int,  // ext3_6
    input stm_alive, // ext3_8

    output stm_miso, // ext3_1
    input stm_mosi,  // ext3_3
    input stm_sck,   // ext3_5
    input stm_ss     // ext3_7
);

    wire rst = ~rst_n; // make reset active high

// these signals should be high-z when not used
    assign spi_miso = 1'bz;
    assign avr_rx = 1'bz;
    assign spi_channel = 4'bzzzz;

    wire ready;
    wire n_rdy = !ready;

    cclk_detector#(.CLK_RATE(CLK_RATE)) cclk_detector(
        .clk(clk),
        .rst(rst),
        .cclk(cclk),
        .ready(ready)
    );

    reg [23:0] blink_cnt = 0;

    always @(posedge clk)
        blink_cnt <= blink_cnt+1;

    assign led[7:0] = blink_cnt[23:16];

    assign avr_rx = 1'b1;
    assign stm_rx = 1'b1;

    assign stm_int = 1'b0;
    assign stm_miso = 1'b0;

    assign ext2_1 = blink_cnt[17];
    assign ext2_2 = blink_cnt[16];
    assign ext2_3 = blink_cnt[15];
    assign ext2_4 = blink_cnt[14];
    assign ext2_5 = blink_cnt[13];
    assign ext2_6 = blink_cnt[12];
    assign ext2_7 = blink_cnt[11];
    assign ext2_8 = blink_cnt[10];

    wire [7:0] tx_data;
    wire tx_wr;
    wire tx_done;

    wire [7:0] rx_data;
    wire rx_done;
    wire enable_16;

    dds_uart_clock uclock(
        .clk(clk),
        .baudrate(EXT_BAUD_RATE/100),
        .enable_16(enable_16)
    );

    uart_transceiver uart(
        .sys_clk(clk),
        .sys_rst(n_rdy),
        .uart_rx(ext_tx),
        .uart_tx(ext_rx),
        .enable_16(enable_16),
        .rx_data(rx_data),
        .rx_done(rx_done),
        .tx_data(tx_data),
        .tx_wr(tx_wr),
        .tx_done(tx_done)
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

    s3g_rx s3g_rx(
        .clk(clk),
        .rst(n_rdy),
        .rx_data(rx_data),
        .rx_done(rx_done),
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

    s3g_tx s3g_tx(
        .clk(clk),
        .rst(n_rdy),
        .tx_data(tx_data),
        .tx_wr(tx_wr),
        .tx_done(tx_done),
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

    wire [31:0] stbs;

    wire [31:0] ext_out_stbs;

    wire [31:0] ext_out_reg_data;
    wire [5:0] ext_out_reg_addr;
    wire ext_out_reg_stb;
    wire ext_out_reg_busy;

    wire [31:0] ext_pending_ints;
    wire [31:0] ext_clear_ints;

    wire [39:0] ext_fifo_data;
    wire ext_fifo_wr;
    wire [31:0] ext_fifo_free_space;
    wire [31:0] ext_fifo_data_count;

    wire be_done;
    wire [7:0] done_aborts;

    wire asg_done;

    wire [31:0] dt_val;
    wire [31:0] steps_val;
    wire [31:0] sp_config;

    wire load_next_params;

    wire [16*12:0] motor_cfg;
    wire [X_BITS-1:0] motor_x [0:11];
    wire [X_BITS-1:0] motor_hold [0:11];
    wire [31:0] pre_n;
    wire [31:0] pulse_n;
    wire [31:0] post_n;
    wire [31:0] motor_x_val;

    wire [31:0] es_timeout;
    wire [31:0] reg_loopback;
    wire [31:0] be_status;
    wire [31:0] apg_status;
    wire [31:0] es_status;

    wire global_abort;

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

        .out_stbs(stbs),

        .ext_fifo_data(ext_fifo_data),
        .ext_fifo_wr(ext_fifo_wr),
        .ext_fifo_free_space(ext_fifo_free_space),

        .int0(be_done),
        .int1(load_next_params),
        .int2(asg_done),
        .int3(global_abort),
        .int4(1'b0),
        .int5(1'b0),
        .int6(1'b0),
        .int7(1'b0),
        .int8(done_aborts[0]),
        .int9(done_aborts[1]),
        .int10(done_aborts[2]),
        .int11(done_aborts[3]),
        .int12(done_aborts[4]),
        .int13(done_aborts[5]),
        .int14(done_aborts[6]),
        .int15(done_aborts[7]),
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
        .int30(1'b0),
        .int31(stbs[31]),

        .ext_out_reg_busy(ext_out_reg_busy),
        .ext_out_reg_data(ext_out_reg_data),
        .ext_out_reg_addr(ext_out_reg_addr),
        .ext_out_reg_stb(ext_out_reg_stb),

        .ext_pending_ints(ext_pending_ints),
        .ext_clear_ints(ext_clear_ints),
        .ext_out_stbs(ext_out_stbs),

        .out_reg0(dt_val),
        .out_reg1(steps_val),
        .out_reg2(sp_config),
        .out_reg3(pre_n),
        .out_reg4(pulse_n),
        .out_reg5(post_n),
        .out_reg6(motor_x_val),
        .out_reg7(motor_cfg[31:0]),
        .out_reg8(motor_cfg[63:32]),
        .out_reg9(motor_cfg[95:64]),
        .out_reg10(motor_cfg[127:96]),
        .out_reg11(motor_cfg[159:128]),
        .out_reg12(motor_cfg[191:160]),
        .out_reg13(es_timeout),
        .out_reg63(reg_loopback),

        .in_reg0(be_status),
        .in_reg1(apg_status),
        .in_reg2(es_status),
        .in_reg3(ext_fifo_free_space),
        .in_reg4(ext_fifo_data_count),
        .in_reg5({{32-X_BITS{1'b0}}, motor_hold[0]}),
        .in_reg6({{32-X_BITS{1'b0}}, motor_hold[1]}),
        .in_reg7({{32-X_BITS{1'b0}}, motor_hold[2]}),
        .in_reg8({{32-X_BITS{1'b0}}, motor_hold[3]}),
        .in_reg9({{32-X_BITS{1'b0}}, motor_hold[4]}),
        .in_reg10({{32-X_BITS{1'b0}}, motor_hold[5]}),
        .in_reg11({{32-X_BITS{1'b0}}, motor_hold[6]}),
        .in_reg12({{32-X_BITS{1'b0}}, motor_hold[7]}),
        .in_reg13({{32-X_BITS{1'b0}}, motor_hold[8]}),
        .in_reg14({{32-X_BITS{1'b0}}, motor_hold[9]}),
        .in_reg15({{32-X_BITS{1'b0}}, motor_hold[10]}),
        .in_reg16({{32-X_BITS{1'b0}}, motor_hold[11]}),
        .in_reg17({{32-X_BITS{1'b0}}, motor_x[0]}),
        .in_reg18({{32-X_BITS{1'b0}}, motor_x[1]}),
        .in_reg19({{32-X_BITS{1'b0}}, motor_x[2]}),
        .in_reg20({{32-X_BITS{1'b0}}, motor_x[3]}),
        .in_reg21({{32-X_BITS{1'b0}}, motor_x[4]}),
        .in_reg22({{32-X_BITS{1'b0}}, motor_x[5]}),
        .in_reg23({{32-X_BITS{1'b0}}, motor_x[6]}),
        .in_reg24({{32-X_BITS{1'b0}}, motor_x[7]}),
        .in_reg25({{32-X_BITS{1'b0}}, motor_x[8]}),
        .in_reg26({{32-X_BITS{1'b0}}, motor_x[9]}),
        .in_reg27({{32-X_BITS{1'b0}}, motor_x[10]}),
        .in_reg28({{32-X_BITS{1'b0}}, motor_x[11]}),

        .in_reg62(ext_pending_ints),
        .in_reg63(reg_loopback)
    );

    wire fifo_empty;
    wire fifo_read;
    wire [39:0] fifo_read_data;

    assign ext_fifo_free_space[31:FIFO_ADDRESS_WIDTH+1] = 0;
    assign ext_fifo_data_count[31:FIFO_ADDRESS_WIDTH+1] = 0;

    fifo#(.ADDRESS_WIDTH(FIFO_ADDRESS_WIDTH), .DATA_WIDTH(40)) fifo(
        .clk(clk),
        .reset(n_rdy),
        .write_data(ext_fifo_data),
        .write(ext_fifo_wr),
        .read_data(fifo_read_data),
        .read(fifo_read),
        .free_count(ext_fifo_free_space[FIFO_ADDRESS_WIDTH:0]),
        .data_count(ext_fifo_data_count[FIFO_ADDRESS_WIDTH:0]),
        .empty(fifo_empty)
    );

    wire [7:0] param_addr;
    wire [31:0] param_in;
    wire param_write_hi;
    wire param_write_lo;
    wire gated_param_write_hi;
    wire gated_param_write_lo;
    wire [7:0] pg_abort;
    wire [7:0] pending_aborts;
    wire start_calc;
    wire calc_done;
    wire load_speeds;

    wire [7:0] es_abort;

    assign pg_abort = stbs[15:8] | {8{global_abort}} | es_abort;

    buf_executor buf_exec(
        .clk(clk),
        .rst(n_rdy),
        .ext_out_reg_busy(ext_out_reg_busy),
        .ext_pending_ints(ext_pending_ints),
        .fifo_empty(fifo_empty),
        .fifo_data(fifo_read_data),
        .fifo_read(fifo_read),
        .fifo_global_count(ext_fifo_data_count),
        .fifo_local_count(ext_fifo_data_count),
        .ext_out_reg_addr(ext_out_reg_addr),
        .ext_out_reg_data(ext_out_reg_data),
        .ext_out_reg_stb(ext_out_reg_stb),
        .start(stbs[0]),
        .abort(stbs[1]),
        .param_addr(param_addr),
        .param_write_data(param_in),
        .param_write_hi(param_write_hi),
        .param_write_lo(param_write_lo),
        .done(be_done),
        .ext_out_stbs(ext_out_stbs),
        .ext_clear_ints(ext_clear_ints),
        .busy(be_status[0]),
        .aborting(be_status[1]),
        .waiting_for_data(be_status[2]),
        .waiting_for_int(be_status[3]),
        .aborted(be_status[4]),
        .buffer_underrun(be_status[5]),
        .bad_code(be_status[6])
    );

    wire [63:0] speed [0:7];

    profile_gen apg(
        .clk(clk),
        .rst(n_rdy),
        .acc_step(start_calc),
        .done(calc_done),
        .param_addr(param_addr),
        .param_in(param_in),
        .param_write_hi(gated_param_write_hi),
        .param_write_lo(gated_param_write_lo),
        .abort(pg_abort),
        .pending_aborts(pending_aborts),
        .done_aborts(done_aborts),
        .speed_0(speed[0]),
        .speed_1(speed[1]),
        .speed_2(speed[2]),
        .speed_3(speed[3]),
        .speed_4(speed[4]),
        .speed_5(speed[5]),
        .speed_6(speed[6]),
        .speed_7(speed[7])
    );

    acc_step_gen#(.MIN_LOAD_CYCLES(50)) asg(
        .clk(clk),
        .reset(n_rdy),
        .dt_val(dt_val),
        .steps_val(steps_val),
        .start(stbs[2]),
        .abort(stbs[3]),
        .param_write_hi(param_write_hi),
        .param_write_lo(param_write_lo),
        .gated_param_write_hi(gated_param_write_hi),
        .gated_param_write_lo(gated_param_write_lo),
        .params_load_done(stbs[4]),
        .pending_aborts(pending_aborts),
        .global_abort(global_abort),
        .start_calc(start_calc),
        .acc_calc_done(calc_done),
        .load_speeds(load_speeds),
        .load_next_params(load_next_params),
        .busy(apg_status[0]),
        .error_unexpected_params_write(apg_status[1]),
        .error_late_params(apg_status[2]),
        .error_abort_requested(apg_status[3]),

        .done(asg_done)
    );

    wire [7:0] es_inputs;

    assign es_inputs[0] = endstop_x1;
    assign es_inputs[1] = endstop_x2;
    assign es_inputs[2] = endstop_y1;
    assign es_inputs[3] = endstop_y2;
    assign es_inputs[4] = endstop_z1;
    assign es_inputs[5] = endstop_z2;
    assign es_inputs[6] = endstop_z3;
    assign es_inputs[7] = endstop_z4;

    wire [7:0] sp_steps;
    wire [7:0] sp_dirs;

    wire [11:0] mm_steps;
    wire [11:0] mm_dirs;
    wire [11:0] mm_holds;
    wire [11:0] motor_steps;
    wire [11:0] motor_dirs;
    wire [11:0] motor_enables;

    wire [7:0] es_holds;
    wire [7:0] es_stbs;


    genvar ch;
    generate
        for (ch = 0; ch < 8; ch = ch+1) begin : es_block
            debounce db(
                .clk(clk),
                .reset(n_rdy),
                .signal_in(es_inputs[ch]),
                .unlock(stbs[7]),
                .timeout(es_timeout),
                .signal(es_status[ch*4]),
                .locked(es_status[ch*4+1]),
                .hold(es_holds[ch]),
                .stb(es_stbs[ch])
            );
        end
    endgenerate

    generate
        for (ch = 0; ch < 6; ch = ch+1) begin : speeds_block
            speed_integrator sp(
                .clk(clk),
                .reset(n_rdy),
                .set_v(load_speeds),
                .set_x(stbs[5]),
                .x_val(64'b0),
                .v_val(speed[ch]),
                .step_bit(sp_config[5:0]),
                .dir(sp_dirs[ch]),
                .step(sp_steps[ch])
            );
        end
    endgenerate

    assign sp_dirs[6] = 1'b0;
    assign sp_steps[6] = 1'b0;
    assign sp_dirs[7] = 1'b0;
    assign sp_steps[7] = 1'b0;

    wire [11:0] mm_stbs;
    wire [7:0] es_aborts [0:12];

    assign es_aborts[0] = 8'b0;
    assign es_abort = es_aborts[12];

    generate
        for (ch = 0; ch < 12; ch = ch+1) begin : motors_block
            endstop_mux em(
                .holds(es_holds),
                .stbs(es_stbs),
                .mux_select(motor_cfg[16*ch+2:16*ch]),
                .hold(mm_holds[ch]),
                .stb(mm_stbs[ch])
            );

            motor_mux mm(
                .steps(sp_steps),
                .dirs(sp_dirs),
                .enable_es_abort(motor_cfg[16*ch+3]),
                .mux_select(motor_cfg[16*ch+6:16*ch+4]),
                .enable_step(motor_cfg[16*ch+7]),

                .in_aborts(es_aborts[ch]),
                .out_aborts(es_aborts[ch+1]),
                .es_abort(mm_stbs[ch]),
                .step(mm_steps[ch]),
                .dir(mm_dirs[ch])
            );

            motor_step_gen#(.X_BITS(X_BITS)) sg(
                .clk(clk),
                .reset(n_rdy),
                .pre_n(pre_n),
                .pulse_n(pulse_n),
                .post_n(post_n),
                .step_stb(mm_steps[ch]),
                .step_dir(mm_dirs[ch]),
                .set_x(motor_cfg[16*ch+9] & stbs[6]),
                .x_val(motor_x_val[X_BITS-1:0]),
                .x(motor_x[ch]),
                .hold(mm_holds[ch]),
                .x_hold(motor_hold[ch]),
                .invert_dir(motor_cfg[16*ch+8]),
                .step(motor_steps[ch]),
                .dir(motor_dirs[ch])
            );
            assign motor_enables[ch] = !motor_cfg[16*ch+15];
        end
    endgenerate

    assign mot_1_step = motor_steps[0];
    assign mot_1_dir = motor_dirs[0];
    assign mot_1_enable = motor_enables[0];

    assign mot_2_step = motor_steps[1];
    assign mot_2_dir = motor_dirs[1];
    assign mot_2_enable = motor_enables[1];

    assign mot_3_step = motor_steps[2];
    assign mot_3_dir = motor_dirs[2];
    assign mot_3_enable = motor_enables[2];

    assign mot_4_step = motor_steps[3];
    assign mot_4_dir = motor_dirs[3];
    assign mot_4_enable = motor_enables[3];

    assign mot_5_step = motor_steps[4];
    assign mot_5_dir = motor_dirs[4];
    assign mot_5_enable = motor_enables[4];

    assign mot_6_step = motor_steps[5];
    assign mot_6_dir = motor_dirs[5];
    assign mot_6_enable = motor_enables[5];

    assign mot_7_step = motor_steps[6];
    assign mot_7_dir = motor_dirs[6];
    assign mot_7_enable = motor_enables[6];

    assign mot_8_step = motor_steps[7];
    assign mot_8_dir = motor_dirs[7];
    assign mot_8_enable = motor_enables[7];

    assign mot_9_step = motor_steps[8];
    assign mot_9_dir = motor_dirs[8];
    assign mot_9_enable = motor_enables[8];

    assign mot_10_step = motor_steps[9];
    assign mot_10_dir = motor_dirs[9];
    assign mot_10_enable = motor_enables[9];

    assign mot_11_step = motor_steps[10];
    assign mot_11_dir = motor_dirs[10];
    assign mot_11_enable = motor_enables[10];

    assign mot_12_step = motor_steps[11];
    assign mot_12_dir = motor_dirs[11];
    assign mot_12_enable = motor_enables[11];

endmodule
