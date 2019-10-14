module endstop_with_mux
(
    input clk,
    input reset,

    input signal_in,
    input abort_in,

    input unlock,

    input [1:0] mux_select,
    input abort_polarity,
    input abort_enabled,
    input [31:0] timeout,

    output [7:0] cycles,
    output signal,
    output signal_changed,
    
    output reg abort_out
);

always @(signal, abort_polarity, abort_enabled, abort_in)
    begin
        abort_out <= abort_in;
        if (abort_enabled && (signal == abort_polarity))
            abort_out <= 1'b1;
    end

debounce debounce(
    .clk(clk),
    .reset(reset),
    .sig_in(signal_in),
    .unlock(unlock),
    .timeout(timeout),
    .sig_out(signal),
    .sig_changed(signal_changed),
    .cycles(cycles)
);

endmodule

