/*
 * sensors.c
 *
 * Created: 8-11-2018 18:06:25
 *  Author: Wouter
 */ 
#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16000000UL
#include <util/delay.h>

#include "sunshade.h"
#include "sensors.h"
#include "serial.h"

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
	OCR1A = 0x640;								// Max length = 400 cm * 4 = Dec.1600 == Hex 640
	USART_putstring("distance : ");
	PORTD |= _BV(PD3);
	_delay_us(10);
	PORTD &= ~_BV(PD3);							// Give pulse from 10ms
	
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
	OCR1A = 0x640;								// Max length = 400 cm * 4 = Dec.1600 == Hex 640
	
	PORTD |= _BV(PD3);
	_delay_us(10);
	PORTD &= ~_BV(PD3);							// Give pulse from 10ms
	loop_until_bit_is_set(PIND, PD2);
	TCNT1 = 0;
	loop_until_bit_is_clear(PIND, PD2);
	uint16_t count = TCNT1;
	float distance = ((float)count / 4);		// Calculate the distance
	itoa(distance, distance_sensor, 10);        // Convert the read value to an ASCII string
}