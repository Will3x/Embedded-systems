#include <avr/io.h>
#include <stdlib.h>
#include <stdio.h>
#define F_CPU 16000000UL
#include <util/delay.h>
#include <avr/interrupt.h>

#include "AVR_TTC_scheduler.h"
#include "main.h"
#include "functies.h"
#include "init.h"

// variables
uint16_t adc_value;						// Reads the ADC value
uint16_t adc_echo;						// Reads the ADC echo
char temp_sensor[5];					// Value of the temperature sensor
char LDR_sensor[5];						// Value of LDR
char distance_sensor[5];				// Value of distance sensor
int temp_down = 24;						// Temperature at which the sunshade closes
int temp_up = 16;						// Temperature at which the sunshade opens
int LDR_down = 60;						// Level of light at which the sunshade closes
int LDR_up = 16;						// Level of light at which the sunshade opens
int distance_up = 20;					// Distance at which the sunshade opens
int distance_down = 5;					// Distance at which the sunshade closes
int distance_manual = 20;				// Manual set distance at which the sunshade closes
int manual = 0;							// if manual is 1 manual mode is enabled
int teller = 0;



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

uint16_t read_adc(uint8_t channel)
{
	ADMUX &= 0xF0;                    //Clear the older channel that was read
	ADMUX |= channel;                 //Defines the new ADC channel to be read
	ADCSRA |= (1<<ADSC);              //Starts a new conversion
	while(ADCSRA & (1<<ADSC));        //Wait until the conversion is done
	return ADCW;                      //Returns the ADC value of the chosen channel
}

void temperature()
{
	USART_putstring("Temp : ");
	adc_value = read_adc(0);
	adc_value = (((((double)adc_value / 1024) * 5) - 0.5) * 100); // Calculate temperature
	itoa(adc_value, temp_sensor, 10);							  //Convert the read value to an ascii string
	USART_putstring(temp_sensor);								  //Send the converted value to the terminal
	USART_putstring("  ");
}

void ldr()
{
	USART_putstring("LDR : ");
	adc_value = read_adc(1);
	adc_value = ((((double)adc_value)/1024)*100 *1.5);			  // Calculate the amount of light
	itoa(adc_value, LDR_sensor, 10);							  // Convert the read value to an ascii string
	USART_putstring(LDR_sensor);								  // Send the converted value to the terminal
	USART_putstring("  ");
}

void distance()
{
	USART_putstring("distance : ");
	PORTD |= _BV(PD3);
	_delay_us(10);
	PORTD &= ~_BV(PD3);
	
	loop_until_bit_is_set(PIND, PD2);
	TCNT1 = 0;
	loop_until_bit_is_clear(PIND, PD2);
	uint16_t count = TCNT1;
	float distance = ((float)count / 4);		// Calculate the distance

	itoa(distance, distance_sensor, 10);        // Convert the read value to an ascii string
	USART_putstring(distance_sensor);			// Send the converted value to the terminal
	USART_putstring("  ");
}

void distanceStill()
{
	PORTD |= _BV(PD3);
	_delay_us(10);								
	PORTD &= ~_BV(PD3);
	loop_until_bit_is_set(PIND, PD2);
	TCNT1 = 0;
	loop_until_bit_is_clear(PIND, PD2);
	uint16_t count = TCNT1;
	float distance = ((float)count / 4);		// Calculate the distance
	itoa(distance, distance_sensor, 10);        // Convert the read value to an ASCII string
}

// Red = pb0 : Down
// Yellow = pb1 : Yellow/moving
// Green = pb2 : Up

void upDown()
{
	int ls = atoi(LDR_sensor);					// Convert light sensor value to int and set ls
	int ts = atoi(temp_sensor);					// Convert temperature sensor value to int and set ts
	distanceStill();							// Get distance
	int as = atoi(distance_sensor);				// Convert distance sensor value to int
	distance_up = distance_manual;				// Set distance_up to the value the user inputs in manual mode
	
	if(((ls >= LDR_down || ts >= temp_down) && !manual) || ((as > (distance_manual+1)) && manual))
	{
		PORTB &= ~(1 << PB2);					// Green LED off
		PORTB |= (1 << PB0);					// Red LED on
			
		if (as > distance_down)
		{
			PORTB |= (1 << PB1);
			_delay_ms(100);
			PORTB &= ~(1 << PB1);
			_delay_ms(100);
		}
	}
	else if(((ls <= LDR_up || ts <= temp_up) && !manual) || ((as < (distance_manual-1)) && manual))
	{
		PORTB &= ~(1 << PB0);					// Red LED off
		PORTB |= (1 << PB2);					// Green LED on
			
		if (as < distance_up)
		{
			PORTB |= (1 << PB1);
			_delay_ms(100);
			PORTB &= ~(1 << PB1);
			_delay_ms(100);
		}
	}
}

void newLine()
{
	USART_send('\r');
	USART_send('\n');
}

int unsigned combine(unsigned x, unsigned y)
{
	x -= 48;
	y -= 48;
	unsigned pow = 10;
	return (y * pow) + x;
}

int unsigned combine3(unsigned x, unsigned y, unsigned z)
{
	x -= 48;
	y -= 48;
	z -= 48;
	unsigned pow1 = 10;
	unsigned pow2 = 100;
	return (z * pow2) + (y * pow1) + x;
}

ISR ( USART_RX_vect )
{
	unsigned char ReceivedByte;
	ReceivedByte = UDR0 ;						// Set ReceivedByte to the received byte from the controller (GUI)
	
	switch(ReceivedByte)
	{
		case '1':								// 1 = Shut the sunshade // Red
			manual = 1;
			distance_manual = 5;
			return;
			
		case '2':								// 2 = Open the sunshade // Green
			manual = 1;
			distance_manual = 10;
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
			int closeopen = combine3((int) USART_receive(), (int) USART_receive(), (int) USART_receive());
			distance_manual = closeopen;
			return;
			
		case '8':								// 8 = set manual
			manual = (int) USART_receive();
			if (manual == 1)
			{
				distance_manual = (int) atoi(distance_sensor);
			return;
			}
		default:
			return;
	}
}