#include "main.h"
#include "cmsis_os.h"
#include <stdio.h>

extern UART_HandleTypeDef huart1;

#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)

void StartDebugBlink(void const * argument)
{
  int i = 0;
  for(;;)
  {
    HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_RESET);
    osDelay(50);
    HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_SET);
    osDelay(450);
    printf("%d. ", i);
    fflush(0);
    i++;
    /* HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF); */
  }
}

void uart_putc(char ch) {
      HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF);
}

int _write_r (struct _reent *r, int file, char * ptr, int len)
{
  if (file == 1 || file == 2) {
     int index;
     for(index=0; index<len; index++) {
          if (ptr[index] == '\n')
          {
            uart_putc('\r');
          }
          uart_putc(ptr[index]);
     }
  }
  return len;
}
