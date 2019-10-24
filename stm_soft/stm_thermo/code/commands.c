#include <stdio.h>
#include "cmdline.h"

#include "main.h"
#include "cmsis_os.h"

extern UART_HandleTypeDef huart1;

void StartCmdLine(void const * argument)
{
  char ch;
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
        "help      - displays available commands\n"
        "\n"
  );
  fflush(0);
}

void s55Function(void) {
  printf("s55\n");
  fflush(0);
  osDelay(1000);
  printf("/s55\n");
}

void setup_commands() {
  cmdlineAddCommand("help",   helpFunction);
  cmdlineAddCommand("s55",    s55Function);
}

