/*
 * functies.h
 *
 * Created: 1-11-2018 12:50:13
 *  Author: Wouter
 */ 


#ifndef FUNCTIES_H_
#define FUNCTIES_H_

// Sunshade
void upDown();							// Opens and closes the sunshade
ISR ( USART_RX_vect );					// Enables the ISR

// Variables
uint16_t adc_value;						// Reads the ADC value
uint16_t adc_echo;						// Reads the ADC echo
char temp_sensor[5];					// Value of the temperature sensor
char LDR_sensor[5];						// Value of LDR
char distance_sensor[10];				// Value of distance sensor


#endif /* FUNCTIES_H_ */