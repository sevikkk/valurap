#include <stdio.h>
#include "cmsis_os.h"
#include "main.h"
#include "hardware.h"
#include "task_thermo.h"

#define ESC_TO_STATUS "\x1b[s\x1b[1;1H\x1b[2K"
#define ESC_BOLD "\x1b[1m"
#define ESC_NORMAL "\x1b[0m"
#define ESC_BACK "\x1b[u"

void StartDebugBlink(void const* argument) {
    TickType_t last_wake;

    int i = 0, h, m, s;
    last_wake = (xTaskGetTickCount() / 500) * 500;

    for (;;) {
        HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_RESET);
        osDelay(50);
        s = i / 2;

        m = s / 60;
        s -= m * 60;

        h = m / 60;
        m -= h * 60;

        HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_SET);
        printf(ESC_TO_STATUS ESC_BOLD
               "[%d:%02d:%02d] | K-t: %3d.%02d | TH: %4d/%3d[%4d] %4d/%3d[%4d] %4d/%3d[%4d]"
               " | Ext: %4d %4d %4d"
               " | Fan: %4d %4d %4d" ESC_NORMAL ESC_BACK,
               h, m, s,
               k_type_temp >> 5,
               25*(k_type_temp >> 3 & 0x3),
               adc_reads[0], adc_temps[0], pid_targets[0],
               adc_reads[1], adc_temps[1], pid_targets[1],
               adc_reads[2], adc_temps[2], pid_targets[2],
               ext_values[0], ext_values[1], ext_values[2], fan_values[0],
               fan_values[1], fan_values[2]);
        fflush(0);
        i++;
        vTaskDelayUntil(&last_wake, 500);
    }
}

void uart_putc(char ch) {
    while (HAL_UART_Transmit(&huart2, (uint8_t*)&ch, 1, 0xFFFF) != HAL_OK)
        taskYIELD();
}

int _write_r(struct _reent* r, int file, char* ptr, int len) {
    if (file == 1 || file == 2) {
        int index;
        while (xSemaphoreTake(consoleMtxHandle, (TickType_t)100) != pdTRUE)
            taskYIELD();
        for (index = 0; index < len; index++) {
            if (ptr[index] == '\n') {
                uart_putc('\r');
            }
            uart_putc(ptr[index]);
        }
        xSemaphoreGive(consoleMtxHandle);
    }
    return len;
}
