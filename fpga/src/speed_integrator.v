module speed_integrator#(
    SPEED_BITS=64
) (
    input clk,
    input reset,
    input set_v,
    input set_x,
    input signed [SPEED_BITS-1:0] x_val,
    input signed [SPEED_BITS-1:0] v_val,
    input [5:0] step_bit,

    output reg signed [SPEED_BITS-1:0] x,
    output reg signed [SPEED_BITS-1:0] v,

    output reg step,
    output reg dir
);

    reg next_dir;
    reg next_step;
    reg signed [SPEED_BITS-1:0] next_x;
    reg signed [SPEED_BITS-1:0] next_v;

    wire signed [SPEED_BITS-1:0] x_acc;

    assign x_acc = x+v;

    always @(*)
        begin
            next_x <= x;
            next_v <= v;
            next_dir <= dir;
            next_step <= 0;

            if (reset)
                begin
                    next_x <= 0;
                    next_v <= 0;
                    next_dir <= 0;
                end
            else begin
                if (set_v)
                    next_v <= v_val;

                if (set_x) begin
                    next_x <= x_val;
                end
                else begin
                    next_x <= x_acc;
                    if (x[step_bit] != x_acc[step_bit])
                        begin
                            if (v > 0)
                                next_dir <= 0;
                            else
                                next_dir <= 1;
                            next_step <= 1;
                        end
                end
            end
        end

    always @(posedge clk)
        begin
            x <= next_x;
            v <= next_v;
            step <= next_step;
            dir <= next_dir;
        end

endmodule
