`timescale 1ns/100ps

`include "../src/acc_step_gen.v"
`include "../src/profile_gen.v"
`include "../src/speed_integrator.v"

module pg_tb;

    reg clk;
    reg rst;
    reg acc_step;
    wire start_calc;
    reg [7:0] param_addr;
    reg [31:0] param_in;
    reg write_hi;
    reg write_lo;

    reg [63:0] cycle;

    reg [31:0] dt_val;
    reg [31:0] steps_val;

    reg assertions_failed = 0;

    wire gated_write_hi;
    wire gated_write_lo;
    wire [7:0] pending_aborts;
    wire [7:0] aborts;
    wire global_abort;
    wire calc_done;

    reg start = 0;
    reg abort = 0;
    reg asg_abort = 0;
    reg params_load_done = 0;

    wire [63:0] speed_0;
    wire [63:0] speed_1;
    wire [63:0] speed_2;
    wire load_speeds;


    acc_step_gen#(.MIN_LOAD_CYCLES(50)) asg(
        .clk(clk),
        .reset(rst),
        .dt_val(dt_val),
        .steps_val(steps_val),
        .start(start),
        .abort(asg_abort),
        .param_write_hi(write_hi),
        .param_write_lo(write_lo),
        .params_load_done(params_load_done),
        .gated_param_write_hi(gated_write_hi),
        .gated_param_write_lo(gated_write_lo),
        .pending_aborts(pending_aborts),
        .global_abort(global_abort),
        .start_calc(start_calc),
        .acc_calc_done(calc_done),
        .load_speeds(load_speeds)
    );

    assign aborts = {8{abort | global_abort}};


    profile_gen pg(
        .clk(clk),
        .rst(rst),
        .acc_step(acc_step | start_calc),
        .param_addr(param_addr),
        .param_in(param_in),
        .param_write_hi(gated_write_hi),
        .param_write_lo(gated_write_lo),
        .abort(aborts),
        .done(calc_done),
        .pending_aborts(pending_aborts),
        .speed_0(speed_0),
        .speed_1(speed_1),
        .speed_2(speed_2)
    );

    speed_integrator sp0(
        .clk(clk),
        .reset(rst),
        .set_v(load_speeds),
        .set_x(1'b0),
        .x_val(64'b0),
        .v_val(speed_0),
        .step_bit(6'd32)
    );

    speed_integrator sp1(
        .clk(clk),
        .reset(rst),
        .set_v(load_speeds),
        .set_x(1'b0),
        .x_val(64'b0),
        .v_val(speed_1),
        .step_bit(6'd32)
    );

    speed_integrator sp2(
        .clk(clk),
        .reset(rst),
        .set_v(load_speeds),
        .set_x(1'b0),
        .x_val(64'b0),
        .v_val(speed_2),
        .step_bit(6'd32)
    );

    localparam
        CH0=0,
        CH1=8'h20,
        CH2=8'h40,
        CH3=8'h60,
        CH4=8'h80,
        CH5=8'hA0,
        CH6=8'hC0,
        CH7=8'hE0;

`define assert_signal(name, signal, value) \
    begin if (signal != value) begin \
            $display("ASSERTION FAILED in %m at %0d: actual %s %h != expected %h", cycle, name, signal, value); \
            assertions_failed = 1; \
        end \
    end

    integer idx;

    initial
        begin
            $dumpfile("test.vcd");
            $dumpvars;

            for (idx = 0; idx < 9; idx = idx+1) begin
                $dumpvars(0, pg.mem0[idx]);
                $dumpvars(0, pg.mem1[idx]);
            end

            rst = 1;
            clk = 0;
            acc_step = 0;
            param_addr = 0;
            param_in = 0;
            write_hi = 0;
            write_lo = 0;
            abort = 0;
            dt_val = 0;
            steps_val = 0;
            #10;
            clk = 1;
            #10;
            clk = 0;
            #10;
            clk = 1;
            #10;
            clk = 0;
            #6;
            rst = 0;
            #4;
            clk = 1;
            #10;
            clk = 0;
            #10;
            clk = 1;
            #10;
            clk = 0;
            #10;
            clk = 1;
            #10;
            clk = 0;
            #10;
            clk = 1;
            #10;
            clk = 0;
            #10;
            clk = 1;
            #10;
            clk = 0;
            #10;
            cycle = 0;
            forever
                begin
                    clk = 1;
                    write_hi = 0;
                    write_lo = 0;
                    params_load_done = 0;
                    #6;
                    case (cycle)
                        10: begin
                            param_addr = CH0 | pg.R_STATUS;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        11: begin
                            param_addr = CH0 | pg.R_V_EFF;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        12: begin
                            param_addr = CH0 | pg.R_V_IN;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        13: begin
                            param_addr = CH0 | pg.R_V_OUT;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        14: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        15: begin
                            param_addr = CH0 | pg.R_J;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        16: begin
                            param_addr = CH0 | pg.R_JJ;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        17: begin
                            param_addr = CH0 | pg.R_TARGET_V;
                            param_addr = 7;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        18: begin
                            param_addr = CH0 | pg.R_ABORT_A;
                            param_addr = 8;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        30: begin
                            param_addr = CH1;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        31: begin
                            param_addr = CH2;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        32: begin
                            param_addr = CH3;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        33: begin
                            param_addr = CH4;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        34: begin
                            param_addr = CH5;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        35: begin
                            param_addr = CH6;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        36: begin
                            param_addr = CH7;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end

                        50: begin
                            param_addr = CH0 | pg.R_STATUS;
                            param_in = pg.STATUS_ENABLE_MASK | pg.STATUS_TARGET_V_MASK;
                            write_hi = 0;
                            write_lo = 1;
                        end
                        51: begin
                            param_addr = CH0 | pg.R_V_OUT;
                            param_in = -300;
                            write_hi = 0;
                            write_lo = 1;
                        end
                        52: begin
                            param_addr = CH0 | pg.R_V_OUT;
                            param_in = -1;
                            write_hi = 1;
                            write_lo = 0;
                        end
                        53: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = 70;
                            write_hi = 0;
                            write_lo = 1;
                        end
                        54: begin
                            param_addr = CH0 | pg.R_J;
                            param_in = 0;
                            write_hi = 0;
                            write_lo = 1;
                        end
                        55: begin
                            param_addr = CH0 | pg.R_JJ;
                            param_in = 0;
                            write_hi = 0;
                            write_lo = 1;
                        end
                        56: begin
                            param_addr = CH0 | pg.R_TARGET_V;
                            param_in = 40;
                            write_hi = 0;
                            write_lo = 1;
                        end
                        57: begin
                            param_addr = CH0 | pg.R_ABORT_A;
                            param_in = 17;
                            write_hi = 0;
                            write_lo = 1;
                        end
                        58: begin
                            param_addr = 0;
                            param_in = 0;
                            write_hi = 0;
                            write_lo = 0;
                        end
                        100: begin
                            acc_step = 1;
                        end
                        101: begin
                            acc_step = 0;
                        end

                        150: `assert_signal("Speed0", pg.speed_0, -265)

                        200: begin
                            acc_step = 1;
                        end
                        201: begin
                            acc_step = 0;
                        end
                        250: `assert_signal("Speed0", pg.speed_0, -195)
                        300: begin
                            acc_step = 1;
                        end
                        301: begin
                            acc_step = 0;
                        end
                        313: begin
                            abort = 1;
                        end
                        314: begin
                            abort = 0;
                        end
                        350: begin
                            `assert_signal("Speed0", pg.speed_0, -125)
                            `assert_signal("Abort0", pg.pending_aborts[0], 1)
                            `assert_signal("Abort0", pg.abort_in_progress[0], 0)
                        end
                        400: begin
                            acc_step = 1;
                        end
                        401: begin
                            acc_step = 0;
                        end
                        450: begin
                            `assert_signal("Speed0", pg.speed_0, -82)
                            `assert_signal("Abort0", pg.pending_aborts[0], 1)
                            `assert_signal("Abort0", pg.abort_in_progress[0], 1)
                        end
                        500: begin
                            acc_step = 1;
                        end
                        501: begin
                            acc_step = 0;
                        end
                        600: begin
                            acc_step = 1;
                        end
                        601: begin
                            acc_step = 0;
                        end
                        700: begin
                            acc_step = 1;
                        end
                        701: begin
                            acc_step = 0;
                        end
                        750: begin
                            abort = 1;
                        end
                        751: begin
                            abort = 0;
                        end
                        800: begin
                            acc_step = 1;
                        end
                        801: begin
                            acc_step = 0;
                        end
                        900: begin
                            acc_step = 1;
                        end
                        901: begin
                            acc_step = 0;
                        end
                        950: begin
                            `assert_signal("Speed0", pg.speed_0, -3)
                            `assert_signal("Abort0", pg.pending_aborts[0], 1)
                            `assert_signal("Abort0", pg.abort_in_progress[0], 1)
                        end
                        1000: begin
                            acc_step = 1;
                        end
                        1001: begin
                            acc_step = 0;
                        end
                        1050: begin
                            `assert_signal("Speed0", pg.speed_0, 0)
                            `assert_signal("Abort0", pg.pending_aborts[0], 0)
                            `assert_signal("Abort0", pg.abort_in_progress[0], 0)
                        end
                        1100: begin
                            acc_step = 1;
                        end
                        1101: begin
                            acc_step = 0;
                        end
                        1200: begin
                            acc_step = 1;
                        end
                        1201: begin
                            acc_step = 0;
                        end
                        1300: begin
                            acc_step = 1;
                        end
                        1301: begin
                            acc_step = 0;
                        end
                        1350: begin
                            `assert_signal("Speed0", pg.speed_0, 0)
                            `assert_signal("Abort0", pg.pending_aborts[0], 0)
                            `assert_signal("Abort0", pg.abort_in_progress[0], 0)
                        end
                        1400: begin
                            acc_step = 1;
                        end
                        1401: begin
                            acc_step = 0;
                        end
                        1500: begin
                            acc_step = 1;
                        end
                        1501: begin
                            acc_step = 0;
                        end
                        1600: begin
                            acc_step = 1;
                        end
                        1601: begin
                            acc_step = 0;
                        end
                        1700: begin
                            acc_step = 1;
                        end
                        1701: begin
                            acc_step = 0;
                        end
                        1800: begin
                            acc_step = 1;
                        end
                        1801: begin
                            acc_step = 0;
                        end
                        1990: begin
                            `assert_signal("Waiting for params", asg.waiting_for_params, 1)
                        end
                        2000: begin
                            dt_val = 200;
                            steps_val = 20;
                        end
                        2001: begin
                            start = 1;
                        end
                        2002: begin
                            start = 0;
                        end
                        2003: begin
                            `assert_signal("Not waiting for params", asg.waiting_for_params, 0)
                            `assert_signal("ASG Busy", asg.busy, 1)
                            `assert_signal("PG Busy", pg.busy, 1)
                        end
                        5838: begin
                            `assert_signal("Not waiting for params", asg.waiting_for_params, 0)
                            `assert_signal("Steps == 19", asg.steps, 19)
                        end
                        5839: begin
                            `assert_signal("Load_speeds", asg.load_speeds, 1)
                            `assert_signal("Not start calc", asg.start_calc, 0)
                        end
                        5840: begin
                            `assert_signal("Waiting for params", asg.waiting_for_params, 1)
                            `assert_signal("Not start calc", asg.start_calc, 0)
                        end
                        6200: begin
                            `assert_signal("Not waiting for params", asg.waiting_for_params, 0)
                            `assert_signal("Error late params", asg.error_late_params, 1)
                        end
                        6500: begin
                            `assert_signal("Waiting for params", asg.waiting_for_params, 1)
                            `assert_signal("ASG not Busy", asg.busy, 0)
                            `assert_signal("PG not Busy", pg.busy, 0)
                        end
                        6600: begin
                            start = 1;
                        end
                        6601: begin
                            start = 0;
                        end
                        6610: begin
                            `assert_signal("Not waiting for params", asg.waiting_for_params, 0)
                            `assert_signal("ASG Busy", asg.busy, 1)
                            `assert_signal("PG Busy", pg.busy, 1)
                        end
                        7701: begin
                            write_lo = 1;
                        end
                        7702: begin
                            write_lo = 0;
                        end
                        6200: begin
                            `assert_signal("Not waiting for params", asg.waiting_for_params, 0)
                            `assert_signal("Error late params", asg.error_unexpected_params_write, 1)
                        end
                        8100: begin
                            `assert_signal("Waiting for params", asg.waiting_for_params, 1)
                            `assert_signal("ASG not Busy", asg.busy, 0)
                            `assert_signal("PG not Busy", pg.busy, 0)
                            `assert_signal("Error late params", asg.error_unexpected_params_write, 1)
                        end

                        //*********************************
                        // 20 steps with A=5
                        //*********************************
                        8400: begin
                            param_addr = CH0 | pg.R_V_OUT;
                            param_in = 0;
                            write_hi = 1;
                            write_lo = 1;
                        end
                        8401: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = 0;
                            write_hi = 1;
                        end
                        8402: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = 5;
                            write_lo = 1;
                        end
                        8403: begin
                            param_addr = CH0 | pg.R_STATUS;
                            param_in = 1;
                            write_lo = 1;
                        end
                        8500: begin
                            start = 1;
                        end
                        8501: begin
                            start = 0;
                        end
                        8510: begin
                            `assert_signal("Not waiting for params", asg.waiting_for_params, 0)
                            `assert_signal("ASG Busy", asg.busy, 1)
                            `assert_signal("PG Busy", pg.busy, 1)
                        end

                        12000: `assert_signal("Speed", sp0.v, 87)
                        12200: `assert_signal("Speed", sp0.v, 92)

                        //*********************************
                        // 20 steps with A=0
                        //*********************************
                        12332: begin
                            `assert_signal("Not waiting for params", asg.waiting_for_params, 0)
                            `assert_signal("Steps == 19", asg.steps, 19)
                        end
                        12333: begin
                            `assert_signal("Load_speeds", asg.load_speeds, 1)
                            `assert_signal("Not start calc", asg.start_calc, 0)
                        end
                        12334: begin
                            `assert_signal("Waiting for params", asg.waiting_for_params, 1)
                            `assert_signal("Load_next params", asg.load_next_params, 1)
                            `assert_signal("Not start calc", asg.start_calc, 0)
                        end
                        12380: `assert_signal("Speed", sp0.v, 97)
                        12400: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = 0;
                            write_hi = 1;
                        end
                        12401: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = 0;
                            write_lo = 1;
                        end
                        12402: begin
                            param_addr = CH0 | pg.R_STATUS;
                            param_in = 1;
                            write_lo = 1;
                        end
                        12450: begin
                            params_load_done = 1;
                            `assert_signal("dt == 112", asg.dt, 117)
                        end
                        12451: begin
                            params_load_done = 0;
                            `assert_signal("Waiting for params", asg.waiting_for_params, 0)
                            `assert_signal("Start calc", asg.start_calc, 1)
                            `assert_signal("Steps == 0", asg.steps, 0)
                            `assert_signal("dt == 113", asg.dt, 118)
                        end

                        12600: `assert_signal("Speed", sp0.v, 100)
                        16000: `assert_signal("Speed", sp0.v, 100)
                        16200: `assert_signal("Speed", sp0.v, 100)
                        //*********************************
                        // 10 steps with A=30
                        //*********************************
                        16350: begin
                            steps_val = 10;
                        end
                        16351: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = 0;
                            write_hi = 1;
                        end
                        16352: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = 30;
                            write_lo = 1;
                        end
                        16353: begin
                            param_addr = CH0 | pg.R_STATUS;
                            param_in = 1;
                            write_lo = 1;
                        end

                        16401: begin
                            params_load_done = 1;
                        end

                        16600: `assert_signal("Speed", sp0.v, 115)
                        16800: `assert_signal("Speed", sp0.v, 145)
                        17000: `assert_signal("Speed", sp0.v, 175)
                        18200: `assert_signal("Speed", sp0.v, 355)
                        //*********************************
                        // 30 steps with A=-27 until 0
                        //*********************************
                        18350: begin
                            steps_val = 30;
                        end
                        18351: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = -1;
                            write_hi = 1;
                        end
                        18352: begin
                            param_addr = CH0 | pg.R_A;
                            param_in = -27;
                            write_lo = 1;
                        end
                        18353: begin
                            param_addr = CH0 | pg.R_TARGET_V;
                            param_in = 0;
                            write_lo = 1;
                        end
                        18354: begin
                            param_addr = CH0 | pg.R_STATUS;
                            param_in = 3;
                            write_lo = 1;
                        end

                        18400: begin
                            params_load_done = 1;
                        end

                        18450: `assert_signal("Speed", sp0.v, 385)
                        18650: `assert_signal("Speed", sp0.v, 386)
                        18850: `assert_signal("Speed", sp0.v, 359)
                        21200: `assert_signal("Speed", sp0.v, 35)
                        21400: `assert_signal("Speed", sp0.v, 11)
                        21600: `assert_signal("Speed", sp0.v, 0)
                        21601: `assert_signal("Speed", sp0.x, 1689600)

                        //*********************************
                        // Done
                        //*********************************
                        24400: begin
                            steps_val = 0;
                        end
                        24401: begin
                            params_load_done = 1;
                        end


                        //*********************************
                        // Final check
                        //*********************************
                        29000: begin
                            `assert_signal("Waiting for params", asg.waiting_for_params, 1)
                            `assert_signal("Steps == 0", asg.steps, 0)
                            `assert_signal("ASG Busy", asg.busy, 0)
                            `assert_signal("Error unexpected params", asg.error_unexpected_params_write, 0)
                            `assert_signal("Error late params", asg.error_late_params, 0)
                        end
                        30000:
                            begin
                                if (assertions_failed)
                                    begin
                                        $display("ERROR: Some assertions failed");
                                    end
                                else
                                    begin
                                        $display("All passed");
                                    end

                                $display("Done");
                                $finish();
                            end
                    endcase

                    #4;
                    clk = 0;
                    #10;
                    cycle = cycle+1;
                    // $display(cycle);
                end
        end

endmodule
