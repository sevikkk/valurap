module debounce(
    input clk,
    input reset,
    input signal_in,
    input unlock,
    input [31:0] timeout,
    output reg signal,
    output reg hold,
    output reg stb,
    output reg [7:0] cycles
);

    reg sig_reg1;
    reg sig;

// sync to clock
    always @(posedge clk)
        begin
            sig_reg1 <= signal_in;
            sig <= sig_reg1;
        end

    localparam
        S_STABLE=0,
        S_BOUNCE1=1,
        S_BOUNCE2=2;

    reg [15:0] timer;
    reg [15:0] next_timer;
    reg [2:0] state;
    reg [2:0] next_state;

    reg next_signal;
    reg next_hold;
    reg next_stb;

    always @(*)
        begin
            next_timer <= timer;
            next_state <= state;
            next_signal <= signal;
            next_hold <= 0;
            next_stb <= 0;

            if (reset)
                begin
                    next_timer <= 0;
                    next_state <= S_STABLE;
                    next_signal <= 0;
                end
            else
                begin
                    case (state)
                        S_STABLE:
                            begin
                                if (sig != signal)
                                    begin
                                        next_timer <= 0;
                                        next_state <= S_BOUNCE1;
                                        next_hold <= 1;
                                    end
                            end
                        S_BOUNCE1:
                            begin
                                if (sig != signal)
                                    begin
                                        next_timer <= timer+1;
                                        if (timer > timeout[15:0])
                                            begin
                                                next_signal <= sig;
                                                next_state <= S_STABLE;
                                                next_stb <= 1;
                                            end
                                    end
                                else
                                    begin
                                        next_state <= S_BOUNCE2;
                                        next_timer <= 0;
                                    end
                            end
                        S_BOUNCE2:
                            begin
                                if (sig == signal)
                                    begin
                                        next_timer <= timer+1;
                                        if (timer > timeout[15:0])
                                            begin
                                                next_state <= S_STABLE;
                                            end
                                    end
                                else
                                    begin
                                        next_state <= S_BOUNCE1;
                                        next_timer <= 0;
                                    end
                            end
                    endcase
                end
        end

    always @(posedge clk)
        begin
            timer <= next_timer;
            state <= next_state;
            signal <= next_signal;
            stb <= next_stb;
            hold <= next_hold;
        end

endmodule
