#include <stdlib.h>
#define F_CPU 16000000UL
#include <util/delay.h>
#include <avr/interrupt.h>

#include "sunshade.h"
#include "sensors.h"
#include "serial.h"

// variables
uint16_t adc_value;						// Reads the ADC value
uint16_t adc_echo;						// Reads the ADC echo
char temp_sensor[5];					// Value of the temperature sensor
char LDR_sensor[5];						// Value of LDR
char distance_sensor[10];				// Value of distance sensor

int temp_down = 24;						// Temperature at which the sunshade closes
int temp_up = 16;						// Temperature at which the sunshade opens
int LDR_down = 60;						// Level of light at which the sunshade closes
int LDR_up = 16;						// Level of light at which the sunshade opens
int distance_up = 40;					// Distance at which the sunshade opens
int distance_down = 5;					// Distance at which the sunshade closes
int distance_manual = 40;				// Manual set distance at which the sunshade closes
int onoff = 0;							// Check if open or close is pressed in manual mode
int manual = 0;							// if manual is 1 manual mode is enabled
int middle = 1;							// 0 = red AND 1 = Green


// Red = pb0 : Down
// Yellow = pb1 : Yellow/moving
// Green = pb2 : Up

void upDown()
{
	int ls = atoi(LDR_sensor);					// Convert light sensor value to int and set ls
	int ts = atoi(temp_sensor);					// Convert temperature sensor value to int and set ts
	distanceStill();							// Get distance
	int as = atoi(distance_sensor);				// Convert distance sensor value to int
	//distance_up = distance_manual;				// Set distance_up to the value the user inputs in manual mode
	
	if(((ls >= LDR_down || ts >= temp_down) && !manual) || ( !distance_manual && onoff && manual)) // Go down as > (distance_manual+1)) &&
	{
		PORTB &= ~(1 << PB2);					// Green LED off
		PORTB |= (1 << PB0);					// Red LED on
		middle = 0;
		
		if (as > distance_down)					// Makes yellow LED blink
		{
			PORTB |= (1 << PB1);
			_delay_ms(100);
			PORTB &= ~(1 << PB1);
			_delay_ms(100);						
		}
	}
	else if(((ls <= LDR_up || ts <= temp_up) && !manual) || ( distance_manual && onoff && manual)) // Go up as < (distance_manual-1)) && 
	{
		PORTB &= ~(1 << PB0);					// Red LED off
		PORTB |= (1 << PB2);					// Green LED on
		middle = 1;
			
		if (as < distance_up)					// Makes yellow LED blink
		{
			PORTB |= (1 << PB1);
			_delay_ms(100);
			PORTB &= ~(1 << PB1);
			_delay_ms(100);
		}
	}
	else if(!manual){ // midden klasse
		if(middle && as < distance_up){ // = 1 Green
			PORTB |= (1 << PB1);
			_delay_ms(100);
			PORTB &= ~(1 << PB1);
			_delay_ms(100);
		}
		else if(!middle && as > distance_down){ // = 0 Red
			PORTB |= (1 << PB1);
			_delay_ms(100);
			PORTB &= ~(1 << PB1);
			_delay_ms(100);
		}
	}
}


int unsigned combine(unsigned x, unsigned y)
{
	unsigned pow = 10;
	return (y * pow) + x;
}

int unsigned combine3(unsigned x, unsigned y, unsigned z)
{
	unsigned pow1 = 10;
	unsigned pow2 = 100;
	return (z * pow2) + (y * pow1) + x;
}

ISR ( USART_RX_vect )
{
	unsigned char ReceivedByte;
	ReceivedByte = UDR0;						// Set ReceivedByte to the received byte from the controller (GUI)
	
	switch(ReceivedByte)
	{
		case '1':								// 1 = Shut the sunshade // Red
			manual = 1;
			onoff = 1;
			distance_manual = 0;
			return;
			
		case '2':								// 2 = Open the sunshade // Green
			manual = 1;
			onoff = 1;
			distance_manual = 1;
			return;
			
		case '3':								// 3 = set
			manual = 0;
			temp_down = combine((int) USART_receive(), (int) USART_receive());
			temp_up = combine((int) USART_receive(), (int) USART_receive());
			LDR_down = combine((int) USART_receive(), (int) USART_receive());
			LDR_up = combine((int) USART_receive(), (int) USART_receive());
			return;
			
		case '7':								// 7 = open/closing distance
			manual = 1;
			onoff = 0;
			int closeopen = combine3((int) USART_receive(), (int) USART_receive(), (int) USART_receive());
			distance_up = closeopen;
			return;
			
		case '8':								// 8 = set manual ON / OFF
			onoff = 0;
			manual = (int) USART_receive();		// 1/0
			if (manual == 1)					// manual mode on
			{
				distance_manual = (int)atoi(distance_sensor);
			}
			return;
		
		default:
			return;
	}
}