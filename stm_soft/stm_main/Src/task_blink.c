#include "main.h"
#include "cmsis_os.h"

void StartDebugBlink(void const * argument)
{
  for(;;)
  {
    HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_RESET);
    osDelay(100);
    HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_SET);
    osDelay(500);
  }
}

