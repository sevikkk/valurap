//
// Created by Vsevolod Lobko on 02.11.2019.
//

#include <stdio.h>
#include "cmsis_os.h"
#include "main.h"
#include "hardware.h"

#include "task_thermo.h"
#include "task_s3g.h"

#define CMD_PING 0
#define CMD_QUERY 1
#define CMD_SET_PID_TARGET 2
#define CMD_SET_PID_PARAMS 3

enum S3G_State {
    S_START = 0,
    S_LEN,
    S_DATA,
    S_CRC,
};

#define START_BYTE 0xD5

uint8_t send_buffer[256];
uint8_t receive_buffer[256];
uint8_t send_buffer_len = 0;
uint8_t send_buffer_crc = 0;
int receive_buffer_len = 0;

static __inline__ uint8_t _crc_ibutton_update(uint8_t crc, uint8_t data) {
    uint8_t i;

    crc = crc ^ data;
    for (i = 0; i < 8; i++) {
        if (crc & 0x01)
            crc = (crc >> 1) ^ 0x8C;
        else
            crc >>= 1;
    }

    return crc;
}

void process_command();

void append8(uint8_t value);
void append16(uint16_t value);
void append32(uint32_t value);
void reset_send_buffer();
void send_packet();

void StartS3GIO(void const *argument) {
    uint8_t ch;
    uint8_t len;
    uint8_t crc;

    reset_send_buffer();
    append16(65535);
    append8(0x55);
    append8(0xAA);
    send_packet();

    enum S3G_State state = S_START;
    crc = 0;
    for (;;) {
        if (xQueueReceive(s3g_rx_bufHandle, &ch, (TickType_t)100)) {
            if (state == S_START) {
                if (ch == START_BYTE) {
                    state = S_LEN;
                    crc = 0;
                }
            } else if (state == S_LEN) {
                len = ch;
                receive_buffer_len = 0;
                state = len == 0 ? S_CRC : S_DATA;
            } else if (state == S_DATA) {
                receive_buffer[receive_buffer_len++] = ch;
                crc = _crc_ibutton_update(crc, ch);
                if (receive_buffer_len == len) state = S_CRC;
            } else if (state == S_CRC) {
                printf("Got command\n len: %d expected crc: %02X\n",
                       receive_buffer_len, crc);
                if (ch == crc) process_command();
                state = S_START;
            }
        } else
            taskYIELD()
    }
}

uint8_t read8(uint8_t index) { return receive_buffer[index]; }

uint16_t read16(uint8_t index) {
    union {
        uint16_t a;
        struct {
            uint8_t data[2];
        } b;
    } shared;
    shared.b.data[0] = receive_buffer[index];
    shared.b.data[1] = receive_buffer[index + 1];

    return shared.a;
}

uint32_t read32(uint8_t index) {
    union {
        uint32_t a;
        struct {
            uint8_t data[4];
        } b;
    } shared;
    shared.b.data[0] = receive_buffer[index];
    shared.b.data[1] = receive_buffer[index + 1];
    shared.b.data[2] = receive_buffer[index + 2];
    shared.b.data[3] = receive_buffer[index + 3];

    return shared.a;
}
void reset_send_buffer() {
    send_buffer_crc = 0;
    send_buffer_len = 2;
    send_buffer[0] = 0xD5;
    send_buffer[1] = 0;
}

void send_packet() {
    send_buffer[1] = send_buffer_len - 2;
    send_buffer[send_buffer_len] = send_buffer_crc;
    while (HAL_UART_Transmit(&huart1, (uint8_t *)send_buffer,
                             send_buffer_len + 1, 0xFFFF) != HAL_OK)
        taskYIELD()
}

void appendByte(uint8_t data) {
    if (send_buffer_len < 250) {
        send_buffer_crc = _crc_ibutton_update(send_buffer_crc, data);
        send_buffer[send_buffer_len] = data;
        send_buffer_len++;
    }
}

// Add an 8-bit byte to the end of the payload
void append8(uint8_t value) { appendByte(value); }
void append16(uint16_t value) {
    appendByte(value & 0xff);
    appendByte((value >> 8) & 0xff);
}
void append32(uint32_t value) {
    appendByte(value & 0xff);
    appendByte((value >> 8) & 0xff);
    appendByte((value >> 16) & 0xff);
    appendByte((value >> 24) & 0xff);
}

void process_command() {
    int i;
    for (i = 0; i < receive_buffer_len; i++)
        printf(" %3d: %02X\n", i, receive_buffer[i]);
    printf("---\n");
    uint16_t cmd_id = read16(0);
    uint8_t cmd = read8(2);

    if (cmd == CMD_PING) {
        reset_send_buffer();
        append16(cmd_id);
        append8(0x81);
        append32(read32(3) + 123);
        send_packet();
    } else if (cmd == CMD_QUERY) {
        reset_send_buffer();
        append16(cmd_id);
        append8(0x81);
        append16(k_type_temp);
        append16(adc_reads[0]);
        append16(adc_reads[1]);
        append16(adc_reads[2]);
        append16(ext_values[0]);
        append16(ext_values[2]);
        append16(ext_values[2]);
        append16(pid_targets[0]);
        append16(pid_targets[1]);
        append16(pid_targets[2]);
        send_packet();
    } else if (cmd == CMD_SET_PID_TARGET) {
        uint8_t channel = read8(3);
        int target = read16(4);
        if (channel >= 1 && channel <= 3) {
            pid_targets[channel - 1] = target;
            reset_send_buffer();
            append16(cmd_id);
            append8(0x81);
            send_packet();
        }
    } else if (cmd == CMD_SET_PID_PARAMS) {
        uint8_t channel = read8(3);
        int k_p = read16(4);
        int k_i = read16(6);
        if (channel >= 1 && channel <= 3) {
            pid_k_p[channel - 1] = k_p;
            pid_k_i[channel - 1] = k_i;
            reset_send_buffer();
            append16(cmd_id);
            append8(0x81);
            send_packet();
        }
    }
}
