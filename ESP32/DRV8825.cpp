/*
  DRV8825.h - Library for using DRV8825 stepper driver.
  Created by Carlos Silva, May, 2020.
*/

#include "DRV8825.h"

DRV8825::DRV8825()
{
}

// Configure the pins connected to the driver
void DRV8825::begin(int enablePin, int dirPin, int stepPin, int M0, int M1, int M2)
{
  _enablePin = enablePin;
  _dirPin = dirPin;
  _dir = LOW;
  _stepPin = stepPin;
  _M0 = M0;
  _M1 = M1;
  _M2 = M2;

  pinMode(_enablePin, OUTPUT);
  digitalWrite(_enablePin, HIGH);
  pinMode(_dirPin, OUTPUT);
  digitalWrite(_dirPin, _dir);
  pinMode(_stepPin, OUTPUT);
  pinMode(_M0, OUTPUT);
  pinMode(_M1, OUTPUT);
  pinMode(_M2, OUTPUT);
}

/*
 * Set step-mode of the driver, options:
 * 1/1  STEP
 * 1/2  STEP
 * 1/4  STEP
 * 1/8  STEP
 * 1/16 STEP
 * 1/32 STEP
 */

void DRV8825::setMode(int steps)
{
  switch (steps){
    case 1:
      digitalWrite(_M0, LOW);
      digitalWrite(_M1, LOW);
      digitalWrite(_M2, LOW);
      break;

    case 2:
      digitalWrite(_M0, HIGH);
      digitalWrite(_M1, LOW);
      digitalWrite(_M2, LOW);
      break;

    case 4:
      digitalWrite(_M0, LOW);
      digitalWrite(_M1, HIGH);
      digitalWrite(_M2, LOW);
      break;

    case 8:
      digitalWrite(_M0, HIGH);
      digitalWrite(_M1, HIGH);
      digitalWrite(_M2, LOW);
      break;

    case 16:
      digitalWrite(_M0, LOW);
      digitalWrite(_M1, LOW);
      digitalWrite(_M2, HIGH);
      break;

    case 32:
      digitalWrite(_M0, HIGH);
      digitalWrite(_M1, LOW);
      digitalWrite(_M2, HIGH);
      break;

    default:
      break;
  }
}

// Send pulse to the driver to take one step in the current step-mode
void DRV8825::takeStep()
{
  digitalWrite(_stepPin, HIGH);
  delayMicroseconds(PULSE_DELAY);
  digitalWrite(_stepPin, LOW);
}

// Change the direction of the steps in the current step-mode
void DRV8825::changeDir()
{
  _dir = !_dir;
  digitalWrite(_dirPin, _dir);
}
