module profile_gen(
    input clk,
    input rst,
    input acc_step,
    output reg busy,
    output reg done,

    output reg signed [63:0] speed_0,
    output reg signed [63:0] speed_1,
    output reg signed [63:0] speed_2,
    output reg signed [63:0] speed_3,
    output reg signed [63:0] speed_4,
    output reg signed [63:0] speed_5,
    output reg signed [63:0] speed_6,
    output reg signed [63:0] speed_7,

    input [7:0] param_addr,
    input [31:0] param_in,
    output signed [63:0] param_out,
    input param_write_hi,
    input param_write_lo,
    input [7:0] abort,
    output reg [7:0] pending_aborts,
    output reg [7:0] done_aborts
);

    reg reg_write;
    reg [7:0] reg_addr;
    reg signed [63:0] reg_in;
    wire signed [63:0] reg_out;

    reg [31:0] mem0 [0:255];
    reg [31:0] mem1 [0:255];
    reg [7:0] addrA;
    reg [7:0] addrB;

    assign param_out[31:0] = mem0[addrA];
    assign param_out[63:32] = mem1[addrA];
    assign reg_out[31:0] = mem0[addrB];
    assign reg_out[63:32] = mem1[addrB];

    always @(posedge clk) begin
        if (param_write_lo)
            mem0[param_addr] <= param_in;

        if (param_write_hi)
            mem1[param_addr] <= param_in;

        if (reg_write) begin
            mem0[reg_addr] <= reg_in[31:0];
            mem1[reg_addr] <= reg_in[63:32];
        end
        addrA <= param_addr;
        addrB <= reg_addr;
    end

    reg [7:0] next_done_aborts;

    always @(posedge clk) begin
        if (rst)
            pending_aborts <= 0;
        else
            pending_aborts <= (pending_aborts | abort) & ~done_aborts;
    end

    reg [5:0] state;
    reg [5:0] next_state;
    reg [2:0] channel;
    reg [2:0] next_channel;
    reg [4:0] reg_num;
    reg [4:0] next_reg_num;

    reg [7:0] next_abort_in_progress;
    reg [7:0] abort_in_progress;

    reg signed [63:0] arg0;
    reg signed [63:0] next_arg0;
    reg signed [63:0] arg1;
    reg signed [63:0] next_arg1;

    reg [63:0] next_speed_value;
    reg next_speed_stb;

    reg [63:0] next_reg_in;
    reg next_reg_write;
    reg next_busy;
    reg next_done;
    reg target_v_set;
    reg next_target_v_set;

    wire signed [63:0] args_sum;
    wire signed [63:0] args_sum_2;

    assign args_sum = arg0+arg1;
    assign args_sum_2 = {args_sum[63], args_sum[63:1]};

    localparam
        S_INIT=0,
        S_START=1,
        S_NEXT=2,
        S_READ_STATUS=3,
        S_READ_STATUS2=4,
        S_SAVE_V=5,
        S_START_ABORT=6,

        R_STATUS=0,
        R_V_EFF=1,
        R_V_IN=2,
        R_V_OUT=3,
        R_A=4,
        R_J=5,
        R_JJ=6,
        R_TARGET_V=7,
        R_ABORT_A=8,

        STATUS_ENABLE_BIT=0,
        STATUS_ENABLE_MASK=32'h1 << STATUS_ENABLE_BIT,
        STATUS_TARGET_V_BIT=0,
        STATUS_TARGET_V_MASK=32'h1 << STATUS_TARGET_V_BIT;

    always @(*) begin
        next_state <= state;
        next_channel <= channel;
        next_arg0 <= arg0;
        next_arg1 <= arg1;
        next_busy <= busy;
        next_target_v_set <= target_v_set;
        next_abort_in_progress <= abort_in_progress;

        next_reg_num <= 0;
        next_reg_in <= 0;
        next_reg_write <= 0;
        next_speed_value <= 0;
        next_speed_stb <= 0;
        next_done_aborts <= 0;
        next_done <= 0;

        if (rst) begin
            next_state <= S_INIT;
            next_channel <= 0;
            next_arg0 <= 0;
            next_arg1 <= 0;
            next_busy <= 0;
            next_target_v_set <= 0;
            next_abort_in_progress <= 0;
        end
        else begin
            case (state)
                S_INIT: begin
                    if (acc_step) begin
                        next_channel <= 0;
                        next_reg_num <= R_STATUS;  // Read JJ
                        next_state <= S_READ_STATUS;
                        next_busy <= 1;
                    end
                end
                // ram: read R_STATUS   ram_out: ---      arg0: ---     arg1: ---    sum: ---
                S_READ_STATUS: begin
                    next_state <= S_READ_STATUS2;
                end
                // ram: ---    ram_out: R_STATUS     arg0: ---     arg1: ---    sum: ---
                S_READ_STATUS2: begin
                    if (!reg_out[0]) begin
                        // Not enabled, skipping
                        if (pending_aborts[channel]) begin
                            next_abort_in_progress[channel] <= 0;
                            next_done_aborts[channel] <= 1;
                        end
                        if (channel == 7) begin
                            next_state <= S_INIT;
                            next_busy <= 0;
                            next_done <= 1;
                        end
                        else begin
                            next_channel <= channel+1;
                            next_reg_num <= R_STATUS;
                            next_state <= S_READ_STATUS;
                        end
                    end
                    else if (pending_aborts[channel] && !abort_in_progress[channel]) begin
                        next_reg_num <= R_STATUS;
                        next_reg_in <= reg_out | 32'b10; // TARGET_V
                        next_reg_write <= 1;
                        next_abort_in_progress[channel] <= 1;
                        next_state <= S_START_ABORT;
                    end
                    else begin
                        next_target_v_set <= reg_out[1];
                        next_reg_num <= R_JJ;
                        next_state <= S_START;
                    end
                end
                // ram: read R_JJ   ram_out: ---      arg0: ---     arg1: ---    sum: ---
                S_START: begin  //  Read J
                    next_reg_num <= R_J;
                    next_state <= 10;
                end
                // ram: read R_J    ram_out: R_JJ     arg0: ---     arg1: ---    sum: ---
                10: begin
                    next_arg0 <= reg_out;  // R_JJ
                    next_state <= state+1;
                end
                // ram: ---         ram_out: R_J      arg0: JJ      arg1: ---    sum: ---
                11: begin
                    next_arg1 <= reg_out;  // R_J
                    next_state <= state+1;
                end
                // ram: ---        ram out: ---       arg0: JJ     arg1: J       sum: JJ + J
                12: begin
                    next_reg_num <= R_J;
                    next_reg_in <= args_sum; // J + JJ
                    next_reg_write <= 1;
                    next_state <= state+1;
                end
                // ram: J + JJ -> J   ram_out: ---    arg0: JJ     arg1: J       sum: JJ + J
                13: begin  //  Read A
                    next_reg_num <= R_A;
                    next_state <= state+1;
                end
                // ram: read R_A    ram_out: ---     arg0:  JJ     arg1: J       sum:JJ + J
                14: begin  //  NOP
                    next_state <= state+1;
                end
                // ram: ---    ram_out: R_A      arg0:  JJ     arg1: J       sum: A + J
                15: begin  //  Use A
                    next_arg0 <= reg_out;  // R_A
                    next_state <= state+1;
                end
                // ram: ---    ram_out: ---     arg0:  A     arg1: J       sum: A + J
                16: begin
                    next_reg_num <= R_A;
                    next_reg_in <= args_sum; // A + J
                    next_reg_write <= 1;
                    next_state <= state+1;
                end
                // ram: J + A -> A   ram_out: ---    arg0: A     arg1: J       sum: A + J
                17: begin  //  Read V_OUT
                    next_reg_num <= R_V_OUT;
                    next_state <= state+1;
                end
                // ram: read R_V_OUT   ram_out: ---     arg0:  A    arg1: J       sum: A + J
                18: begin  //  NOP
                    next_state <= state+1;
                end
                // ram: ---    ram_out: R_V_OUT    arg0:  A     arg1: J       sum: A + J
                19: begin
                    next_arg1 <= reg_out;
                    next_reg_num <= R_V_IN;
                    next_reg_in <= reg_out;
                    next_reg_write <= 1;
                    next_state <= state+1;
                end
                // ram: Write V_OUT -> V_IN   ram_out: ---     arg0:  A     arg1: R_V_OUT       sum: A + V_OUT
                20: begin
                    if (target_v_set) begin
                        next_reg_num <= R_TARGET_V;
                        next_state <= state+1;
                    end
                    else begin
                        next_arg0 <= args_sum;
                        next_reg_num <= R_V_OUT;
                        next_reg_in <= args_sum;
                        next_reg_write <= 1;
                        next_state <= S_SAVE_V;
                    end
                end
                21: begin
                    next_state <= state+1;
                end
                22: begin
                    if (((arg1 <= reg_out) && (reg_out <= args_sum)) || ((args_sum <= reg_out) && (reg_out <= arg1))) begin
                        next_arg0 <= reg_out;
                        next_reg_num <= R_A;
                        next_reg_in <= 0;
                        next_reg_write <= 1;
                        if (abort_in_progress[channel] && (arg1 == reg_out)) begin
                            // Will be triggered on first hit, if next_v == target
                            // or on the second cycle in other cases
                            // as A==0, we are guaranted to get hit
                            // on the second cycle
                            next_abort_in_progress[channel] <= 0;
                            next_done_aborts[channel] <= 1;
                        end
                        next_state <= state+1;
                    end
                    else begin
                        next_arg0 <= args_sum;
                        next_reg_num <= R_V_OUT;
                        next_reg_in <= args_sum;
                        next_reg_write <= 1;
                        next_state <= S_SAVE_V;
                    end
                end
                23: begin
                    next_reg_num <= R_J;
                    next_reg_in <= 0;
                    next_reg_write <= 1;
                    next_state <= state+1;
                end
                24: begin
                    next_reg_num <= R_JJ;
                    next_reg_in <= 0;
                    next_reg_write <= 1;
                    next_state <= state+1;
                end
                25: begin
                    next_reg_num <= R_V_OUT;
                    next_reg_in <= arg0;
                    next_reg_write <= 1;
                    next_state <= S_SAVE_V;
                end
                // ram: Write A + V_OUT -> V_OUT  ram_out: ---     arg0:  R_V_OUT + A     arg1: R_V_OUT       sum: A + V_OUT*2
                S_SAVE_V: begin
                    next_reg_num <= R_V_EFF;
                    next_reg_in <= args_sum_2; // R_V_OUT + A
                    next_reg_write <= 1;
                    next_state <= S_NEXT;
                    next_speed_value <= args_sum_2;
                    next_speed_stb <= 1;
                end
                // ram: write R_V_OUT + A -> R_V_OUT     sum: R_V_OUT*2 + A   arg0: R_V_OUT + A     arg1: R_V_OUT(last)

                S_NEXT: begin
                    // next cycle
                    next_arg0 <= 0;
                    next_arg1 <= 0;
                    if (channel == 7) begin
                        next_state <= S_INIT;
                        next_busy <= 0;
                        next_done <= 1;
                    end
                    else begin
                        next_channel <= channel+1;
                        next_reg_num <= R_STATUS;
                        next_state <= S_READ_STATUS;
                    end
                end
                S_START_ABORT: begin
                    next_reg_num <= R_ABORT_A;
                    next_state <= 40;
                end
                40: begin
                    next_reg_num <= R_JJ;
                    next_reg_in <= 0;
                    next_reg_write <= 1;
                    next_state <= state+1;
                end
                41: begin
                    next_arg0 <= reg_out;
                    next_reg_num <= R_V_OUT;
                    next_state <= state+1;
                end
                42: begin
                    next_reg_num <= R_J;
                    next_reg_in <= 0;
                    next_reg_write <= 1;
                    next_state <= state+1;
                end
                43: begin
                    if (arg0 == 0)
                        next_arg0 <= -reg_out;
                    else if (reg_out > 0)
                        next_arg0 <= -arg0;
                    next_reg_num <= R_TARGET_V;
                    next_reg_in <= 0;
                    next_reg_write <= 1;
                    next_state <= state+1;
                end
                44: begin
                    next_reg_num <= R_A;
                    next_reg_in <= arg0;
                    next_reg_write <= 1;
                    next_state <= state+1;
                end
                45: begin
                    next_reg_num <= R_STATUS;
                    next_state <= S_READ_STATUS;
                end
            endcase
        end
    end

    always @(posedge clk) begin
        state <= next_state;
        channel <= next_channel;
        arg0 <= next_arg0;
        arg1 <= next_arg1;
        busy <= next_busy;
        done <= next_done;
        target_v_set <= next_target_v_set;
        done_aborts <= next_done_aborts;
        abort_in_progress <= next_abort_in_progress;

        reg_num <= next_reg_num;
        reg_in <= next_reg_in;
        reg_write <= next_reg_write;
        reg_addr <= {next_channel, next_reg_num};
    end

    always @(posedge clk) begin
        if (rst) begin
            speed_0 <= 0;
            speed_1 <= 0;
            speed_2 <= 0;
            speed_3 <= 0;
            speed_4 <= 0;
            speed_5 <= 0;
            speed_6 <= 0;
            speed_7 <= 0;
        end
        else if (next_speed_stb)
            case (next_channel)
                0: speed_0 <= next_speed_value;
                1: speed_1 <= next_speed_value;
                2: speed_2 <= next_speed_value;
                3: speed_3 <= next_speed_value;
                4: speed_4 <= next_speed_value;
                5: speed_5 <= next_speed_value;
                6: speed_6 <= next_speed_value;
                7: speed_7 <= next_speed_value;
            endcase
    end


endmodule