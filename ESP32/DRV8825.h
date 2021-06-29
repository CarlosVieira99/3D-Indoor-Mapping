/*
  DRV8825.h - Library for using DRV8825 stepper driver.
  Created by Carlos Silva, May, 2020.
*/

#include <Arduino.h>

//#define PULSE_DELAY 500
#define PULSE_DELAY 5

class DRV8825
{
  public:
    DRV8825();
    void begin(int enablePin, int dirPin, int stepPin, int M0, int M1, int M2);
    void setMode(int steps);
    void takeStep();
    void changeDir();
    
  private:
    int _enablePin;
    int _dirPin;
    bool _dir;
    int _stepPin;
    int _M0;
    int _M1;
    int _M2;
};
