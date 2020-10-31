`timescale 1ns/100ps

`include "../src/profile_gen.v"

module pg_tb;

    reg clk;
    reg rst;
    reg acc_step;
    reg [7:0] param_addr;
    reg [7:0] abort;
    reg [31:0] param_in;
    reg write_hi;
    reg write_lo;

    reg [63:0] cycle;

    reg assertions_failed = 0;


    profile_gen pg(
        .clk(clk),
        .rst(rst),
        .acc_step(acc_step),
        .param_addr(param_addr),
        .param_in(param_in),
        .param_write_hi(write_hi),
        .param_write_lo(write_lo),
        .abort(abort)
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
                        2000:
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
