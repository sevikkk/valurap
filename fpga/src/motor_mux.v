module motor_mux
(
    input clk,
    input step_x,
    input step_y,
    input step_z,

    input dir_x,
    input dir_y,
    input dir_z,

    input [1:0] mux_select,
    input invert_dir,

    output reg step,
    output reg dir
);

always @(posedge clk)
    begin
        case (mux_select)
        2'h0:
            begin
                step <= 0;
                dir <= invert_dir;
            end
        2'h1:
            begin
                step <= step_x;
                dir <= dir_x ^ invert_dir;
            end
        2'h2:
            begin
                step <= step_y;
                dir <= dir_y ^ invert_dir;
            end
        2'h3:
            begin
                step <= step_z;
                dir <= dir_z ^ invert_dir;
            end
        endcase
    end

endmodule

