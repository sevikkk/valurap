#include <stdio.h>
#include <avr/pgmspace.h>
#include "cmdline.h"

void helpFunction(void)
{
  printf_P(PSTR(
        "\n"
        "Available commands are:\n"
        "help      - displays available commands\n"
        "\n"
  ));
}


void setup_commands() {
  cmdlineAddCommand("help",   helpFunction);

}


