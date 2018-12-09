module buf_cmds();

function [39:0] BUF_CMD;
    input [1:0] prefix;
    input [5:0] cmd;
    input [31:0] data;

    begin
        BUF_CMD = { data[7:0], data[15:8], data[23:16], data[31:24], prefix, cmd};
    end
endfunction

function [39:0] OUTPUT;
    input [5:0] reg_num;
    input [31:0] data;

    begin
        OUTPUT = BUF_CMD(1, reg_num, data);
    end
endfunction

function [39:0] DONE;
    input [31:0] data;
    begin
        DONE = BUF_CMD(2, 63, data);
    end
endfunction

function [39:0] STB;
    input [31:0] data;
    begin
        STB = BUF_CMD(2, 1, data);
    end
endfunction

function [39:0] WAIT_ALL;
    input [31:0] data;
    begin
        WAIT_ALL = BUF_CMD(2, 2, data);
    end
endfunction

function [39:0] WAIT_ANY;
    input [31:0] data;
    begin
        WAIT_ANY = BUF_CMD(2, 3, data);
    end
endfunction

function [39:0] CLEAR;
    input [31:0] data;
    begin
        CLEAR = BUF_CMD(2, 4, data);
    end
endfunction

function [63:0] S3G_WRITE_BUFFER_HDR;
    input [15:0] offset;
    input [7:0] len;
    reg [7:0] cmd_len;
    begin
        cmd_len = 6 + len * 5;
        S3G_WRITE_BUFFER_HDR = {
            8'hD5, cmd_len, 16'h7654,
            8'd65, len, offset[7:0], offset[15:8]
        };
    end
endfunction

function [79:0] S3G_OUTPUT_T(
    input [7:0] reg_num,
    input [31:0] data,
    input [15:0] tag
  );
    begin
        S3G_OUTPUT_T = {
            8'hD5, 8'd8, tag,
            8'd60, reg_num, data[7:0], data[15:8], data[23:16], data[31:24]
        };
    end
endfunction

function [79:0] S3G_OUTPUT(
    input [7:0] reg_num,
    input [31:0] data
  );
    begin
        S3G_OUTPUT = S3G_OUTPUT_T(reg_num, data, 16'h7654);
    end
endfunction

function [47:0] S3G_INPUT;
    input [7:0] reg_num;
    begin
        S3G_INPUT = {
            8'hD5, 8'd4, 16'h7654,
            8'd61, reg_num
        };
    end
endfunction

function [71:0] S3G_STB;
    input [31:0] data;
    begin
        S3G_STB = {
            8'hD5, 8'd7, 16'h7654,
            8'd62, data[7:0], data[15:8], data[23:16], data[31:24]
        };
    end
endfunction

function [71:0] S3G_CLEAR;
    input [31:0] data;
    begin
        S3G_CLEAR = {
            8'hD5, 8'd7, 16'h7654,
            8'd63, data[7:0], data[15:8], data[23:16], data[31:24]
        };
    end
endfunction

function [71:0] S3G_MASK;
    input [31:0] data;
    begin
        S3G_MASK = {
            8'hD5, 8'd7, 16'h7654,
            8'd64, data[7:0], data[15:8], data[23:16], data[31:24]
        };
    end
endfunction

endmodule

