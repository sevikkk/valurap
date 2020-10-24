module endstop_mux
    (
        input [7:0] signals,
        input [7:0] holds,
        input [7:0] stbs,

        input [2:0] mux_select,
        input invert,
        input mute,

        output signal,
        output hold,
        output stb
    );

    assign signal = signals[mux_select] ^ invert;
    assign hold = holds[mux_select] & mute;
    assign stb = stbs[mux_select] & mute;

endmodule
