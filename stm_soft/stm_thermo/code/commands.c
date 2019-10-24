#include <stdio.h>
#include "cmdline.h"

void helpFunction(void)
{
  printf(
        "\n"
        "Available commands are:\n"
        "help      - displays available commands\n"
        "\n"
  );
}

void s55Function(void) {
	printf("s55\n");
}

void setup_commands() {
  cmdlineAddCommand("help",   helpFunction);
  cmdlineAddCommand("s55",    s55Function);
}

