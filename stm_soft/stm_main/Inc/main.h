/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under Ultimate Liberty license
  * SLA0044, the "License"; You may not use this file except in compliance with
  * the License. You may obtain a copy of the License at:
  *                             www.st.com/SLA0044
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define DEBUG_LED_Pin GPIO_PIN_13
#define DEBUG_LED_GPIO_Port GPIOC
#define TH3_Pin GPIO_PIN_7
#define TH3_GPIO_Port GPIOA
#define TH2_Pin GPIO_PIN_0
#define TH2_GPIO_Port GPIOB
#define TH1_Pin GPIO_PIN_1
#define TH1_GPIO_Port GPIOB
#define HEAT_3_Pin GPIO_PIN_10
#define HEAT_3_GPIO_Port GPIOB
#define FPGA_INT_Pin GPIO_PIN_8
#define FPGA_INT_GPIO_Port GPIOA
#define ISP_TX_Pin GPIO_PIN_9
#define ISP_TX_GPIO_Port GPIOA
#define ISP_RX_Pin GPIO_PIN_10
#define ISP_RX_GPIO_Port GPIOA
#define HEAT_1_Pin GPIO_PIN_15
#define HEAT_1_GPIO_Port GPIOA
#define HEAT_2_Pin GPIO_PIN_3
#define HEAT_2_GPIO_Port GPIOB
#define USART1_RE_Pin GPIO_PIN_5
#define USART1_RE_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
