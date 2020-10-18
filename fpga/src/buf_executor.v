module buf_executor (
           input clk,
           input rst,

           // OUT_* registers interface
           output reg [5:0] ext_out_reg_addr,   /* combinatorial */
           output reg [31:0] ext_out_reg_data,  /* combinatorial */
           output reg ext_out_reg_stb,          /* combinatorial */
           input ext_out_reg_busy,

           // output STB_* interface
           output reg [31:0] ext_out_stbs,      /* combinatorial */

           // Interrupts interface
           input [31:0] ext_pending_ints,
           output reg [31:0] ext_clear_ints,    /* combinatorial */

           // Profile Generator parameters interface
           output reg [7:0] param_addr,
           output reg [31:0] param_write_data,
           output reg param_write_hi,
           output reg param_write_lo,
           input [63:0] param_read_data,

           // Input FIFO interface
           input fifo_empty,
           input [39:0] fifo_data,
           input [31:0] fifo_global_count,      /* amount of data on all fifo levels */
           input [31:0] fifo_local_count,       /* amount of data in single-clock fifo */
           output reg fifo_read,                /* combinatorial */
           output reg [31:0] fifo_expected_global_count,
           output reg [31:0] fifo_expected_local_count,

           // Management
           //     control
           input start, // Start fetching data
           input abort, // Stop and drain input fifo

           //     running state
           output reg busy,            // idle or doing something
           output reg aborting,
           output reg waiting_for_data,
           output reg waiting_for_int,

           // Previous activity status
           output reg done,            // finished by BUF_DONE
           output reg aborted,         // aborted by signal
           output reg buffer_underrun, // aborted by unexpected empty FIFO
           output reg bad_code         // runtime error
);

reg next_busy;
reg next_done;
reg next_aborting;
reg next_aborted;
reg next_buffer_underrun;
reg next_bad_code;
reg next_waiting_for_data;
reg next_waiting_for_int;

reg [31:0] next_fifo_expected_global_count;
reg [31:0] next_fifo_expected_local_count;

reg [3:0] state;
reg [3:0] next_state;

reg [39:0] command;
reg [39:0] next_command;

reg [7:0] next_param_addr;
reg [31:0] next_param_write_data;
reg next_param_write_hi;
reg next_param_write_lo;

localparam S_INIT = 0,
    S_WAIT_DONE = 1,
    S_REG_BUSY = 2,
    S_DECODE = 3,
    S_FETCH = 4,
    S_DRAIN = 5,
    S_WAIT_FOR_DATA = 6,
    S_FETCH_2 = 7;

always @(*)
    begin
        next_state <= state;
        next_command <= command;

        next_busy <= busy;
        next_done <= done;
        next_aborting <= aborting;
        next_aborted <= aborted;
        next_buffer_underrun <= buffer_underrun;
        next_bad_code <= bad_code;
        next_waiting_for_data <= waiting_for_data;
        next_waiting_for_int <= waiting_for_int;
        next_fifo_expected_global_count <= fifo_expected_global_count;
        next_fifo_expected_local_count <= fifo_expected_local_count;

        fifo_read <= 0;

        ext_out_reg_addr <= 0;
        ext_out_reg_data <= 0;
        ext_out_reg_stb <= 0;

        ext_out_stbs <= 0;
        ext_clear_ints <= 0;

        next_param_addr <= param_addr;
        next_param_write_data <= 0;
        next_param_write_hi <= 0;
        next_param_write_lo <= 0;

        if (rst || abort) begin
            next_busy <= 0;
            next_done <= 0;
            next_aborting <= 0;
            next_aborted <= 0;
            next_buffer_underrun <= 0;
            next_bad_code <= 0;
            next_waiting_for_data <= 0;
            next_waiting_for_int <= 0;
            next_fifo_expected_global_count <= 0;
            next_fifo_expected_local_count <= 0;
            next_command <= 0;
            next_param_addr <= 0;
            next_state <= S_INIT;

            if (abort) begin
                if (fifo_empty) begin
                    next_aborted <= 1;
                end
                else begin
                    next_busy <= 1;
                    fifo_read <= 1;
                    next_aborting <= 1;
                    next_state <= S_DRAIN;
                end
            end
        end else
            case (state)
                S_INIT:
                    begin
                        if (start)
                            begin
                                next_busy <= 1;
                                next_done <= 0;
                                next_aborting <= 0;
                                next_aborted <= 0;
                                next_buffer_underrun <= 0;
                                next_bad_code <= 0;
                                if (!fifo_empty) begin
                                    next_state <= S_FETCH;
                                end
                                else begin
                                    next_waiting_for_data <= 1;
                                    next_fifo_expected_global_count <= 0;
                                    next_fifo_expected_local_count <= 1;
                                    next_state <= S_WAIT_FOR_DATA;
                                end
                            end
                    end
                S_DRAIN:
                    begin
                        if (fifo_empty) begin
                            next_aborting <= 0;
                            next_aborted <= 1;
                            next_busy <= 0;
                            next_state <= S_INIT;
                        end
                        else
                            fifo_read <= 1;
                    end
                S_WAIT_FOR_DATA:
                    begin
                        if ((fifo_global_count >= fifo_expected_global_count) && (fifo_local_count >= fifo_expected_local_count)) begin
                            next_fifo_expected_global_count <= 0;
                            next_fifo_expected_local_count <= 0;
                            next_waiting_for_data <= 0;
                            next_state <= S_FETCH;
                        end
                    end
                S_FETCH:
                    begin
                        if (fifo_empty) begin
                            next_busy <= 0;
                            next_buffer_underrun <= 1;
                            next_state <= S_INIT;
                        end
                        else begin
                            fifo_read <= 1;
                            next_state <= S_FETCH_2;
                        end
                    end
                S_FETCH_2:
                    begin
                        next_command <= fifo_data;
                        next_state <= S_DECODE;
                    end
                S_DECODE:
                    begin
                        case (command[39:38])
                            2'b01: // WRITE_REG
                                begin
                                    if (!ext_out_reg_busy)
                                    begin
                                        next_state <= S_FETCH;
                                        ext_out_reg_addr <= command[37:32];
                                        ext_out_reg_data <= command[31:0];
                                        ext_out_reg_stb <= 1;
                                    end
                                end
                            2'b10: // Misc
                                case (command[37:32])
                                    0: // NOP
                                        begin
                                            next_state <= S_FETCH;
                                        end
                                    1: // STB
                                        begin
                                            ext_out_stbs <= command[31:0];
                                            next_state <= S_FETCH;
                                        end
                                    2: // WAIT_ALL
                                        begin
                                            if ((ext_pending_ints & command[31:0]) == command[31:0])
                                                begin
                                                    next_waiting_for_int <= 0;
                                                    next_state <= S_FETCH;
                                                end
                                            else
                                                begin
                                                    next_waiting_for_int <= 1;
                                                end
                                        end
                                    3: // WAIT_ANY
                                        begin
                                            if ((ext_pending_ints & command[31:0]) != 0)
                                                begin
                                                    next_state <= S_FETCH;
                                                    next_waiting_for_int <= 0;
                                                end
                                            else
                                                begin
                                                    next_waiting_for_int <= 1;
                                                end
                                        end
                                    4: // CLEAR clear ints
                                        begin
                                            ext_clear_ints <= command[31:0];
                                            next_state <= S_FETCH;
                                        end
                                    5: // WAIT_FIFO wait until fifo has at least specified amount of data
                                        begin
                                            if (command[31]) begin
                                                next_fifo_expected_global_count <= {1'b0, command[30:0]};
                                            end
                                            else begin
                                                next_fifo_expected_local_count <= {1'b0, command[30:0]};
                                            end
                                            next_waiting_for_data <= 1;
                                            next_state <= S_WAIT_FOR_DATA;
                                        end

                                    6: // PARAM_ADDR set address for param writes
                                        begin
                                            next_param_addr <= command[7:0];
                                            next_state <= S_FETCH;
                                        end
                                    7: // PARAM_WRITE_HI write to high 32 bits of param
                                        begin
                                            next_param_write_data <= command[31:0];
                                            next_param_write_hi <= 1;
                                            next_state <= S_FETCH;
                                        end
                                    8,9,10,11,12,13,14: // PARAM_WRITE_LO_* write to low 32 bits of param with addr preincrement
                                        // 8 - PARAM_WRITE_LO - no increment
                                        // 9 - PARAM_WRITE_LO_1 - +1
                                        // ...
                                        // 14 - PARAM_WRITE_LO_1 - +6
                                        begin
                                            next_param_write_data <= command[31:0];
                                            next_param_write_lo <= 1;
                                            next_param_addr <= param_addr + command[34:32];
                                            next_state <= S_FETCH;
                                        end
                                    15: // PARAM_WRITE_LO_NC write to low 32 bits of param with addr preincrement to next channel status
                                        // ADDR = ( ADDR + 0x20 ) & 0xE0
                                        begin
                                            next_param_write_data <= command[31:0];
                                            next_param_write_lo <= 1;
                                            next_param_addr <= (param_addr + 8'h20) & 8'hE0;
                                            next_state <= S_FETCH;
                                        end
                                    63: // DONE
                                        begin
                                            next_done <= 1;
                                            next_busy <= 0;
                                            next_state <= S_INIT;
                                        end
                                    default: // halt on error
                                        begin
                                            next_bad_code <= 1;
                                            next_busy <= 0;
                                            next_state <= S_INIT;
                                        end
                                endcase
                            default: // halt on error
                                begin
                                    next_bad_code <= 1;
                                    next_busy <= 0;
                                    next_state <= S_INIT;
                                end
                        endcase
                    end
            endcase
    end

always @(posedge clk)
    begin
        state <= next_state;
        command <= next_command;

        busy <= next_busy;
        done <= next_done;
        aborting <= next_aborting;
        aborted <= next_aborted;
        buffer_underrun <= next_buffer_underrun;
        bad_code <= next_bad_code;
        waiting_for_data <= next_waiting_for_data;
        waiting_for_int <= next_waiting_for_int;
        fifo_expected_global_count <= next_fifo_expected_global_count;
        fifo_expected_local_count <= next_fifo_expected_local_count;
        param_addr <= next_param_addr;
        param_write_data <= next_param_write_data;
        param_write_hi <= next_param_write_hi;
        param_write_lo <= next_param_write_lo;
    end

endmodule