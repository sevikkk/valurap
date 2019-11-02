#include <stdio.h>

#include "cmdline.h"
#include "cmsis_os.h"
#include "main.h"
#include "hardware.h"
#include "task_thermo.h"

extern char* build_timestamp;

void helpFunction(void) {
    printf(
        "\n"
        "Available commands are:\n"
        "help         - displays available commands\n"
        "clear        - clear screen\n"
        "exttest      - turm extra channels on and off\n"
        "sep <N>      - set extruders prescaler to N\n"
        "sfp <N>      - set fans prescaler to N\n"
        "sev <C> <N>  - set extruder C to N\n"
        "sfv <C> <N>  - set fan C to N\n"
        "spt <C> <N>  - set PID target for channel C to N\n"
        "spp <C> <k_p> <k_i> - set PID parameters for channel C\n"
        "shpid <C>    - show PID state for channel C\n"
        "\n");
    fflush(0);
}

void exttestFunction(void) {
    int i;
    printf("ext\n");
    fflush(0);
    for (i = 0; i < 10; i++) {
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_14, GPIO_PIN_SET);
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_15, GPIO_PIN_SET);
        osDelay(1000);
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_14, GPIO_PIN_RESET);
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_15, GPIO_PIN_RESET);
        osDelay(1000);
    };
    printf("/ext\n");
    fflush(0);
}

void clearFunction(void) {
    printf("\x1b[0m\x1b[2J\n\n");
    fflush(0);
}

void setup_commands() {
    cmdlineAddCommand("help", helpFunction);
    cmdlineAddCommand("clear", clearFunction);
    cmdlineAddCommand("exttest", exttestFunction);
    cmdlineAddCommand("sep", sepFunction);
    cmdlineAddCommand("sfp", sfpFunction);
    cmdlineAddCommand("sev", sevFunction);
    cmdlineAddCommand("sfv", sfvFunction);
    cmdlineAddCommand("spt", sptFunction);
    cmdlineAddCommand("spp", sppFunction);
    cmdlineAddCommand("shpid", shpidFunction);
}

void StartCmdLine(void const* argument) {
    char ch;

    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_1);
    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_2);
    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_3);

    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_3);

    cmdlineInit();
    setup_commands();
    printf("\x1b[0m\n\n\x1b[1mSTMThermo\x1b[0m (%s)\n\n", build_timestamp);
    fflush(0);
    if (xSemaphoreTake(consoleMtxHandle, (TickType_t)1000) == pdTRUE) {
        cmdlinePrintPrompt();
        xSemaphoreGive(consoleMtxHandle);
    };
    for (;;) {
        if (HAL_UART_Receive(&huart2, (uint8_t*)&ch, 1, 1) == HAL_OK) {
            if (xSemaphoreTake(consoleMtxHandle, (TickType_t)1000) == pdTRUE) {
                cmdlineInputFunc((uint8_t)ch);
                xSemaphoreGive(consoleMtxHandle);
            };
            if (cmdlineMainLoop()) {
                if (xSemaphoreTake(consoleMtxHandle, (TickType_t)1000) ==
                    pdTRUE) {
                    cmdlinePrintPrompt();
                    xSemaphoreGive(consoleMtxHandle);
                };
            }
        } else {
            taskYIELD();
        };
    }
}
