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
#define EXT1_ON_Pin GPIO_PIN_14
#define EXT1_ON_GPIO_Port GPIOC
#define EXT2_ON_Pin GPIO_PIN_15
#define EXT2_ON_GPIO_Port GPIOC
#define ADC_TH1_Pin GPIO_PIN_0
#define ADC_TH1_GPIO_Port GPIOA
#define RS485_DE_Pin GPIO_PIN_1
#define RS485_DE_GPIO_Port GPIOA
#define RS485_TX_Pin GPIO_PIN_2
#define RS485_TX_GPIO_Port GPIOA
#define RS485_RX_Pin GPIO_PIN_3
#define RS485_RX_GPIO_Port GPIOA
#define ADC_TH2_Pin GPIO_PIN_4
#define ADC_TH2_GPIO_Port GPIOA
#define ADC_TH3_Pin GPIO_PIN_5
#define ADC_TH3_GPIO_Port GPIOA
#define TIM3_CH1_E1_Pin GPIO_PIN_6
#define TIM3_CH1_E1_GPIO_Port GPIOA
#define TIM3_CH2_E2_Pin GPIO_PIN_7
#define TIM3_CH2_E2_GPIO_Port GPIOA
#define TIM3_CH3_E3_Pin GPIO_PIN_0
#define TIM3_CH3_E3_GPIO_Port GPIOB
#define TIM1_CH1N_F3_Pin GPIO_PIN_13
#define TIM1_CH1N_F3_GPIO_Port GPIOB
#define TIM1_CH2N_F2_Pin GPIO_PIN_14
#define TIM1_CH2N_F2_GPIO_Port GPIOB
#define TIM1_CH3N_F1_Pin GPIO_PIN_15
#define TIM1_CH3N_F1_GPIO_Port GPIOB
#define SPI1_NSS_Pin GPIO_PIN_15
#define SPI1_NSS_GPIO_Port GPIOA
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
