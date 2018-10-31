// A0 : TMP36 (middelste van de 3)
// A1 : LDR (min kant)
// A2 : Echo
// A3 : Trig
//
// TMP36 rechts = min en links is plus (platte kant voor)
// LDR plus aangesloten op 3,3 V
// VCC : 5v


#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16000000UL
#include <util/delay.h>

// distant zaken
#include <avr/interrupt.h>
int dist, d[4], c=0, t=0;
static volatile int pulse = 0;
static volatile int nummer = 0;

#define BAUDRATE 9600
#define BAUD_PRESCALLER (((F_CPU / (BAUDRATE * 16UL))) - 1)

uint16_t adc_value;            //Variable used to store the value read from the ADC
uint16_t adc_echo;            //Variable used to store the value read from the ADC
char buffer[5];                //Output of the itoa function
uint8_t i=0;                //Variable for the for() loop

void adc_init(void);            //Function to initialize/configure the ADC
uint16_t read_adc(uint8_t channel);    //Function to read an arbitrary analogic channel/pin
void USART_init(void);            //Function to initialize and configure the USART/serial
void USART_send( unsigned char data);    //Function that sends a char over the serial port
void USART_putstring(char* StringPtr);    //Function that sends a string over the serial port
void temperatuur(void);
void ldr(void);
void afstand(void);
void dist_init(void);

void dist_init(void){
	MCUCR |= (1 << ISC00);
	sei(); // interupt aanzetten
}
ISR(INT0_vect){ // interupt service routine
	if (nummer == 1){
		TCCR1B = 0;
		pulse = TCNT1;
		TCNT1 = 0;
		i = 0;
	}
	if (nummer == 0){
		TCCR1B |= 1<<CS10; // start de counter van de microcontroller. prescaler 1
		nummer = 1;
	}
}
int main(void){
	dist_init();
	adc_init();        //Setup the ADC
	USART_init();        //Setup the USART
	// disable U2X mode
	UCSR0A = 0;
	// Enable receiver and transmitter
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	/* Set frame format: 8data, 2stop bit */
	UCSR0C = (1<<USBS0)|(3<<UCSZ00);
	
	int16_t count_a = 0;
	char show_a[16];
	DDRD = 0b11111011;
	_delay_ms(50);
	
	// echo = INT0
	// TRIGGER = DP0
	while(1){
		PORTD |= (1<< PIND0);
		_delay_ms(15); //dit geeft dus een puls van 15ms naar pind0
		PORTD &= ~(1 << PIND0);
		count_a = pulse/58;
		itoa(count_a, show_a, 10);
		USART_putstring(show_a);
		USART_putstring(" cm");
		USART_send('\r');
		USART_send('\n');
	}
	while(1){        //Our infinite loop
		temperatuur();
		ldr();
		afstand();
		
		USART_send('\r');
		USART_send('\n');                //This two lines are to tell to the terminal to change line
	}
}

void temperatuur(void){
	USART_putstring("Temp : ");
	adc_value = read_adc(0);
	adc_value = (((((double)adc_value / 1024) * 5) - 0.5) * 100); // graden celsius
	itoa(adc_value, buffer, 10);        //Convert the read value to an ascii string
	USART_putstring(buffer);        //Send the converted value to the terminal
	
	//Some more formatting
	USART_putstring("  ");  //You can tweak this value to have slower or faster readings or for max speed remove this line
}

void ldr(void){ // licht sensor
	USART_putstring("LDR : ");
	adc_value = read_adc(1);
	itoa(adc_value, buffer, 10);        //Convert the read value to an ascii string
	USART_putstring(buffer);        //Send the converted value to the terminal
	
	//Some more formatting
	USART_putstring("  ");  //You can tweak this value to have slower or faster readings or for max speed remove this line
}

void afstand(void){ // hc-sr04
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
	USART_putstring("  ");  //You can tweak this value to have slower or faster readings or for max speed remove this line
}

void adc_init(void){
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));    //16Mhz/128 = 125Khz the ADC reference clock
	ADMUX |= (1<<REFS0);                //Voltage reference from Avcc (5v)
	ADCSRA |= (1<<ADEN);                //Turn on ADC
	ADCSRA |= (1<<ADSC);                //Do an initial conversion because this one is the slowest and to ensure that everything is up and running
}

uint16_t read_adc(uint8_t channel){
	ADMUX &= 0xF0;                    //Clear the older channel that was read
	ADMUX |= channel;                //Defines the new ADC channel to be read
	ADCSRA |= (1<<ADSC);                //Starts a new conversion
	while(ADCSRA & (1<<ADSC));            //Wait until the conversion is done
	return ADCW;                    //Returns the ADC value of the chosen channel
}

void USART_init(void){
	
	UBRR0H = (uint8_t)(BAUD_PRESCALLER>>8);
	UBRR0L = (uint8_t)(BAUD_PRESCALLER);
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	UCSR0C = (3<<UCSZ00);
}

void USART_send( unsigned char data){
	
	while(!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
	
}

void USART_putstring(char* StringPtr){
	
	while(*StringPtr != 0x00){
		USART_send(*StringPtr);
	StringPtr++;}
	
}