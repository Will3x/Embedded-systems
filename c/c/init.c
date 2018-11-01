#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16000000UL
#include <util/delay.h>

#include "AVR_TTC_scheduler.h"
#include "main.h"
#include "functies.h"
#include "init.h"

#define BAUDRATE 9600
#define BAUD_PRESCALLER (((F_CPU / (BAUDRATE * 16UL))) - 1)

void init_connectie();		// Connection 
void init_adc();			// Function to initialize/configure the ADC
void init_USART();			// Function to initialize and configure the USART/serial
void init_dist();
void init_scheduler();

void init_connectie(){
	// disable U2X mode
	UCSR0A = 0;
	// Enable receiver and transmitter
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	/* Set frame format: 8data, 2stop bit */
	UCSR0C = (1<<USBS0)|(3<<UCSZ00);
}

void init_USART(){
	
	UBRR0H = (uint8_t)(BAUD_PRESCALLER>>8);
	UBRR0L = (uint8_t)(BAUD_PRESCALLER);
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	UCSR0C = (3<<UCSZ00);
}

void init_scheduler()
{
	SCH_Init_T1();
	SCH_Add_Task(temperatuur,0,1);	// moet 4000 worden@@@
	SCH_Add_Task(ldr,0,1);			// moet 3000 worden
	SCH_Add_Task(newRegel,0,1);	
	SCH_Start();
}

void init_adc(){
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));    //16Mhz/128 = 125Khz the ADC reference clock
	ADMUX |= (1<<REFS0);                //Voltage reference from Avcc (5v)
	ADCSRA |= (1<<ADEN);                //Turn on ADC
	ADCSRA |= (1<<ADSC);                //Do an initial conversion because this one is the slowest and to ensure that everything is up and running
}

void init_dist(){
	DDRD |= _BV(PD3); // Pin 3 Trigger Output
	DDRD &= ~_BV(PD4); // Pin 4 Echo Input
}