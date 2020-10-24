module dds_uart_clock(
    input clk,
    input [15:0] baudrate,
    output reg enable_16
);

    parameter TOP=31250;


    reg [15:0] accum = 0;

    always @(posedge clk)
        begin
            if (accum >= TOP)
                begin
                    accum <= accum+baudrate-TOP;
                    enable_16 <= 1;
                end
            else
                begin
                    accum <= accum+baudrate;
                    enable_16 <= 0;
                end
        end

endmodule
