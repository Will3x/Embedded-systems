/*
 * functies.h
 *
 * Created: 1-11-2018 12:50:13
 *  Author: Wouter
 */ 


#ifndef FUNCTIES_H_
#define FUNCTIES_H_

void USART_send(unsigned char data);  
void USART_putstring(char* StringPtr);
unsigned char USART_receive(void);
void temperatuur();
void ldr();
void afstand();
void newRegel();
void upDown();
void goDown();
void goUp();
void check_input();
void test();
uint16_t read_adc(uint8_t channel);



#endif /* FUNCTIES_H_ */