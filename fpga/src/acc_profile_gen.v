module acc_profile_gen(
           input clk,
           input reset,
           input acc_step,
           input load,
           input set_x,
           input set_v,
           input set_a,
           input set_j,
           input set_jj,
           input set_target_v,
           input signed [63:0] x_val,
           input signed [31:0] v_val,
           input signed [31:0] a_val,
           input signed [31:0] j_val,
           input signed [31:0] jj_val,
           input signed [31:0] target_v_val,
           input [5:0] step_bit,

           input abort,
           input signed [31:0] abort_a_val,

           output reg signed [63:0] x,
           output reg signed [31:0] v,
           output reg signed [31:0] a,
           output reg signed [31:0] j,
           output reg signed [31:0] jj,
           output reg signed [63:0] step_start_x,
           output reg signed [31:0] step_start_v,

           output reg step,
           output reg dir,
           output reg stopped
       );

reg signed [23:0] next_v;
reg signed [23:0] next_a;
reg signed [23:0] next_j;
reg signed [23:0] next_jj;
reg next_stopped;

reg target_set;
reg next_target_set;

reg signed [23:0] target_v;
reg signed [23:0] next_target_v;

reg signed [63:0] next_step_start_x;
reg signed [23:0] next_step_start_v;

wire signed [23:0] next_v_comb;
wire signed [31:0] next_v_comb1;
assign next_v_comb1 = {v, 8'b0} + a;
assign next_v_comb = next_v_comb1[31:8];

always @(reset, acc_step, load,
		set_v, set_a, set_j, set_jj, set_x,
		v_val, a_val, j_val, jj_val,
		v, a, j, jj,
		abort, abort_a_val,
		stopped,
		target_set, set_target_v, target_v_val, target_v,
		x, step_start_x, step_start_v)
    begin
        next_v <= v;
        next_a <= a;
        next_j <= j;
        next_jj <= jj;
        next_target_v <= target_v;
        next_target_set <= target_set;
        next_step_start_x <= step_start_x;
        next_step_start_v <= step_start_v;
        if (reset)
            begin
                next_v <= 0;
                next_a <= 0;
                next_j <= 0;
                next_jj <= 0;
                next_target_set <= 0;
                next_target_v <= 0;
                next_step_start_x <= 0;
                next_step_start_v <= 0;
            end
        else if (load)
            begin
                if (set_v)
                    begin
                        next_v <= v_val;
                        next_step_start_v <= v_val;
                    end
                if (set_v || set_x)
                    begin
                        next_step_start_x <= 64'h7ffffffffffffff;
                    end
                if (set_a)
                    next_a <= a_val;
                if (set_j)
                    next_j <= j_val;
                if (set_jj)
                    next_jj <= jj_val;

                if (set_target_v)
                    begin
                        next_target_set <= 1;
                        next_target_v <= target_v_val;
                    end
                else
                    begin
                        next_target_set <= 0;
                        next_target_v <= 0;
                    end
            end
        else if (acc_step)
            begin
                next_step_start_x <= x;
                next_step_start_v <= v;
                if (abort)
                    begin
                        next_jj <= 0;
                        next_j <= 0;
                        if (v != 0)
                            begin
                                if (v > abort_a_val)
                                    begin
                                        next_v <= v - abort_a_val;
                                        next_a <= 0;
                                    end
                                else if (v >= -abort_a_val)
                                    begin
                                        next_v <= 0;
                                        next_a <= 0;
                                    end
                                else
                                    begin
                                        next_v <= v + abort_a_val;
                                        next_a <= 0;
                                    end
                            end
                        else
                            begin
                                next_v <= 0;
                                next_a <= 0;
                            end
                    end
                else
                    begin
                        next_v <= next_v_comb;
                        next_a <= a + j;
                        next_j <= j + jj;
                        if (target_set)
                            begin
                                if (v == target_v)
                                    begin
                                        next_jj <= 0;
                                        next_j <= 0;
                                        next_a <= 0;
                                        next_v <= target_v;
                                    end
                                else if ((v < target_v && next_v_comb > target_v) || (v > target_v && next_v_comb < target_v))
                                    begin
                                        next_jj <= 0;
                                        next_j <= 0;
                                        next_v <= target_v;
                                        next_a <= 0;
                                    end
                            end
                    end
            end
    end

reg next_dir;
reg next_step;
reg signed [63:0] next_x;
wire signed [63:0] x_acc;
wire signed [24:0] v_effective;
wire signed [63:0] delta_x;

assign v_effective = v + step_start_v;
assign delta_x[23:0] = v_effective[24:1];
assign delta_x[63:24] = v_effective[24]?40'hFFFFFFFFFF:40'h0;

assign x_acc = x + delta_x;

always @(reset, load, set_x, x_val, x, v, dir, step_bit, stopped, x_acc, v_effective)
    begin
        next_x <= x;
        next_dir <= dir;
        next_step <= 0;
        next_stopped <= stopped;

        if (reset)
            begin
                next_x <= 0;
                next_dir <= 0;
            end
        else if (load && set_x)
            begin
                next_x <= x_val;
            end
        else
            begin
                next_x <= x_acc;
                if (x[step_bit] != x_acc[step_bit])
                    begin
                        if (v_effective > 0)
                            next_dir <= 1;
                        else
                            next_dir <= 0;
                        next_step <= 1;
                    end
                if (v_effective == 0)
                    begin
                        next_stopped <= 1;
                    end
                else
                    begin
                        next_stopped <= 0;
                    end
            end
    end

always @(posedge clk)
    begin
        x <= next_x;
        v <= next_v;
        a <= next_a;
        j <= next_j;
        jj <= next_jj;
        step <= next_step;
        dir <= next_dir;
        stopped <= next_stopped;
        target_v <= next_target_v;
        target_set <= next_target_set;
        step_start_x <= next_step_start_x;
        step_start_v <= next_step_start_v;
    end

endmodule
