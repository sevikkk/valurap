#include <stdio.h>
#include "cmdline.h"

#include "main.h"
#include "cmsis_os.h"

extern UART_HandleTypeDef huart1;

extern TIM_HandleTypeDef htim1;
extern TIM_HandleTypeDef htim3;

extern SPI_HandleTypeDef hspi1;

volatile int32_t k_type_temp = 0;


void StartThermoRead(void const * argument) {
  uint8_t in_buffer[2];
  uint8_t out_buffer[2];
  for(;;) {
	HAL_GPIO_WritePin(SPI1_NSS_GPIO_Port, SPI1_NSS_Pin, GPIO_PIN_RESET);
        HAL_SPI_TransmitReceive(&hspi1, out_buffer, in_buffer, 2, 1000);
	HAL_GPIO_WritePin(SPI1_NSS_GPIO_Port, SPI1_NSS_Pin, GPIO_PIN_SET);
	k_type_temp = in_buffer[0] << 8 | in_buffer[1];
	printf("t: %d\n", k_type_temp >> 5);
	fflush(0);
	osDelay(500);
  };
}

void StartCmdLine(void const * argument)
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
  cmdlinePrintPrompt();
  for(;;)
  {
      if (HAL_UART_Receive(&huart1, (uint8_t *)&ch, 1, 1) == HAL_OK) {
	      cmdlineInputFunc((uint8_t)ch);
	      cmdlineMainLoop();
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
        "\n"
  );
  fflush(0);
}

void exttestFunction(void) {
  int i;
  printf("ext\n");
  fflush(0);
  for (i=0; i<10; i++) {
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

int32_t ech_ids[3] = {
  TIM_CHANNEL_1,
  TIM_CHANNEL_2,
  TIM_CHANNEL_3,
};

void sevFunction(void) {
 int32_t ch;
 int32_t val;

 ch = cmdlineGetArgInt(1);
 val = cmdlineGetArgInt(2);
 if (ch > 0 && ch <= 3)
    __HAL_TIM_SET_COMPARE(&htim3, ech_ids[ch - 1], val);
}

int32_t fch_ids[3] = {
  TIM_CHANNEL_3,
  TIM_CHANNEL_2,
  TIM_CHANNEL_1,
};

void sfvFunction(void) {
 int32_t ch;
 int32_t val;

 ch = cmdlineGetArgInt(1);
 val = cmdlineGetArgInt(2);
 if (ch > 0 && ch <= 3)
    __HAL_TIM_SET_COMPARE(&htim1, fch_ids[ch - 1], val);
}

void setup_commands() {
  cmdlineAddCommand("help",    helpFunction);
  cmdlineAddCommand("exttest", exttestFunction);
  cmdlineAddCommand("sep", sepFunction);
  cmdlineAddCommand("sfp", sfpFunction);
  cmdlineAddCommand("sev", sevFunction);
  cmdlineAddCommand("sfv", sfvFunction);
}

