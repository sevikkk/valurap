//
// Created by Vsevolod Lobko on 02.11.2019.
//

#include <stdio.h>
#include "cmsis_os.h"
#include "main.h"
#include "hardware.h"

#include "task_thermo.h"
#include "task_s3g.h"

enum S3G_State {
    S_START = 0,
    S_LEN,
    S_DATA,
    S_CRC,
};

#define START_BYTE 0xD5

char send_buffer[256];
char receive_buffer[256];
int send_buffer_ready = 0;
int send_buffer_len = 0;
int receive_buffer_len = 0;

int check_crc(uint8_t ch);

void process_command();

void StartS3GIO(void const* argument) {
    uint8_t ch;
    uint8_t len;
    enum S3G_State state = S_START;
    for (;;) {
        if (xQueueReceive(s3g_rx_bufHandle, &ch, (TickType_t)100)) {
            if (state == S_START) {
                if (ch == START_BYTE) {
                    state = S_LEN;
                }
            } else if (state == S_LEN) {
                len = ch;
                receive_buffer_len = 0;
                state = len == 0 ? S_CRC : S_DATA;
            } else if (state == S_DATA) {
                receive_buffer[receive_buffer_len++] = ch;
                if (receive_buffer_len == len) state = S_CRC;
            } else if (state == S_CRC) {
                if (check_crc(ch)) process_command();
                state = S_START;
            }
        } else
            taskYIELD()
    }
}

void process_command() {
    int i;
    printf("Got command\n len: %d\n", receive_buffer_len);
    for (i = 0; i < receive_buffer_len; i++)
        printf(" %3d: %02X\n", i, receive_buffer[i]);
    printf("---\n");
}

int check_crc(uint8_t ch) { return 1; }
