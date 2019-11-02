//
// Created by Vsevolod Lobko on 02.11.2019.
//

#ifndef STM_THERMO_HARDWARE_H
#define STM_THERMO_HARDWARE_H

extern ADC_HandleTypeDef hadc1;

extern SPI_HandleTypeDef hspi1;

extern TIM_HandleTypeDef htim1;
extern TIM_HandleTypeDef htim3;

extern UART_HandleTypeDef huart1;
extern UART_HandleTypeDef huart2;

extern osThreadId defaultTaskHandle;
extern osThreadId DebugBlinkHandle;
extern osThreadId CmdLineHandle;
extern osThreadId ThermoReadHandle;
extern osThreadId S3G_IOHandle;
extern osMutexId consoleMtxHandle;

#endif  // STM_THERMO_HARDWARE_H
