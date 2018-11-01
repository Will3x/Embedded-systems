// A0 : TMP36 (middelste van de 3)
// A1 : LDR (min kant)
// PIND2 : Echo
// PIND3 : Trig
//
// TMP36 rechts = min en links is plus (platte kant voor)
// LDR plus aangesloten op 3,3 V
// VCC : 5v

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

int main(void){
	setup();
	while(1) {
		SCH_Dispatch_Tasks();
	}
}

void setup(){
	init_connectie();
	init_adc();			// Setup the ADC
	init_USART();			// Setup the USART
	init_dist();
	init_scheduler();
}