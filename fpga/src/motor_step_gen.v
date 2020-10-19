module motor_step_gen(
    input clk,
    input reset,
    input [31:0] pre_n,
    input [31:0] pulse_n,
    input [31:0] post_n,
    input step_stb,
    input step_dir,
    output reg step,
    output reg dir,
    output reg missed

    input set_x,
    input signed [31:0] x_val,
    output signed [31:0] x,

    input hold,
    output signed [31:0] x_hold
    );
	 
reg [15:0] cnt;
reg [15:0] next_cnt;
reg signed [31:0] next_x;
reg signed [31:0] next_x_hold;
reg next_dir;
reg next_step;
reg next_missed;

always @(*)
	begin
		next_cnt <= 0;
		next_dir <= dir;
		next_step <= 0;
		next_missed <= 0;
		next_x <= x;
		next_x_hold <= x_hold;

		if (reset)
			begin
				next_dir <= 0;
                                next_x <= 0;
                                next_x_hold <= 0;
			end
		else if (cnt == 0)
			begin
				if (step_stb)
					begin
						next_dir <= step_dir;
						next_cnt <= 1;
                                                if (step_dir)
                                                    next_x <= x - 1;
                                                else
                                                    next_x <= x + 1;
					end
			end
		else
			begin
				if (step_stb)
					next_missed <= 1;
				next_cnt <= cnt + 1;
				if (cnt < pre_n[15:0])
					next_step <= 0;
				else if (cnt < pulse_n[15:0])
					next_step <= 1;
				else if (cnt < post_n[15:0])
					next_step <= 0;
				else
					next_cnt <= 0;
			end

                if (!reset & hold)
                    next_x_hold <= x;
	end
	
always @(posedge clk)
	begin
		cnt <= next_cnt;
		dir <= next_dir;
		step <= next_step;
		missed <= next_missed;
		x <= next_x;
		x_hold <= next_x_hold;
	end

endmodule
