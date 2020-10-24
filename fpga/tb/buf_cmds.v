module buf_cmds();

    function [39:0] BUF_CMD;
        input [1:0] prefix;
        input [5:0] cmd;
        input [31:0] data;

        begin
            BUF_CMD = {data[7:0], data[15:8], data[23:16], data[31:24], prefix, cmd};
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
            cmd_len = 6+len*5;
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

    localparam
        LEDS=0,
        ASG_STEPS_VAL=1,
        ASG_DT_VAL=2,
        ASG_CONTROL=3,
        ASG_CONTROL_SET_STEPS_LIMIT=32'h00000001,
        ASG_CONTROL_SET_DT_LIMIT=32'h00000002,
        ASG_CONTROL_RESET_STEPS=32'h00000004,
        ASG_CONTROL_RESET_DT=32'h00000008,
        ASG_CONTROL_APG_X_SET_X=32'h00000100,
        ASG_CONTROL_APG_X_SET_V=32'h00000200,
        ASG_CONTROL_APG_X_SET_A=32'h00000400,
        ASG_CONTROL_APG_X_SET_J=32'h00000800,
        ASG_CONTROL_APG_X_SET_JJ=32'h00001000,
        ASG_CONTROL_APG_X_SET_TARGET_V=32'h00002000,
        MSG_ALL_PRE_N=4,
        MSG_ALL_PULSE_N=5,
        MSG_ALL_POST_N=6,
        MSG_CONTROL=7,
        MSG_CONTROL_ENABLE_X=32'h00000001,
        APG_X_X_VAL_LO=8,
        APG_X_X_VAL_HI=9,
        APG_X_V_VAL=10,
        APG_X_A_VAL=11,
        APG_X_J_VAL=12,
        APG_X_JJ_VAL=13,
        APG_X_TARGET_V_VAL=14,
        APG_X_ABORT_A_VAL=15,
        BE_START_ADDR=62,
        SE_REG_LB=63;

    localparam
        STB_ASG_LOAD=32'h00000001,
        STB_BE_START=32'h20000000,
        STB_BE_ABORT=32'h40000000,
        STB_SE_INT_LB=32'h80000000;

    localparam
        INT_ASG_DONE=32'h00000001,
        INT_ASG_ABORT=32'h00000002,
        INT_BE_COMPLETE=32'h40000000,
        INT_SE_INT_LB=32'h80000000;

endmodule

