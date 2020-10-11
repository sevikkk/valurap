module profile_gen(
    input clk,
    input rst,
    input acc_step,
    output reg busy,

    output reg [63:0] speed_0,
    output reg [63:0] speed_1,
    output reg [63:0] speed_2,
    output reg [63:0] speed_3,
    output reg [63:0] speed_4,
    output reg [63:0] speed_5,
    output reg [63:0] speed_6,
    output reg [63:0] speed_7,

    input [7:0]  param_addr,
    input [31:0] param_in,
    output [63:0] param_out,
    input param_write_hi,
    input param_write_lo
);
    reg reg_write;
    reg [7:0] reg_addr;
    reg [63:0] reg_in;
    wire [63:0] reg_out;

    reg [31:0] mem0 [0:255];
    reg [31:0] mem1 [0:255];
    reg [7:0] addrA;
    reg [7:0] addrB;

    assign param_out[31:0] = mem0[addrA];
    assign param_out[63:32] = mem1[addrA];
    assign reg_out[31:0] = mem0[addrB];
    assign reg_out[63:32] = mem1[addrB];

    always @( posedge clk) begin
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

    reg [5:0] state;
    reg [5:0] next_state;
    reg [2:0] channel;
    reg [2:0] next_channel;
    reg [4:0] reg_num;
    reg [4:0] next_reg_num;

    reg signed [63:0] arg0;
    reg signed [63:0] next_arg0;
    reg signed [63:0] arg1;
    reg signed [63:0] next_arg1;

    reg [63:0] next_speed_0;
    reg [63:0] next_speed_1;
    reg [63:0] next_speed_2;
    reg [63:0] next_speed_3;
    reg [63:0] next_speed_4;
    reg [63:0] next_speed_5;
    reg [63:0] next_speed_6;
    reg [63:0] next_speed_7;

    reg [63:0] next_reg_in;
    reg next_reg_write;
    reg next_busy;
    reg target_v_set;
    reg next_target_v_set;

    wire [63:0] args_sum;
    wire [63:0] args_sum_2;

    assign args_sum = arg0 + arg1;
    assign args_sum_2 = {args_sum[63], args_sum[63:1]};

    localparam
        S_INIT = 0,
        S_START = 1,
        S_NEXT = 2,
        S_READ_STATUS = 3,
        S_READ_STATUS2 = 4,

        R_STATUS = 0,
        R_V_EFF = 1,
        R_V_IN = 2,
        R_V_OUT = 3,
        R_A = 4,
        R_J = 5,
        R_JJ = 6,
        R_TARGET_V = 7;

    always @(*) begin
        next_state <= state;
        next_channel <= channel;
        next_arg0 <= arg0;
        next_arg1 <= arg1;
        next_busy <= busy;
        next_target_v_set <= target_v_set;

        next_speed_0 <= speed_0;
        next_speed_1 <= speed_1;
        next_speed_2 <= speed_2;
        next_speed_3 <= speed_3;
        next_speed_4 <= speed_4;
        next_speed_5 <= speed_5;
        next_speed_6 <= speed_6;
        next_speed_7 <= speed_7;

        next_reg_num <= 0;
        next_reg_in <= 0;
        next_reg_write <= 0;

        if (rst) begin
            next_state <= S_INIT;
            next_channel <= 0;
            next_arg0 <= 0;
            next_arg1 <= 0;
            next_speed_0 <= 0;
            next_speed_1 <= 0;
            next_speed_2 <= 0;
            next_speed_3 <= 0;
            next_speed_4 <= 0;
            next_speed_5 <= 0;
            next_speed_6 <= 0;
            next_speed_7 <= 0;
            next_busy <= 0;
            next_target_v_set <= 0;
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
                        if (channel == 7) begin
                            next_state <= S_INIT;
                            next_busy <= 0;
                        end
                        else begin
                            next_channel <= channel + 1;
                            next_reg_num <= R_STATUS;
                            next_state <= S_READ_STATUS;
                        end
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
                    next_state <= state + 1;
                end
                // ram: ---         ram_out: R_J      arg0: JJ      arg1: ---    sum: ---
                11: begin
                    next_arg1 <= reg_out;  // R_J
                    next_state <= state + 1;
                end
                // ram: ---        ram out: ---       arg0: JJ     arg1: J       sum: JJ + J
                12: begin
                    next_reg_num <= R_J;
                    next_reg_in <= args_sum; // J + JJ
                    next_reg_write <= 1;
                    next_state <= state + 1;
                end
                // ram: J + JJ -> J   ram_out: ---    arg0: JJ     arg1: J       sum: JJ + J
                13: begin  //  Read A
                    next_reg_num <= R_A;
                    next_state <= state + 1;
                end
                // ram: read R_A    ram_out: ---     arg0:  JJ     arg1: J       sum:JJ + J
                14: begin  //  NOP
                    next_state <= state + 1;
                end
                // ram: ---    ram_out: R_A      arg0:  JJ     arg1: J       sum: A + J
                15: begin  //  Use A
                    next_arg0 <= reg_out;  // R_A
                    next_state <= state + 1;
                end
                // ram: ---    ram_out: ---     arg0:  A     arg1: J       sum: A + J
                16: begin
                    next_reg_num <= R_A;
                    next_reg_in <= args_sum; // A + J
                    next_reg_write <= 1;
                    next_state <= state + 1;
                end
                // ram: J + A -> A   ram_out: ---    arg0: A     arg1: J       sum: A + J
                17: begin  //  Read V_OUT
                    next_reg_num <= R_V_OUT;
                    next_state <= state + 1;
                end
                // ram: read R_V_OUT   ram_out: ---     arg0:  A    arg1: J       sum: A + J
                18: begin  //  NOP
                    next_state <= state + 1;
                end
                // ram: ---    ram_out: R_V_OUT    arg0:  A     arg1: J       sum: A + J
                19: begin
                    next_arg1 <= reg_out;
                    next_reg_num <= R_V_IN;
                    next_reg_in <= reg_out;
                    next_reg_write <= 1;
                    next_state <= state + 1;
                end
                // ram: Write V_OUT -> V_IN   ram_out: ---     arg0:  A     arg1: R_V_OUT       sum: A + V_OUT
                20: begin
                    next_arg0 <= args_sum;
                    next_reg_num <= R_V_OUT;
                    next_reg_in <= args_sum;
                    next_reg_write <= 1;
                    next_state <= state + 1;
                end
                // ram: Write A + V_OUT -> V_OUT  ram_out: ---     arg0:  R_V_OUT + A     arg1: R_V_OUT       sum: A + V_OUT*2
                21: begin
                    next_reg_num <= R_V_EFF;
                    next_reg_in <= args_sum_2; // R_V_OUT + A
                    next_reg_write <= 1;
                    next_state <= S_NEXT;
                    case (channel)
                        0: next_speed_0 <= args_sum_2;
                        1: next_speed_1 <= args_sum_2;
                        2: next_speed_2 <= args_sum_2;
                        3: next_speed_3 <= args_sum_2;
                        4: next_speed_4 <= args_sum_2;
                        5: next_speed_5 <= args_sum_2;
                        6: next_speed_6 <= args_sum_2;
                        7: next_speed_7 <= args_sum_2;
                    endcase
                end
                // ram: write R_V_OUT + A -> R_V_OUT     sum: R_V_OUT*2 + A   arg0: R_V_OUT + A     arg1: R_V_OUT(last)

                S_NEXT: begin
                    // next cycle
                    next_arg0 <= 0;
                    next_arg1 <= 0;
                    if (channel == 7) begin
                        next_state <= S_INIT;
                        next_busy <= 0;
                    end
                    else begin
                        next_channel <= channel + 1;
                        next_reg_num <= R_STATUS;
                        next_state <= S_READ_STATUS;
                    end
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
        target_v_set <= next_target_v_set;

        speed_0 <= next_speed_0;
        speed_1 <= next_speed_1;
        speed_2 <= next_speed_2;
        speed_3 <= next_speed_3;
        speed_4 <= next_speed_4;
        speed_5 <= next_speed_5;
        speed_6 <= next_speed_6;
        speed_7 <= next_speed_7;

        reg_num <= next_reg_num;
        reg_in <= next_reg_in;
        reg_write <= next_reg_write;
        reg_addr <= {next_channel, next_reg_num};
    end

endmodule