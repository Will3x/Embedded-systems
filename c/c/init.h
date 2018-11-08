/*
 * init.h
 *
 * Created: 1-11-2018 12:46:36
 *  Author: Wouter
 */ 


#ifndef INIT_H_
#define INIT_H_

void init_connectie();					// Connection
void init_adc();						// Function to initialize/configure the ADC
void init_USART();						// Function to initialize/configure the USART/serial
void init_dist();						// Function to initialize/configure the distance sensor
void init_scheduler();					// Function to initialize and add all the tasks to the scheduler
void init_LEDS();						// Function to initialize/configure the LED's


#endif /* INIT_H_ */