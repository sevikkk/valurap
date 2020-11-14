module motor_mux
    (
        input [7:0] steps,
        input [7:0] dirs,

        input [2:0] mux_select,
        input enable_step,
        input invert_dir,

        input [7:0] in_aborts,
        input enable_es_abort,
        input es_abort,
        output reg [7:0] out_aborts,

        output step,
        output dir
    );

    assign step = steps[mux_select] & enable_step;
    assign dir = dirs[mux_select] ^ invert_dir;

    always @(*) begin
        out_aborts <= in_aborts;
        if (es_abort & enable_es_abort)
            out_aborts[mux_select] <= 1'b1;
    end

endmodule
