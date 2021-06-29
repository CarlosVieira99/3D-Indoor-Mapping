/*
  LIDAR.h - Library for using DRV8825 stepper driver.
  Created by Carlos Silva, May, 2020.
*/

#include "LIDAR.h"

const byte FIRMW_VERSION[4]     = {0x5A, 0x04, 0x01, 0x5F};
const byte SYS_RESET[4]         = {0x5A, 0x04, 0x02, 0x60};
const byte TRIG_DETECT[4]       = {0x5A, 0x04, 0x04, 0x62};
const byte REST_SETTINGS[4]     = {0x5A, 0x04, 0x10, 0x6E};
const byte SAVE_SETTINGS[4]     = {0x5A, 0x04, 0x11, 0x6F};
const byte OUT_CM[5]            = {0x5A, 0x05, 0x05, 0x01, 0x65};
const uint8_t OUT_MM[5]         = {0x5A, 0x05, 0x05, 0x06, 0x6A};
const uint8_t FRAME_RATE_MAX[6] = {0x5A, 0x06, 0x03, 0xE8, 0x03, 0x4E};
const byte OUT_DISABLE[5]       = {0x5A, 0x05, 0x07, 0x00, 0x66};
const byte OUT_ENABLE[5]        = {0x5A, 0x05, 0x07, 0x01, 0x67};

LIDAR::LIDAR()
{
}

// Start communication with LIDAR sensor and set distance output to mm (default cm)
void LIDAR::begin(int baudrate)
{
  Serial2.begin(baudrate, SERIAL_8N1, RXD2, TXD2);
  delay(2000);
  for(int i=0; i<=4; i++) Serial2.write(OUT_MM[i]);
  delay(2000);
}

void LIDAR::readData(void)
{
  uint8_t frame[TFMINI_FRAME_SIZE];

  Serial2.flush();
  while(!Serial2.available());
    if(Serial2.read() == 0x59)
    {
      if(Serial2.read() == 0x59)
      {
        for(int i=0; i<=6; i++)
        {
          frame[i] = Serial2.read();
        }

        uint16_t distData     = (frame[1] << 8) + frame[0];
        uint16_t strengthData = (frame[3] << 8) + frame[2];
        uint16_t celsiusData  = (frame[5] << 8) + frame[4];

        //This value is interpreted into the decimal value in the range of 0-12000.
        //When the signal strength is lower than 100, the detection is unreliable, 
        //TFmini-S will set distance value to -1
        _distance = int(distData);
        //Represents the signal strength with the default value in the rangeof 0-65535
        _strength = float(strengthData);
        //Represents the chip temperature of TFmini-S. Degree centigrade = Temp / 8 -256
        _celsius  = int(celsiusData)/8 - 256;
        
      }
    }
}

// Return distance value
float LIDAR::getDistance()
{
  return _distance;
}

// Return signal strength value
float LIDAR::getStrength(){
  return _strength;
}

// Return sensor temperature value
float LIDAR::getCelsius()
{
  return _celsius;
}
