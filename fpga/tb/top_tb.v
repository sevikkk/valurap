`timescale 1ns/100ps

`include "../src/mojo_top.v"
`include "../src/cclk_detector.v"

module top_tb;

reg clk;
reg rst_n;
reg cclk;
wire avr_tx;
wire avr_rx;

reg [63:0] cycle;

reg assertions_failed = 0;

mojo_top #(
    ) dut (
           .clk(clk),
           .rst_n(rst_n),
           .cclk(cclk),
           .avr_tx(avr_tx),
           .avr_rx(avr_rx)
       );

initial
    begin
        $dumpfile("test.vcd");
        $dumpvars;

        rst_n = 0;
        cclk = 0;
        clk = 0;
        #10;
        clk = 1;
        #10;
        clk = 0;
        #10;
        clk = 1;
        #10;
        clk = 0;
        #6;
        rst_n = 1;
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
        #6;
        cclk = 1;
        #4;
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
