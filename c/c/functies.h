/*
 * functies.h
 *
 * Created: 1-11-2018 12:50:13
 *  Author: Wouter
 */ 


#ifndef FUNCTIES_H_
#define FUNCTIES_H_

// Serial send/receive
void USART_send(unsigned char data);	// Sent a char over the serial port
void USART_putstring(char* StringPtr);	// Sent a String to the serial port
void newLine();							// Sent a new line
void check_input(unsigned char data);	// Checks the serial port on input
uint16_t read_adc(uint8_t channel);     // Function to read the analog pin(s)

// Sensors
void temperature();						// Read the temperature sensor
void ldr();								// Read the light sensor
void distance();						// Read the distance sensor

// Sunshade
void upDown();							// Opens and closes the sunshade
void manual_off();						// Manual mode on/off
void distanceStill();					// Checks if the shade is moving
ISR ( USART_RX_vect );					// Enables the ISR

// Variables
uint16_t adc_value;						// Reads the ADC value
uint16_t adc_echo;						// Reads the ADC echo
char temp_sensor[5];					// Value of the temperature sensor
char LDR_sensor[5];						// Value of LDR
char distance_sensor[5];				// Value of distance sensor
int temp_down;						// Temperature at which the sunshade closes
int temp_up;						// Temperature at which the sunshade opens
int LDR_down;						// Level of light at which the sunshade closes
int LDR_up;						// Level of light at which the sunshade opens
int distance_up;					// Distance at which the sunshade opens
int distance_down;					// Distance at which the sunshade closes
int distance_manual;				// Manual set distance at which the sunshade closes
int manual;							// if manual is 1 manual mode is enabled
int teller;
#endif /* FUNCTIES_H_ */