/*
  LIDAR.h - Library for using TFmini-S Lidar distance sensor.
  Created by Carlos Silva, May, 2020.
*/

#include "Arduino.h"

#define RXD2 16
#define TXD2 17

// Defines
#define LIDAR_BAUDRATE   115200

// The frame size is nominally 9 characters, 
// but we don't include the first two 0x59's marking the start of the frame
#define TFMINI_FRAME_SIZE                 7

// Timeouts
#define TFMINI_MAXBYTESBEFOREHEADER       30
#define TFMINI_MAX_MEASUREMENT_ATTEMPTS   10

// States
#define READY                             0
#define ERROR_SERIAL_NOHEADER             1
#define ERROR_SERIAL_BADCHECKSUM          2
#define ERROR_SERIAL_TOOMANYTRIES         3
#define MEASUREMENT_OK                    10

class LIDAR {
  public:
    //Constructor
    LIDAR();

    //Methods
    void  readData(void);
    void  begin(int baudrate=LIDAR_BAUDRATE);
    float getDistance();
    float getStrength();
    float getCelsius();

  private:
    float _distance, _strength, _celsius;
};
