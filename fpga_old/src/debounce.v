module debounce(
    input clk,
    input reset,
    input sig_in,
    input unlock,
    input [31:0] timeout,
    output reg sig_out,
    output reg sig_changed,
    output reg [7:0] cycles
);

reg sig_reg1;
reg sig;

// sync to clock
always @(posedge clk)
	begin
		sig_reg1 <= sig_in;
		sig <= sig_reg1;
	end

localparam
    DSTATE_STABLE = 0,
    DSTATE_BOUNCE1 = 1,
    DSTATE_BOUNCE2 = 2;

reg [15:0] timer;
reg [2:0] dstate;
reg value;
reg value_changed;

reg [15:0] next_timer;
reg [2:0] next_dstate;
reg next_value;
reg next_value_changed;

always @(reset or timeout or sig or timer or dstate or value or unlock)
	begin
		next_timer <= timer;
		next_dstate <= dstate;
		next_value <= value;
		next_value_changed <= 0;
		
		if (reset)
			begin
				next_timer <= 0;
				next_dstate <= DSTATE_STABLE;
				next_value <= 0;
			end
		else
			begin
				case (dstate)
				DSTATE_STABLE:
					begin
						if (sig != value)
							begin
								next_timer <= 0;
								next_dstate <= DSTATE_BOUNCE1;
							end
					end
				DSTATE_BOUNCE1:
					begin
						if (sig != value)
							begin
								next_timer <= timer + 1;
								if (timer > timeout[15:0])
									begin
										next_value <= sig;
										next_dstate <= DSTATE_STABLE;
										next_value_changed <= 1;
									end
							end
						else
							begin
								next_dstate <= DSTATE_BOUNCE2;
								next_timer <= 0;
							end
					end
				DSTATE_BOUNCE2:
					begin
						if (sig == value)
							begin
								next_timer <= timer + 1;
								if (timer > timeout[15:0])
									begin
										next_dstate <= DSTATE_STABLE;
									end
							end
						else
							begin
								next_dstate <= DSTATE_BOUNCE1;
								next_timer <= 0;
							end
					end
				endcase
			end
	end
	
always @(posedge clk)
	begin
		timer <= next_timer;
		dstate <= next_dstate;
		value <= next_value;
		value_changed <= next_value_changed;
	end
	
localparam
    STATE_UNLOCKED = 0,
    STATE_LOCKED = 1;

reg [1:0] state;

reg [1:0] next_state;
reg [31:0] next_pos_out;
reg [7:0] next_cycles;
reg next_sig_out;
reg next_sig_changed;

always @(reset or unlock or value or value_changed or state or cycles or sig_out or sig_changed)
	begin
		next_state <= state;
		next_cycles <= cycles;
		next_sig_out <= sig_out;
		next_sig_changed <= sig_changed;
		
		if (reset)
			begin
				next_state <= STATE_UNLOCKED;
				next_cycles <= 0;
				next_sig_out <= 0;
				next_sig_changed <= 0;
			end
		else
			begin
				case (state)
					STATE_UNLOCKED:
						begin
							if (value_changed)
								begin
									next_state <= STATE_LOCKED;
									next_cycles <= cycles + 1;
									next_sig_out <= value;
									next_sig_changed <= 1;
								end
						end
					STATE_LOCKED:
						begin
							if (unlock)
								begin
									next_state <= STATE_UNLOCKED;
									next_sig_changed <= 0;
									next_sig_out <= value;
								end
							else if (value_changed)
								begin
									next_cycles <= cycles + 1;
								end
						end
				endcase
			end
	end

always @(posedge clk)
	begin
		state <= next_state;
		cycles <= next_cycles;
		sig_out <= next_sig_out;
		sig_changed <= next_sig_changed;
	end

endmodule
