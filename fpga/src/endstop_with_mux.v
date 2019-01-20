module endstop_with_mux
(
    input clk,
    input reset,

    input [63:0] x,
    input [63:0] y,
    input [63:0] z,

    input signal_in,
    input abort_in,

    input unlock,

    input [1:0] mux_select,
    input abort_polarity,
    input abort_enabled,
    input [31:0] timeout,

    output [63:0] pos_out,
    output [31:0] max_bounce,
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

reg [63:0] pos_in;

always @(mux_select, x, y, z)
    begin
        case (mux_select)
            2'h0: pos_in <= 0;
            2'h1: pos_in <= x;
            2'h2: pos_in <= y;
            2'h3: pos_in <= z;
        endcase
    end

debounce debounce(
    .clk(clk),
    .reset(reset),
    .sig_in(signal_in),
    .unlock(unlock),
    .pos_in(pos_in),
    .timeout(timeout),
    .sig_out(signal),
    .sig_changed(signal_changed),
    .pos_out(pos_out),
    .max_bounce(max_bounce),
    .cycles(cycles)
);

endmodule

