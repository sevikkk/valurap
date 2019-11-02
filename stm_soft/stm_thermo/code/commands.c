#include <stdio.h>

#include "cmdline.h"
#include "cmsis_os.h"
#include "main.h"

extern UART_HandleTypeDef huart2;

extern TIM_HandleTypeDef htim1;
extern TIM_HandleTypeDef htim3;

extern SPI_HandleTypeDef hspi1;

extern ADC_HandleTypeDef hadc1;

extern osMutexId consoleMtxHandle;

volatile int32_t k_type_temp = 0;
volatile int32_t adc_reads[5];
volatile int32_t ext_values[3];
volatile int32_t fan_values[3];

volatile int32_t pid_targets[3] = { 5000, 5000, 5000 };
volatile int32_t pid_integrals[3];
volatile int32_t pid_k_i[3] = { 500, 500, 500 };
volatile int32_t pid_k_p[3] = { 4000, 4000, 4000 };

int32_t ech_ids[3] = {
    TIM_CHANNEL_1,
    TIM_CHANNEL_2,
    TIM_CHANNEL_3,
};

int32_t fch_ids[3] = {
    TIM_CHANNEL_3,
    TIM_CHANNEL_2,
    TIM_CHANNEL_1,
};

void StartThermoRead(void const* argument)
{
    uint8_t in_buffer[2];
    uint8_t out_buffer[2];
    uint32_t adc_vals[5];
    uint32_t channels[5] = {
        ADC_CHANNEL_0,
        ADC_CHANNEL_4,
        ADC_CHANNEL_5,
        ADC_CHANNEL_TEMPSENSOR,
        ADC_CHANNEL_VREFINT
    };
    ADC_ChannelConfTypeDef sConfig = { 0 };
    int i, j;

    TickType_t start_ticks, cur_ticks, last_wake;
    int real_time;
    int cycle_time;

#define PID_CYCLE 400
#define PID_ADC_SUPERSAMPLE 250

    last_wake = xTaskGetTickCount() + 33;

    for (;;) {
        cur_ticks = xTaskGetTickCount();
        cycle_time = cur_ticks - start_ticks;
        start_ticks = cur_ticks;

        HAL_GPIO_WritePin(SPI1_NSS_GPIO_Port, SPI1_NSS_Pin, GPIO_PIN_RESET);
        HAL_SPI_TransmitReceive(&hspi1, out_buffer, in_buffer, 2, 1000);
        HAL_GPIO_WritePin(SPI1_NSS_GPIO_Port, SPI1_NSS_Pin, GPIO_PIN_SET);
        k_type_temp = in_buffer[0] << 8 | in_buffer[1];

        for (i = 0; i < 5; i++)
            adc_vals[i] = 0;

        for (j = 0; j < PID_ADC_SUPERSAMPLE; j++)
            for (i = 0; i < 5; i++) {
                sConfig.Channel = channels[i];
                sConfig.Rank = ADC_REGULAR_RANK_1;
                sConfig.SamplingTime = ADC_SAMPLETIME_41CYCLES_5;
                HAL_ADC_ConfigChannel(&hadc1, &sConfig);
                HAL_ADC_Start(&hadc1);
                if (HAL_ADC_PollForConversion(&hadc1, 1000000) == HAL_OK) {
                    adc_vals[i] += HAL_ADC_GetValue(&hadc1);
                } else {
                    adc_vals[i] += 9999;
                };
                HAL_ADC_Stop(&hadc1);
            };
        /* printf("k-t: %d\n", k_type_temp >> 5); */
        for (i = 0; i < 5; i++) {
            /* printf("adc%d: %d\n", i, adc_vals[i]/100); */
            adc_reads[i] = adc_vals[i] / PID_ADC_SUPERSAMPLE;
        };

        for (i = 0; i < 3; i++) {
            int pid_error = adc_reads[i] - pid_targets[i];
            int current_value = ext_values[i];
            int control_value = 0;

            if (pid_error > 1000) {
                control_value = 500;
            } else if (pid_error < -1000) {
                control_value = 0;
            } else {
                int new_pid_integral = pid_integrals[i];

                new_pid_integral += pid_error * pid_k_i[i] / 1000;

                if (new_pid_integral > 15000)
                    new_pid_integral = 15000;
                if (new_pid_integral < -5000)
                    new_pid_integral = -5000;

                pid_integrals[i] = new_pid_integral;
                control_value = new_pid_integral / 10 + pid_error * pid_k_p[i] / 1000;
            };
            if (control_value > 500)
                control_value = 500;
            if (control_value < 30)
                control_value = 0;

            __HAL_TIM_SET_COMPARE(&htim3, ech_ids[i], control_value);
        };

        for (i = 0; i < 3; i++) {
            ext_values[i] = __HAL_TIM_GET_COMPARE(&htim3, ech_ids[i]);
            fan_values[i] = __HAL_TIM_GET_COMPARE(&htim1, fch_ids[i]);
            /* printf("ext%d: %d\n", i, ext_values[i]);
		printf("fan%d: %d\n", i, fan_values[i]); */
        };
        /* fflush(0); */
        cur_ticks = xTaskGetTickCount();
        /* printf("rt: %d %d %d\n", real_time, cycle_time, last_wake); */
        vTaskDelayUntil(&last_wake, PID_CYCLE);
    };
}

void StartCmdLine(void const* argument)
{
    char ch;

    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_1);
    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_2);
    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_3);

    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_3);

    cmdlineInit();
    setup_commands();
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
                if (xSemaphoreTake(consoleMtxHandle, (TickType_t)1000) == pdTRUE) {
                    cmdlinePrintPrompt();
                    xSemaphoreGive(consoleMtxHandle);
                };
            }
        } else {
            taskYIELD();
        };
    }
}

void helpFunction(void)
{
    printf(
        "\n"
        "Available commands are:\n"
        "help         - displays available commands\n"
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

void exttestFunction(void)
{
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

void sepFunction(void)
{
    int32_t psc;
    psc = cmdlineGetArgInt(1);
    __HAL_TIM_SET_PRESCALER(&htim3, psc);
}

void sfpFunction(void)
{
    int32_t psc;
    psc = cmdlineGetArgInt(1);
    __HAL_TIM_SET_PRESCALER(&htim1, psc);
}

void sevFunction(void)
{
    int32_t ch;
    int32_t val;

    ch = cmdlineGetArgInt(1);
    val = cmdlineGetArgInt(2);
    if (ch > 0 && ch <= 3)
        __HAL_TIM_SET_COMPARE(&htim3, ech_ids[ch - 1], val);
}

void sfvFunction(void)
{
    int32_t ch;
    int32_t val;

    ch = cmdlineGetArgInt(1);
    val = cmdlineGetArgInt(2);
    if (ch > 0 && ch <= 3)
        __HAL_TIM_SET_COMPARE(&htim1, fch_ids[ch - 1], val);
}

void sptFunction(void)
{
    int32_t ch;
    int32_t val;

    ch = cmdlineGetArgInt(1);
    val = cmdlineGetArgInt(2);
    if (ch > 0 && ch <= 3)
        pid_targets[ch - 1] = val;
}

void sppFunction(void)
{
    int32_t ch;
    int32_t val_p;
    int32_t val_i;

    ch = cmdlineGetArgInt(1);
    val_p = cmdlineGetArgInt(2);
    val_i = cmdlineGetArgInt(3);
    if (ch > 0 && ch <= 3) {
        pid_k_p[ch - 1] = val_p;
        pid_k_i[ch - 1] = val_i;
    };
}

void shpidFunction(void)
{
    int32_t ch;

    ch = cmdlineGetArgInt(1);
    if (ch <= 0 && ch > 3)
        return;

    printf("pid_k_p: %d\n", pid_k_p[ch - 1]);
    printf("pid_k_i: %d\n", pid_k_i[ch - 1]);
    printf("integral: %d\n", pid_integrals[ch - 1]);
    fflush(0);
}

void setup_commands()
{
    cmdlineAddCommand("help", helpFunction);
    cmdlineAddCommand("exttest", exttestFunction);
    cmdlineAddCommand("sep", sepFunction);
    cmdlineAddCommand("sfp", sfpFunction);
    cmdlineAddCommand("sev", sevFunction);
    cmdlineAddCommand("sfv", sfvFunction);
    cmdlineAddCommand("spt", sptFunction);
    cmdlineAddCommand("spp", sppFunction);
    cmdlineAddCommand("shpid", shpidFunction);
}
