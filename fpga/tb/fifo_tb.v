`timescale 1ns/100ps

`include "../src/dp_ram.v"
`include "../src/fifo.v"

module fifo_tb;

reg clk;
reg reset;
reg [7:0] write_data;
reg read;
reg write;

reg [63:0] cycle;

reg assertions_failed = 0;

fifo #(.ADDRESS_WIDTH(4), .DATA_WIDTH(8)) dut (
           .clk(clk),
           .reset(reset),
           .write_data(write_data),
           .read(read),
           .write(write)
       );

integer idx;

initial
    begin
        $dumpfile("test.vcd");
        $dumpvars;

        for (idx = 0; idx < 16; idx = idx + 1) begin
            $dumpvars(0,dut.ram.ram[idx]);
        end

        reset = 1;
        clk = 0;
        write_data = 0;
        read = 0;
        write = 0;
        #10;
        clk = 1;
        #10;
        clk = 0;
        #10;
        clk = 1;
        #10;
        clk = 0;
        #6;
        reset = 0;
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
                read = 0;
                write = 0;
                #6;
                case (cycle)
                    10: begin
                        read = 1;
                    end
                    12: begin
                        read = 1;
                    end
                    13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38: begin
                        write_data = cycle - 12;
                        write = 1;
                    end
                    50,51,52,53,55,56,57,58,60,61,62,63,65,66,67,68,69: begin
                        read = 1;
                    end
                    80,81,82,83,84: begin
                        write_data = cycle - 79;
                        write = 1;
                    end
                    90,92,93: begin
                        write_data = cycle - 89;
                        read = 1;
                        write = 1;
                    end
                    100,101,102,103,104,105,106,107,108: begin
                        read = 1;
                    end
                    110,111,112,113: begin
                        write_data = cycle - 100;
                        read = 1;
                        write = 1;
                    end
                    2000:
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
