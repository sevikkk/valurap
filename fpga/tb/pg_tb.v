`timescale 1ns/100ps

`include "../src/profile_gen.v"

module pg_tb;

reg clk;
reg rst;
reg acc_step;
reg [7:0] param_addr;
reg [31:0] param_in;
reg write_hi;
reg write_lo;

reg [63:0] cycle;

reg assertions_failed = 0;

profile_gen dut (
           .clk(clk),
           .rst(rst),
           .acc_step(acc_step),
           .param_addr(param_addr),
           .param_in(param_in),
           .param_write_hi(write_hi),
           .param_write_lo(write_lo)
       );

integer idx;

initial
    begin
        $dumpfile("test.vcd");
        $dumpvars;

        for (idx = 0; idx < 9; idx = idx + 1) begin
            $dumpvars(0,dut.mem0[idx]);
            $dumpvars(0,dut.mem1[idx]);
        end

        rst = 1;
        clk = 0;
        acc_step = 0;
        param_addr = 0;
        param_in = 0;
        write_hi = 0;
        write_lo = 0;
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
                        param_addr = 0;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    11: begin
                        param_addr = 1;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    12: begin
                        param_addr = 2;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    13: begin
                        param_addr = 3;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    14: begin
                        param_addr = 4;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    15: begin
                        param_addr = 5;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    16: begin
                        param_addr = 6;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    17: begin
                        param_addr = 7;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    18: begin
                        param_addr = 8'h20;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    19: begin
                        param_addr = 8'h40;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    20: begin
                        param_addr = 8'h60;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    21: begin
                        param_addr = 8'h80;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    22: begin
                        param_addr = 8'hA0;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    23: begin
                        param_addr = 8'hC0;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end
                    24: begin
                        param_addr = 8'hE0;
                        param_in = 0;
                        write_hi = 1;
                        write_lo = 1;
                    end

                    25: begin
                        param_addr = 0;
                        param_in = 3;
                        write_hi = 0;
                        write_lo = 1;
                    end
                    26: begin
                        param_addr = 3;
                        param_in = -300;
                        write_hi = 0;
                        write_lo = 1;
                    end
                    27: begin
                        param_addr = 3;
                        param_in = -1;
                        write_hi = 1;
                        write_lo = 0;
                    end
                    28: begin
                        param_addr = 4;
                        param_in = 70;
                        write_hi = 0;
                        write_lo = 1;
                    end
                    29: begin
                        param_addr = 5;
                        param_in = 0;
                        write_hi = 0;
                        write_lo = 1;
                    end
                    30: begin
                        param_addr = 6;
                        param_in = 0;
                        write_hi = 0;
                        write_lo = 1;
                    end
                    31: begin
                        param_addr = 7;
                        param_in = 40;
                        write_hi = 0;
                        write_lo = 1;
                    end
                    32: begin
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
                    200: begin
                        acc_step = 1;
                    end
                    201: begin
                        acc_step = 0;
                    end
                    300: begin
                        acc_step = 1;
                    end
                    301: begin
                        acc_step = 0;
                    end
                    400: begin
                        acc_step = 1;
                    end
                    401: begin
                        acc_step = 0;
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
                    1000: begin
                        acc_step = 1;
                    end
                    1001: begin
                        acc_step = 0;
                    end
                    1500:
                        begin
                            $display("Done");
                            $finish();
                        end
                    endcase

                #4;
                clk = 0;
                #10;
                cycle = cycle + 1;
                // $display(cycle);
            end
    end

endmodule
