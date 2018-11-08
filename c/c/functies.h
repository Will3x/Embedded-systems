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

#endif /* FUNCTIES_H_ */