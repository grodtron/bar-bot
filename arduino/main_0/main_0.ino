#include <Wire.h>
#include <Adafruit_NeoPixel.h>
#include "motor.h"
#include "led.h"

#define MSGSIZE 32
#define BOTTLESTEP_AMT 3333 //todo: change with calibration

enum CommunicationType{PouringRequest = 0, IdleRequest = 1, CommandAckRequest = 2, FaultRequest = 3};

//pouring mode
enum DispenseType{Shot = 0, FreePour = 1, NoPour = 2};
enum Rotation{CW = 0, CCW = 1, Quick = 2};

//fault request responses
enum FaultStatus{NoFaults = 0, BottleAlignment = 1, HookAlignment = 2};

bool readFlag;
bool requestFlag;
bool checkSumFlag;
uint8_t timeRemaining;
uint8_t msgBuffer[MSGSIZE];
uint8_t currentComState;
FaultStatus faultStatus;

//StepperMotor* stepper;
//LedStrip* strip;

//pin assignments
uint8_t stepPin = A2;
uint8_t ms1Pin = 11;
uint8_t ms2Pin = 12;
uint8_t ms3Pin = 13;
uint8_t dirPin = A3;
uint8_t enablePin = 10;
uint8_t resetPin = A0;

uint8_t ledCtrlPin = 6;

void setup(){
  readFlag = false;
  requestFlag = false;
  checkSumFlag = true;
  faultStatus = NoFaults;
  timeRemaining = 0;

  //I2C initialization
  Wire.begin(6);                
  Wire.onReceive(receiveEvent); 
  Wire.onRequest(requestEvent);

  //stepper motor initialization
  //stepper = new StepperMotor(stepPin, ms1Pin, ms2Pin, ms3Pin, dirPin, enablePin, resetPin);
  //stepper -> Initialize();

  //LED initialization
  //strip = new LedStrip(ledCtrlPin);
  //strip -> Initialize();

  Serial.begin(9600);           
  Serial.println("Connected"); 
}

void loop(){
	  	
	if(readFlag){
		Serial.println("In handling read..."); 
		Serial.print("Current com state: "); 
		Serial.println(currentComState); 

		//parse according to communication type
		switch(currentComState){
		case PouringRequest: 
			{
			Serial.println("In PouringRequest..."); 
			uint8_t x=1;
			uint8_t cmpCheckSum=0;
			uint8_t bottleNum, dispenseType, pourAmount, rotation, ledMode, ledColor, checkSum;
			bottleNum = msgBuffer[x++];
					Serial.print("bottleNum: "); 
					Serial.println(bottleNum);
			dispenseType = msgBuffer[x++];
					Serial.print("dispenseType: "); 
					Serial.println(dispenseType);
			pourAmount = msgBuffer[x++];
					Serial.print("pourAmount: "); 
					Serial.println(pourAmount);
			rotation = msgBuffer[x++];
					Serial.print("rotation: "); 
					Serial.println(rotation);
			ledMode = msgBuffer[x++];
					Serial.print("ledMode: "); 
					Serial.println(ledMode);
			ledColor = msgBuffer[x++];
					Serial.print("ledColor: "); 
					Serial.println(ledColor);
			checkSum = msgBuffer[x++];
					Serial.print("checkSum: "); 
					Serial.println(checkSum);

			for(int i=1; i < (x- 1); i++)
				cmpCheckSum ^= msgBuffer[i];
			
			Serial.print("Master checksum: "); 
			Serial.println(checkSum); 

			Serial.print("Client checksum: "); 
			Serial.println(cmpCheckSum); 

			if(cmpCheckSum == checkSum){
				//put everything else here
				//stepper->SetMotor(Fast, bottleNum * (5373/6),

				Serial.println("Checksum correct."); 
				
			}
			else{
				Serial.println("Checksum incorrect.");
				checkSumFlag = false;
			}
			break;
			}
		case IdleRequest: 
			Serial.println("In IdleRequest..."); 
			break;
		case CommandAckRequest:
			Serial.println("In CommandAckRequest..."); 
			break;
		case FaultRequest:
			Serial.println("In FaultRequest..."); 
			break;
		default: 
			Serial.println("In default..."); 
			break;
		}

		readFlag = false;
	}
	else{
	}


	delay(20);
}

void receiveEvent(int numBytes){
	if(!readFlag)
	{
		int i=0;
		while(Wire.available()){
			msgBuffer[i] = Wire.read();
			i++;
		}

		currentComState = msgBuffer[0];

		if(currentComState > IdleRequest){
			requestFlag = true;
			readFlag = false;
		}
		else{
			readFlag = true;
			checkSumFlag = true;
		}
	}	
}

void requestEvent(){
	Wire.write(22);

	if(requestFlag){ //redundant check

		switch(currentComState){
		case CommandAckRequest:
			if(!checkSumFlag){
				Wire.write(0);
				checkSumFlag = true;
			}
			else{
				timeRemaining += 1; //testing
				Wire.write(timeRemaining);
			}
			break;
		case FaultRequest:
			Wire.write(faultStatus);
			break;
		default:
			Wire.write(69);
			break;
		}		
	}
	else{ //temp testing to see if this gets called without receiveEvent firing
		Wire.write(33);
	}
	requestFlag = false;
}






