module motor_mux
(
    input clk,
    input [7:0] steps,
    input [7:0] dirs,
    input [7:0] holds,

    input [2:0] mux_select,
    input invert_dir,
    input mute,

    output step,
    output dir,
    output hold,
);

assign step = steps[mux_select] & mute;
assign hold = steps[mux_select] & mute;
assign dir = dirs[mux_select] ^ invert_dir;

endmodule
