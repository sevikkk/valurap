module acc_step_gen
    #(parameter
    MIN_LOAD_CYCLES=100
    )
    (
        input clk,
        input reset,
        input [31:0] dt_val,        // Step interval
        input [31:0] steps_val,     // Number of steps in current sequence

        input start,                // from buf_exec
        input abort,                // from buf_exec

        input param_write_lo,       // from buf_exec
        input param_write_hi,       // from buf_exec
        input params_load_done,       // from buf_exec
        output reg load_next_params,  // to buf_exec
        output reg waiting_for_params,
        output gated_param_write_lo,  // to_
        output gated_param_write_hi,  // from buf_exec

        input [7:0] pending_aborts,   // ..
        output reg global_abort,
        output reg error_unexpected_params_write,
        output reg error_late_params,
        output reg error_abort_requested,

        output reg start_calc,        // to profile_gen
        input acc_calc_done,          // from profile_gen

        output reg load_speeds,       // to speed_integrators
        output reg done,
        output reg busy,

        /* debug */
        output reg [31:0] steps,
        output reg [31:0] dt
    );

    localparam S_INIT=0,
               S_ABORTING=1,
               S_ABORTING_WAIT_FIRST_CALC=2,
               S_ABORTING_CALC=3,
               S_ABORTING_WAIT_CALC=4,
               S_ABORTING_WAIT=5,
               S_WAIT_FIRST_CALC=6,
               S_CALC=7,
               S_WAIT_CALC=8,
               S_WAIT_FOR_LOAD=9,
               S_WAIT=10,
               S_WAIT_LAST=11;

    reg [31:0] next_dt;
    reg [31:0] next_steps;

    reg [31:0] steps_limit;
    reg [31:0] next_steps_limit;
    reg [31:0] dt_limit;
    reg [31:0] next_dt_limit;

    reg [2:0] state = S_INIT;
    reg [2:0] next_state;

    reg next_waiting_for_params;

    reg global_abort_in_progress;
    reg next_global_abort_in_progress;

    reg next_global_abort;
    reg next_load_next_params;
    reg next_start_calc;
    reg next_load_speeds;
    reg next_done;
    reg next_busy;
    reg next_error_unexpected_params_write;
    reg next_error_late_params;
    reg next_error_abort_requested;

    assign gated_param_write_hi = param_write_hi & waiting_for_params;
    assign gated_param_write_lo = param_write_lo & waiting_for_params;

    always @(*)
        begin
            next_state <= state;
            next_dt <= dt+1;
            next_steps <= steps;
            next_steps_limit <= steps_limit;
            next_dt_limit <= dt_limit;

            next_busy <= busy;
            next_waiting_for_params <= waiting_for_params;
            next_error_unexpected_params_write <= error_unexpected_params_write;
            next_error_late_params <= error_late_params;
            next_error_abort_requested <= error_abort_requested;
            next_global_abort_in_progress <= global_abort_in_progress;

            next_global_abort <= 0;
            next_load_next_params <= 0;
            next_start_calc <= 0;
            next_load_speeds <= 0;
            next_done <= 0;

            if (reset)
                begin
                    next_state <= S_INIT;
                    next_dt <= 0;
                    next_steps <= 0;
                    next_steps_limit <= 0;
                    next_dt_limit <= 0;
                    next_busy <= 0;
                    next_waiting_for_params <= 1;

                    next_error_unexpected_params_write <= 0;
                    next_error_late_params <= 0;
                    next_error_abort_requested <= 0;
                    next_global_abort_in_progress <= 0;
                end
            else if (
                (!waiting_for_params && !global_abort_in_progress && (
                    param_write_lo || param_write_hi || params_load_done
                    ))
                    || abort)
                begin
                    next_state <= S_ABORTING;
                    if (abort)
                        next_error_unexpected_params_write <= 1;
                    else
                        next_error_abort_requested <= 1;
                    next_global_abort_in_progress <= 1;
                    next_global_abort <= 1;
                    next_dt <= 0;
                    next_steps <= 0;
                    next_busy <= 1;
                end
            else case (state)
                S_INIT:
                    begin
                        if (start)
                            begin
                                next_waiting_for_params <= 0;
                                next_error_unexpected_params_write <= 0;
                                next_error_late_params <= 0;
                                next_error_abort_requested <= 0;
                                next_dt <= 0;
                                next_steps <= 0;
                                next_dt_limit <= dt_limit;
                                next_steps_limit <= steps_limit;
                                next_start_calc <= 1;
                                next_busy <= 1;
                                next_state <= S_WAIT_FIRST_CALC;
                            end
                    end
                S_ABORTING:
                    begin
                        next_start_calc <= 1;
                        next_state <= S_ABORTING_WAIT_FIRST_CALC;
                    end
                S_ABORTING_WAIT_FIRST_CALC:
                    begin
                        if (acc_calc_done)
                            begin
                                next_load_speeds <= 1;
                                next_dt <= 0;
                                next_state <= S_ABORTING_CALC;
                            end
                    end
                S_ABORTING_CALC: begin
                    next_start_calc <= 1;
                    next_state <= S_ABORTING_WAIT_CALC;
                end
                S_ABORTING_WAIT_CALC:
                    begin
                        if (acc_calc_done)
                            begin
                                next_state <= S_ABORTING_WAIT;
                            end
                    end
                S_ABORTING_WAIT:
                    begin
                        if (dt+1 >= dt_limit)
                            begin
                                next_dt <= 0;
                                next_load_speeds <= 1;
                                if (pending_aborts == 8'h0) begin
                                    next_state <= S_INIT;
                                    next_dt_limit <= 0;
                                    next_steps_limit <= 0;
                                    next_global_abort_in_progress <= 0;
                                    next_waiting_for_params <= 1;
                                    next_busy <= 0;
                                    next_done <= 1;
                                end
                                else
                                    next_state <= S_ABORTING_CALC;
                            end
                    end
                S_WAIT_FIRST_CALC:
                    begin
                        if (acc_calc_done)
                            begin
                                next_load_speeds <= 1;
                                next_dt <= 0;
                                next_state <= S_CALC;
                            end
                    end
                S_CALC: begin
                    next_waiting_for_params <= 0;
                    next_start_calc <= 1;
                    next_state <= S_WAIT_CALC;
                end
                S_WAIT_CALC:
                    begin
                        if (acc_calc_done)
                            begin
                                if (steps+1 >= steps_limit)
                                    begin
                                        next_waiting_for_params <= 1;
                                        next_load_next_params <= 1;
                                        next_state <= S_WAIT_FOR_LOAD;
                                    end
                                else
                                    next_state <= S_WAIT;
                            end
                    end
                S_WAIT:
                    begin
                        if (dt+1 >= dt_limit)
                            begin
                                next_dt <= 0;
                                next_steps <= steps+1;
                                next_load_speeds <= 1;
                                next_state <= S_CALC;
                            end
                    end
                S_WAIT_FOR_LOAD:
                    begin
                        if (params_load_done)
                            begin
                                if (dt_val == 0) begin
                                    next_state <= S_WAIT_LAST;
                                end
                                else begin
                                    next_steps_limit <= steps_val;
                                    next_steps <= 0;
                                    next_waiting_for_params <= 0;
                                    next_start_calc <= 1;
                                    next_state <= S_WAIT_CALC;
                                end
                            end
                        else if (dt+MIN_LOAD_CYCLES >= dt_limit)
                            begin
                                next_state <= S_ABORTING;
                                next_error_late_params <= 1;
                                next_global_abort_in_progress <= 1;
                                next_global_abort <= 1;
                                next_dt <= 0;
                                next_steps <= 0;
                            end
                    end
                S_WAIT_LAST:
                    begin
                        if (dt+1 >= dt_limit)
                            begin
                                next_load_speeds <= 1;
                                next_state <= S_INIT;
                                next_dt_limit <= 0;
                                next_steps_limit <= 0;
                                next_waiting_for_params <= 1;
                                next_busy <= 0;
                                next_done <= 1;
                            end
                    end

            endcase
        end

    always @(posedge clk)
        begin
            dt <= next_dt;
            dt_limit <= next_dt_limit;
            steps <= next_steps;
            steps_limit <= next_steps_limit;
            state <= next_state;

            busy <= next_busy;
            waiting_for_params <= next_waiting_for_params;
            error_unexpected_params_write <= next_error_unexpected_params_write;
            error_late_params <= next_error_late_params;
            error_abort_requested <= next_error_abort_requested;
            global_abort_in_progress <= next_global_abort_in_progress;

            global_abort <= next_global_abort;
            load_next_params <= next_load_next_params;
            start_calc <= next_start_calc;
            load_speeds <= next_load_speeds;
            done <= next_done;
        end

endmodule
