#include "main.h"
#include "cmsis_os.h"
#include <stdio.h>

extern UART_HandleTypeDef huart1;

extern volatile int32_t k_type_temp;
extern volatile int32_t adc_reads[5];
extern volatile int32_t ext_values[3];
extern volatile int32_t fan_values[3];

#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#define ESC_TO_STATUS "\x1b[s\x1b[1;1H\x1b[2K"
#define ESC_BOLD "\x1b[1m"
#define ESC_NORMAL "\x1b[0m"
#define ESC_BACK "\x1b[u"

void StartDebugBlink(void const * argument)
{
  int i = 0;
  for(;;)
  {
    HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_RESET);
    osDelay(50);
    HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_SET);
    osDelay(450);
    printf(ESC_TO_STATUS ESC_BOLD
		    "[%d] | K-t: %3d | TH: %4d %4d %4d"
		    " | Ext: %4d %4d %4d"
		    " | Fan: %4d %4d %4d"
		    ESC_NORMAL ESC_BACK, 
		    i,
		    k_type_temp >> 5,
		    adc_reads[0],
		    adc_reads[1],
		    adc_reads[2],
		    ext_values[0],
		    ext_values[1],
		    ext_values[2],
		    fan_values[0],
		    fan_values[1],
		    fan_values[2]
    );
    fflush(0);
    i++;
    /* HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF); */
  }
}

void uart_putc(char ch) {
      while (HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF) != HAL_OK) taskYIELD();
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
