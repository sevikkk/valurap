#include <Arduino.h>
#include <stdio.h>
#include <avr/pgmspace.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>

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

void s0Function(void) {
  Serial1.write(0xd5);
  Serial1.write(0x01);
  Serial1.write(0x00);
  Serial1.write(0x00);
}

void sAAFunction(void) {
  Serial1.write(0xd5);
  Serial1.write(0x01);
  Serial1.write(0xaa);
  Serial1.write(0xd1);
}

void s55Function(void) {
  Serial1.write(0xd5);
  Serial1.write(0x01);
  Serial1.write(0x55);
  Serial1.write(0xe4);
}

extern "C" void setup_commands() {
  cmdlineAddCommand("help",   helpFunction);
  cmdlineAddCommand("s0",     s0Function);
  cmdlineAddCommand("sAA",    sAAFunction);

  cmdlineAddCommand("s55",    s55Function);


}


