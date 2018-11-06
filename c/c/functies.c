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
uint16_t adc_value;            //Variable used to store the value read from the ADC
uint16_t adc_echo;            //Variable used to store the value read from the ADC
char temp_sensor[5];                //Output of the itoa function
char licht_sensor[5];
char afstand_sensor[5];
int temp_up = 22;
int temp_down = 18;
int licht_up = 40;
int licht_down = 10;
int afstand_up = 10;
int afstand_down = 5;
int manual = 0;		// 1 is manual aan
int teller = 0;

void USART_send(unsigned char data);    //Function that sends a char over the serial port
void USART_putstring(char* StringPtr);    //Function that sends a string over the serial port
void temperatuur();
void ldr();
void afstand();
void newRegel();
void upDown();
void goDown();
void goUp();
void afstandStil();
void manual_uit();
void check_input(unsigned char data);
ISR ( USART_RX_vect );
uint16_t read_adc(uint8_t channel);    //Function to read an arbitrary analogic channel/pin


unsigned char USART_receive(void){
	while(!(UCSR0A & (1<<RXC0)));
	return UDR0;
}

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
	itoa(adc_value, temp_sensor, 10);        //Convert the read value to an ascii string
	USART_putstring(temp_sensor);        //Send the converted value to the terminal
	
	//Some more formatting
	USART_putstring("  ");
}

void ldr(){ // licht sensor
	USART_putstring("LDR : ");
	adc_value = read_adc(1);
	adc_value = ((((double)adc_value)/1024)*100 *1.5);
	itoa(adc_value, licht_sensor, 10);        //Convert the read value to an ascii string
	USART_putstring(licht_sensor);        //Send the converted value to the terminal
	
	//Some more formatting
	USART_putstring("  ");
}

void afstand(){ // hc-sr04
	USART_putstring("Afstand : ");
	PORTD |= _BV(PD3);
	_delay_us(10);
	PORTD &= ~_BV(PD3);

	loop_until_bit_is_set(PIND, PD2);
	TCNT1 = 0;
	//PORTB |= _BV(PB3);
	loop_until_bit_is_clear(PIND, PD2);
	//PORTB &= ~_BV(PB3);
	uint16_t count = TCNT1;
	//transmit(count);
	float distance = ((float)count / 4);
	
	itoa(distance, afstand_sensor, 10);        //Convert the read value to an ascii string
	USART_putstring(afstand_sensor);        //Send the converted value to the terminal
	
	//Some more formatting
	USART_putstring("  ");
}

void afstandStil(){ // hc-sr04
	PORTD |= _BV(PD3);
	_delay_us(10);
	PORTD &= ~_BV(PD3);

	loop_until_bit_is_set(PIND, PD2);
	TCNT1 = 0;
	//PORTB |= _BV(PB3);
	loop_until_bit_is_clear(PIND, PD2);
	//PORTB &= ~_BV(PB3);
	uint16_t count = TCNT1;
	//transmit(count);
	float distance = ((float)count / 4);
	
	itoa(distance, afstand_sensor, 10);        //Convert the read value to an ascii string
}

// rood = pb0 : hij is beneden
// geel = pb1 : proces naar beneden gaan knipperend lampje
// groe = pb2 : hij is omhoog
void upDown(){
	int ls = 0;	// licht sensor
	int ts = 0;	// temperatuur sensor
	for (int i = 0; i < 10; i++){
		ls = ls + atoi(licht_sensor); // maakt er int van en stopt het bij ls
		ts = ts + atoi(temp_sensor);
	}
	ls = ls / 10;
	ts = ts / 10;
	if((ls >= licht_up || ts >= temp_up) && !manual){
		goDown();				// warm/licht ga omlaag ROOD
	}
	else if((ls <= licht_down || ts <= temp_down) && !manual){
		goUp();					// koud/donker ga omhoog GROEN
	}
}

void goDown(){
	int as = atoi(afstand_sensor);	// afstand sensor wordt int
	PORTB &= ~(1 << PB2); // groen lampje uit
	if (as > afstand_down){
		PORTB |= (1 << PB0); // rood lampje aan
		_delay_ms(100);
		PORTB |= (1 << PB1); // geel lampje aan
		_delay_ms(100);
		PORTB &= ~(1 << PB1); // geel lampje uit
		
		afstandStil();
		as = atoi(afstand_sensor);
	}
	PORTB |= (1 << PB0); // rood lampje aan
}

void goUp(){
	int as = atoi(afstand_sensor);	// afstand sensor wordt int
	PORTB &= ~(1 << PB0); // rood lampje uit
	if (as < afstand_up){
		PORTB |= (1 << PB2); // groen lampje aan
		_delay_ms(100);
		PORTB |= (1 << PB1); // geel lampje aan
		_delay_ms(100);
		PORTB &= ~(1 << PB1); // geel lampje uit
		
		afstandStil();
		as = atoi(afstand_sensor);
	}
	PORTB |= (1 << PB2); // groen lampje aan
}

void manual_uit(){
	manual = 1;
	afstand_up = 20;
	afstand_down = 5;
}

void check_input(unsigned char data){
	USART_putstring(" jeej functie! ");
	// USART_receive();
	
}

void newRegel(){
	USART_send('\r');
	USART_send('\n');
}

ISR ( USART_RX_vect ){
	unsigned char ReceivedByte;
	ReceivedByte = UDR0 ; // Fetch the received byte value into the variable " ByteReceived "
	
	switch(ReceivedByte){
		// 1 = rolluik uitrollen
		case '1':
			manual = 1;
			goUp();
			return;
			
		// 2 = rolluik oprollen
		case '2':
			manual = 1;
			goDown();
			return;
			
		// 3 = uitrol temp grens
		case '3':
			manual_uit();
			temp_down = USART_receive();
			return;
			
		// 4 = uitrol licht grens
		case '4':
			manual_uit();
			licht_down = USART_receive();
			return;
			
		// 5 = oprol temp grens
		case '5':
			manual_uit();
			temp_up = USART_receive();
			return;
			
		// 6 = oprol licht grens
		case '6':
			manual_uit();
			licht_up = USART_receive();
			return;
			
		// 7 = uit-/oprol afstand
		case '7':
			manual = 1;
			int uitoprol = USART_receive();
			afstand_up = uitoprol;
			afstand_down = uitoprol;
			goDown();
			return;
			
		// 8 = set manual
		case '8':
			manual = 1;
			return;
			
		default:
		return;
	}
}