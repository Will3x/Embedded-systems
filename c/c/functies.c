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

void USART_send(unsigned char data);    //Function that sends a char over the serial port
void USART_putstring(char* StringPtr);    //Function that sends a string over the serial port
unsigned char USART_receive(void);
void temperatuur();
void ldr();
void afstand();
void newRegel();
void upDown();
void goDown();
void goUp();
void afstandStil();
void test();
uint16_t read_adc(uint8_t channel);    //Function to read an arbitrary analogic channel/pin

void test(){
	char echodit[5];
	int a = USART_receive();
	itoa(a, echodit, 10);
	USART_putstring(echodit);
}

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
	adc_value = ((((double)adc_value)/1024)*100);
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
		SCH_Add_Task(goDown,0,1);	// warm/licht ga omlaag ROOD
	}
	else if((ls <= licht_down || ts <= temp_down) && !manual){
		SCH_Add_Task(goUp,0,1);				// koud/donker ga omhoog GROEN
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
void check_input(){
	if(recieve() == 0xff){
		int i = 0;
		while((i = recieve()) != 0) // wacht tot er nieuwe recieve gevonden is
		switch(i){
			case 0x01:
				USART_putstring(":1:");
				return;
			
			case 0x02:
				USART_putstring(":2:");
				return;
			
			case 0x03:
				USART_putstring(":3:");
				return;
			
			case 0x04:
				USART_putstring(":4:");
				return;
			
			case 0x05:
				USART_putstring(":5:");
				return;
			
			case 0x06:
				USART_putstring(":6:");
				return;
			
			case 0x07:
				USART_putstring(":7:");
				return;
			
			default:
				return;
				
			
		}
	}
	return;
	
	
	char data= USART_receive();
	char running = '0';
	char sluiten = '1';
	char openen = '2';
	USART_putstring("status: ");
	if(data == sluiten){USART_putstring("sluiten");}
	if(data == openen){USART_putstring("openen");}
	if(data == running){USART_putstring("running");}
	USART_putstring(" ");
}

void newRegel(){
	USART_send('\r');
	USART_send('\n');
}