/*
 * serail.h
 *
 * Created: 8-11-2018 19:00:57
 *  Author: timgo
 */ 


#ifndef SERAIL_H_
#define SERAIL_H_

// Serial send/receive
void USART_send(unsigned char data);	// Sent a char over the serial port
void USART_putstring(char* StringPtr);	// Sent a String to the serial port
void newLine();							// Sent a new line
void check_input(unsigned char data);	// Checks the serial port on input
uint16_t read_adc(uint8_t channel);     // Function to read the analog pin(s)

#endif /* SERAIL_H_ */