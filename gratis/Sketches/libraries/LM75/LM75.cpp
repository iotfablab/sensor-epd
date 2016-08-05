
#include <Arduino.h>
#include <Wire.h>

#include "LM75.h"


// LM75 address
#define LM75_ADDR  0x49

// Registers in the LM75
#define LM75_TEMP_REGISTER  0
#define LM75_CONF_REGISTER  1
#define LM75_THYST_REGISTER 2
#define LM75_TOS_REGISTER   3

// the default Temperature device
LM75_Class LM75(LM75_ADDR);


LM75_Class::LM75_Class(int addr) : address(addr) {
}


// initialise the i2c bus
void LM75_Class::begin() {
	// make sure sensor is not in shutdown mode
	Wire.beginTransmission(address);
	Wire.write(LM75_CONF_REGISTER);
	Wire.write(0<<0);
	Wire.endTransmission();	
}


void LM75_Class::end() {
	// put sensor in shutdown mode
	Wire.beginTransmission(address);
	Wire.write(LM75_CONF_REGISTER);
	Wire.write(1<<0);
	Wire.endTransmission();	
}

// return temperature as integer in Celsius
int LM75_Class::read() {
	Wire.beginTransmission(address);
	Wire.write(LM75_TEMP_REGISTER);
	Wire.endTransmission();
	
	Wire.requestFrom(address, 2);
	word regdata = (Wire.read() << 8) | Wire.read();
	
	// lower 5 bits are not used
	regdata = regdata >> 5;
	
	// sign extend negative numbers
	if (regdata & (1<<10)) {
		regdata |= 0xFC00;
	}
	
	// return the temperature in C
	return regdata / 8;
}
