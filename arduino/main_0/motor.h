#ifndef MOTOR_H
#define MOTOR_H
#include <Arduino.h>
#include <stdint.h>

#define MICROS_MAX 4200000000

enum Direction{Clockwise, CounterClockwise};
enum StepType{Full, Half, Quarter, Eighth, Sixteenth};
enum StepSpeed{Slow, Medium, Fast};

class StepperMotor {

  private:
	//control pins
	uint8_t stepPin;
	uint8_t ms1Pin, ms2Pin, ms3Pin;
	uint8_t dirPin, enablePin, resetPin;
	uint32_t prevTime, currTime;

	void busyWait(uint32_t waitTime);

  public:
    StepperMotor(uint8_t _stepPin, uint8_t _ms1Pin,
				uint8_t _ms2Pin, uint8_t _ms3Pin, uint8_t _dirPin,
				uint8_t _enablePin, uint8_t _resetPin );
	void Initialize();
	void SetMotor(uint8_t speed, uint16_t numSteps, uint8_t sType, uint8_t dir);
};

#endif
