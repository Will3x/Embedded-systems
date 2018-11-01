#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16000000UL
#include <util/delay.h>

#include "AVR_TTC_scheduler.h"
#include "main.h"
#include "functies.h"
#include "init.h"

// variables
uint16_t adc_value;            //Variable used to store the value read from the ADC
uint16_t adc_echo;            //Variable used to store the value read from the ADC
char buffer[5];                //Output of the itoa function

void USART_send(unsigned char data);    //Function that sends a char over the serial port
void USART_putstring(char* StringPtr);    //Function that sends a string over the serial port
void temperatuur();
void ldr();
void afstand();
void newRegel();
uint16_t read_adc(uint8_t channel);    //Function to read an arbitrary analogic channel/pin


void USART_send(unsigned char data){
	while(!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
}

void USART_putstring(char* StringPtr){
	while(*StringPtr != 0x00){
		USART_send(*StringPtr);
	StringPtr++;}
}

uint16_t read_adc(uint8_t channel){
	ADMUX &= 0xF0;                    //Clear the older channel that was read
	ADMUX |= channel;                //Defines the new ADC channel to be read
	ADCSRA |= (1<<ADSC);                //Starts a new conversion
	while(ADCSRA & (1<<ADSC));            //Wait until the conversion is done
	return ADCW;                    //Returns the ADC value of the chosen channel
}

void temperatuur(){
	USART_putstring("Temp : ");
	adc_value = read_adc(0);
	adc_value = (((((double)adc_value / 1024) * 5) - 0.5) * 100); // graden celsius
	itoa(adc_value, buffer, 10);        //Convert the read value to an ascii string
	USART_putstring(buffer);        //Send the converted value to the terminal
	
	//Some more formatting
	USART_putstring("  "); 
}

void ldr(){ // licht sensor
	USART_putstring("LDR : ");
	adc_value = read_adc(1);
	adc_value = ((((double)adc_value)/1024)*100);
	itoa(adc_value, buffer, 10);        //Convert the read value to an ascii string
	USART_putstring(buffer);        //Send the converted value to the terminal
	
	//Some more formatting
	USART_putstring("  ");  
}

void afstand(){ // hc-sr04
	USART_putstring("Echo : "); // ontvangt het signaal
	adc_value = read_adc(2);
	itoa(adc_value, buffer, 10);        //Convert the read value to an ascii string
	USART_putstring(buffer);
	USART_putstring("  ");
	
	USART_putstring("Trig : "); // deze verstuurd een signaal (10us HIGH pulse)
	adc_echo = read_adc(3);
	itoa(adc_echo, buffer, 10);        //Convert the read value to an ascii string
	USART_putstring(buffer);        //Send the converted value to the terminal
	
	//Some more formatting
	USART_putstring("  "); 
}

void newRegel(){
	USART_send('\r');
	USART_send('\n');
}