#include <avr/io.h>
#include <stdlib.h>
#include <avr/interrupt.h>

#define F_CPU 16000000UL
#include <util/delay.h>

#include "AVR_TTC_scheduler.h"
#include "main.h"
#include "functies.h"
#include "init.h"

#define BAUDRATE 9600
#define BAUD_PRESCALLER (((F_CPU / (BAUDRATE * 16UL))) - 1)

void init_connectie()
{
	UCSR0A = 0;							// disable U2X mode
	UCSR0C = (1<<USBS0)|(3<<UCSZ00);	// Set frame format: 8data, 2stop bit 
}

void init_USART()
{
	UBRR0H = (uint8_t)(BAUD_PRESCALLER>>8);
	UBRR0L = (uint8_t)(BAUD_PRESCALLER);
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);		// Enable receiver and transmitter
	UCSR0C = (3<<UCSZ00);
	UCSR0B |= (1 << RXCIE0 );			// Enable the USART Receive Complete interrupt ( USART_RXC )
	sei ();								// Enable the Global Interrupt Enable flag so that interrupts can be processed
}

void init_scheduler()
{
	SCH_Init_T1();
	SCH_Add_Task(temperature,1,100);
	SCH_Add_Task(ldr,2,100);
	SCH_Add_Task(distance,3,100);
	SCH_Add_Task(newLine,6,100);
	SCH_Add_Task(upDown,8,20);
	SCH_Start();
}

void init_adc()
{
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));    //16Mhz/128 = 125Khz the ADC reference clock
	ADMUX |= (1<<REFS0);							 //Voltage reference from AVCC (5v)
	ADCSRA |= (1<<ADEN);							 //Turn on ADC
	ADCSRA |= (1<<ADSC);							 //Do an initial conversion because this one is the slowest and to ensure that everything is up and running
}

void init_dist()
{
	DDRD |= _BV(PD3);			// Pin 3 Trigger Output
	DDRD &= ~_BV(PD2);			// Pin 2 Echo Input
}

void init_LEDS()
{ 
	DDRB |= _BV(PB0);			// pin0 B = output
	DDRB |= _BV(PB1);			// pin1 B = output
	DDRB |= _BV(PB2);			// pin2 B = output
	PORTB |= (1 << PB2);		// Green LED on
}