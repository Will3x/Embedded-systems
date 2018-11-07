// A0 : TMP36 (the middle pin)
// A1 : LDR (min side)
// PIND2 : Echo
// PIND3 : Trig
//
// TMP36 Right pin = min and left pin is plus (flat side in front)
// LDR : 3.3v
// VCC : 5v
// Refer to the setup page in manual if needed

#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16000000UL
#include <util/delay.h>

#include "AVR_TTC_scheduler.h"
#include "main.h"
#include "functies.h"
#include "init.h"

int main(void);
void setup();

int main(void)
{
	setup();
	while(1) {
		SCH_Dispatch_Tasks();
	}
}

void setup()
{
	init_connectie();
	init_adc();				// Setup the ADC
	init_USART();			// Setup the USART
	init_dist();			// Setup distance sensor
	init_scheduler();		// Setup scheduler
	init_LEDS();			// Setup LED
}