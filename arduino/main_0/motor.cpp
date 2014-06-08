#include "motor.h"

StepperMotor::StepperMotor (uint8_t _stepPin, uint8_t _ms1Pin,
				uint8_t _ms2Pin, uint8_t _ms3Pin, uint8_t _dirPin,
				uint8_t _enablePin, uint8_t _resetPin ): 
					stepPin(_stepPin), ms1Pin(ms1Pin), ms2Pin(_ms2Pin), ms3Pin(_ms3Pin), dirPin(_dirPin),
						enablePin(_enablePin), resetPin(_resetPin) {}

void StepperMotor::Initialize()
{
	//pin directions
	 pinMode(stepPin, OUTPUT);
	 pinMode(ms1Pin, OUTPUT);
	 pinMode(ms2Pin, OUTPUT);
	 pinMode(ms3Pin, OUTPUT);
	 pinMode(dirPin, OUTPUT);
	 pinMode(resetPin, OUTPUT);
	 pinMode(enablePin, OUTPUT);
 
	 //initial pin states
	 digitalWrite(enablePin, LOW);
	 digitalWrite(resetPin, HIGH);
	 digitalWrite(ms1Pin, LOW);
	 digitalWrite(ms2Pin, LOW);
	 digitalWrite(ms3Pin, LOW);
}

void StepperMotor::SetMotor(uint8_t speed, uint16_t numSteps, uint8_t sType, uint8_t dir){
	//delay in microseconds between step transitions - half the period
	uint32_t halfPeriod = 0;

	//set direction
	digitalWrite(dirPin, dir);
		
	//extensibility? probably always using full steps ie. ms1=ms2=ms3=LOW
	switch(sType){
	case Half:
		digitalWrite(ms1Pin, HIGH);
		digitalWrite(ms2Pin, LOW);
		digitalWrite(ms3Pin, LOW);
		break;
	case Full:
		digitalWrite(ms1Pin, LOW);
		digitalWrite(ms2Pin, LOW);
		digitalWrite(ms3Pin, LOW);
		break;
	}
	
	//set (half) period amount depending on speed
	switch(speed){
	case Slow: halfPeriod = 1000; //500 Hz
		break;
	case Medium: halfPeriod = 500; //1 kHz
		break;
	case Fast: halfPeriod = 333; //~3 kHz
		break;
	default: halfPeriod = 500;
	}
	
	for(int i = 0; i < numSteps; i++){

		digitalWrite(stepPin, LOW);
		busyWait(halfPeriod);

		digitalWrite(stepPin, HIGH);
		busyWait(halfPeriod);
	}
}

void StepperMotor::busyWait(uint32_t waitTime){
	uint32_t elapsed = 0;
	prevTime = micros();
		
	while(elapsed < waitTime){
		currTime = micros();
			
		if(currTime < prevTime){
			//handle counter reset ~ every 70 minutes
			elapsed = currTime + (MICROS_MAX - prevTime); 
		}
		else if (currTime == prevTime){
			//unlikely
			elapsed = 0;
		}
		else{
			//normal case
			elapsed = currTime - prevTime;	
		}
	    //todo: add small delay here to avoid spin?
	}
}







