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

endmodule

