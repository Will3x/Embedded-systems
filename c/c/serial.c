/*
 * CFile1.c
 *
 * Created: 8-11-2018 19:00:28
 *  Author: timgo
 */ 

#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16000000UL
#include <util/delay.h>

#include "AVR_TTC_scheduler.h"
#include "main.h"
#include "sunshade.h"
#include "init.h"
#include "sensors.h"
#include "serial.h"

unsigned char USART_receive(void)
{
	while(!(UCSR0A & (1<<RXC0)));
	return UDR0;
}

void USART_send(unsigned char data)
{
	while(!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
}

void USART_putstring(char* StringPtr)
{
	while(*StringPtr != 0x00){
		USART_send(*StringPtr);
	StringPtr++;}
}

void newLine()
{
	USART_send('\r');
	USART_send('\n');
}

uint16_t read_adc(uint8_t channel)
{
	ADMUX &= 0xF0;                    //Clear the older channel that was read
	ADMUX |= channel;                 //Defines the new ADC channel to be read
	ADCSRA |= (1<<ADSC);              //Starts a new conversion
	while(ADCSRA & (1<<ADSC));        //Wait until the conversion is done
	return ADCW;                      //Returns the ADC value of the chosen channel
}