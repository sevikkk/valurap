module endstop_mux
    (
        input [7:0] holds,
        input [7:0] stbs,

        input [2:0] mux_select,

        output hold,
        output stb
    );

    assign hold = holds[mux_select];
    assign stb = stbs[mux_select];

endmodule
