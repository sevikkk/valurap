`timescale 1ns/100ps

`include "../src/dp_ram.v"
`include "../src/fifo.v"
`include "../src/buf_executor.v"

module buf_exec_tb;

reg clk;
reg reset;
reg [39:0] fifo_write_data;
reg fifo_write;

reg be_start;
reg be_abort;

reg [63:0] cycle;

reg assertions_failed = 0;

wire [31:0] fifo_data_count;
wire [39:0] fifo_read_data;
wire fifo_read;
wire fifo_empty;

reg [31:0] pending_ints;

assign fifo_data_count[31:5] = 0;

fifo #(.ADDRESS_WIDTH(4), .DATA_WIDTH(40)) fifo (
           .clk(clk),
           .reset(reset),
           .write_data(fifo_write_data),
           .read(fifo_read),
           .write(fifo_write),
           .empty(fifo_empty),
           .read_data(fifo_read_data),
           .data_count(fifo_data_count[4:0])
       );

buf_executor buf_exec(
       .clk(clk),
       .rst(reset),
    .ext_out_reg_busy(1'b0),
    .ext_pending_ints(pending_ints),
    .fifo_empty(fifo_empty),
    .fifo_data(fifo_read_data),
    .fifo_read(fifo_read),
    .fifo_global_count(fifo_data_count),
    .fifo_local_count(fifo_data_count),
    .start(be_start),
    .abort(be_abort)
);

integer idx;

initial
    begin
        $dumpfile("test.vcd");
        $dumpvars;

        for (idx = 0; idx < 16; idx = idx + 1) begin
            $dumpvars(0,fifo.ram.ram[idx]);
        end

        reset = 1;
        clk = 0;
        fifo_write_data = 0;
        fifo_write = 0;
        pending_ints = 0;
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
                fifo_write = 0;
                be_start = 0;
                be_abort = 0;
                #6;
                case (cycle)
                    13: begin
                        fifo_write_data = 40'h8000000000;
                        fifo_write = 1;
                    end
                    14: begin
                        fifo_write_data = 40'hBF00000000;
                        fifo_write = 1;
                    end
                    50: be_start = 1;
                    100: be_start = 1;
                    113: begin
                        fifo_write_data = 40'h8000000000;
                        fifo_write = 1;
                    end
                    200: begin
                        fifo_write_data = 40'h8000000000;
                        fifo_write = 1;
                    end
                    201: begin
                        fifo_write_data = 40'h4000000000;
                        fifo_write = 1;
                    end
                    202: begin
                        fifo_write_data = 40'h8300000001;
                        fifo_write = 1;
                    end
                    203: begin
                        fifo_write_data = 40'hBF00000000;
                        fifo_write = 1;
                    end
                    250: be_start = 1;
                    300: pending_ints = 1;
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

