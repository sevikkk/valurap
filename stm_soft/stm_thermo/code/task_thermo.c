//
// Created by Vsevolod Lobko on 02.11.2019.
//

#include <stdio.h>

#include "main.h"
#include "cmsis_os.h"
#include "cmdline.h"
#include "hardware.h"

volatile int32_t pid_targets[3] = {5000, 5000, 5000};
volatile int32_t pid_integrals[3];
volatile int32_t pid_k_i[3] = {500, 500, 500};
volatile int32_t pid_k_p[3] = {4000, 4000, 4000};

volatile int32_t k_type_temp = 0;
volatile int32_t adc_reads[5];
volatile int32_t ext_values[3];
volatile int32_t fan_values[3];

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

void StartThermoRead(void const* argument) {
    uint8_t in_buffer[2];
    uint8_t out_buffer[2];
    uint32_t adc_vals[5];
    uint32_t channels[5] = {ADC_CHANNEL_0, ADC_CHANNEL_4, ADC_CHANNEL_5,
                            ADC_CHANNEL_TEMPSENSOR, ADC_CHANNEL_VREFINT};
    ADC_ChannelConfTypeDef sConfig = {0};
    int i, j;

    TickType_t last_wake;

#define PID_CYCLE 400
#define PID_ADC_SUPERSAMPLE 250

    last_wake = xTaskGetTickCount() + 33;

    for (;;) {
        HAL_GPIO_WritePin(SPI1_NSS_GPIO_Port, SPI1_NSS_Pin, GPIO_PIN_RESET);
        HAL_SPI_TransmitReceive(&hspi1, out_buffer, in_buffer, 2, 1000);
        HAL_GPIO_WritePin(SPI1_NSS_GPIO_Port, SPI1_NSS_Pin, GPIO_PIN_SET);
        k_type_temp = (((uint32_t)in_buffer[0] << 8u) | (uint32_t)in_buffer[1]);

        for (i = 0; i < 5; i++) adc_vals[i] = 0;

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
                }
                HAL_ADC_Stop(&hadc1);
            }

        for (i = 0; i < 5; i++) {
            adc_reads[i] = adc_vals[i] / PID_ADC_SUPERSAMPLE;
        }

        for (i = 0; i < 3; i++) {
            int pid_error = adc_reads[i] - pid_targets[i];
            int control_value = 0;

            if (pid_error > 1000) {
                control_value = 500;
            } else if (pid_error < -1000) {
                control_value = 0;
            } else {
                int new_pid_integral = pid_integrals[i];

                new_pid_integral += pid_error * pid_k_i[i] / 1000;

                if (new_pid_integral > 15000) new_pid_integral = 15000;
                if (new_pid_integral < -5000) new_pid_integral = -5000;

                pid_integrals[i] = new_pid_integral;
                control_value =
                    new_pid_integral / 10 + pid_error * pid_k_p[i] / 1000;
            }
            if (control_value > 500) control_value = 500;
            if (control_value < 30) control_value = 0;

            __HAL_TIM_SET_COMPARE(&htim3, ech_ids[i], control_value);
        }

        for (i = 0; i < 3; i++) {
            ext_values[i] = __HAL_TIM_GET_COMPARE(&htim3, ech_ids[i]);
            fan_values[i] = __HAL_TIM_GET_COMPARE(&htim1, fch_ids[i]);
        }
        vTaskDelayUntil(&last_wake, PID_CYCLE);
    }
}

void sepFunction(void) {
    int32_t psc;
    psc = cmdlineGetArgInt(1);
    __HAL_TIM_SET_PRESCALER(&htim3, psc);
}

void sfpFunction(void) {
    int32_t psc;
    psc = cmdlineGetArgInt(1);
    __HAL_TIM_SET_PRESCALER(&htim1, psc);
}

void sevFunction(void) {
    int32_t ch;
    int32_t val;

    ch = cmdlineGetArgInt(1);
    val = cmdlineGetArgInt(2);
    if (ch > 0 && ch <= 3) __HAL_TIM_SET_COMPARE(&htim3, ech_ids[ch - 1], val);
}

void sfvFunction(void) {
    int32_t ch;
    int32_t val;

    ch = cmdlineGetArgInt(1);
    val = cmdlineGetArgInt(2);
    if (ch > 0 && ch <= 3) __HAL_TIM_SET_COMPARE(&htim1, fch_ids[ch - 1], val);
}

void sptFunction(void) {
    int32_t ch;
    int32_t val;

    ch = cmdlineGetArgInt(1);
    val = cmdlineGetArgInt(2);
    if (ch > 0 && ch <= 3) pid_targets[ch - 1] = val;
}

void sppFunction(void) {
    int32_t ch;
    int32_t val_p;
    int32_t val_i;

    ch = cmdlineGetArgInt(1);
    val_p = cmdlineGetArgInt(2);
    val_i = cmdlineGetArgInt(3);
    if (ch > 0 && ch <= 3) {
        pid_k_p[ch - 1] = val_p;
        pid_k_i[ch - 1] = val_i;
    }
}

void shpidFunction(void) {
    int32_t ch;

    ch = cmdlineGetArgInt(1);
    if (ch <= 0 || ch > 3) return;

    printf("pid_k_p: %ld\n", pid_k_p[ch - 1]);
    printf("pid_k_i: %ld\n", pid_k_i[ch - 1]);
    printf("integral: %ld\n", pid_integrals[ch - 1]);
    fflush(0);
}