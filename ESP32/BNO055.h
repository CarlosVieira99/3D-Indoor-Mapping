/*
  BNO055.h Library for using DRV8825 stepper driver.
  Created by Carlos Silva, May, 2020.
*/

#include "Arduino.h"
#include <Wire.h>

// Setup
//#define ADDRESS 0x28
#define PWR_MODE 0x3E
#define UNIT_SEL 0x3B
#define REFRESH_RATE 50

// Operation Mode
#define OPR_MODE 0x3D
#define CONFIGMODE 0x00
#define ACCONLY 0x01
#define MAGONLY 0x02
#define GYROONLY 0x03
#define ACCMAG 0x04
#define ACCGYRO 0x05
#define MAGGYRO 0x06
#define AMG 0x07
#define IMU 0x08
#define COMPASS 0x09
#define M4G 0x0A
#define NDOF_FMC_OFF 0x0B
#define NDOF 0x0C

// Chip ID's
#define CHIP_ID 0x00
#define ACC_ID 0x01
#define MAG_ID 0x02
#define GYR_ID 0x03

// Accelerometer (default m/s^2)
#define ACC_Config 0x08
#define ACC_DATA_X_LSB 0x08
#define ACC_DATA_X_MSB 0x09
#define ACC_DATA_Y_LSB 0x0A
#define ACC_DATA_Y_MSB 0x0B
#define ACC_DATA_Z_LSB 0x0C
#define ACC_DATA_Z_MSB 0x0D

// Magnetometer (uTesla)
#define MAG_Config 0x09
#define MAG_DATA_X_LSB 0x0E
#define MAG_DATA_X_MSB 0x0F
#define MAG_DATA_Y_LSB 0x10
#define MAG_DATA_Y_MSB 0x11
#define MAG_DATA_Z_LSB 0x12
#define MAG_DATA_Z_MSB 0x13

// Gyroscope (default dps)
#define GYR_Config_0 0x0A
#define GYR_Config_1 0x0B
#define GYR_DATA_X_LSB 0x14
#define GYR_DATA_X_MSB 0x15
#define GYR_DATA_Y_LSB 0x16
#define GYR_DATA_Y_MSB 0x17
#define GYR_DATA_Z_LSB 0x18
#define GYR_DATA_Z_MSB 0x19

// Euler Angles (default degrees)
#define EUL_DATA_X_LSB 0x1A
#define EUL_DATA_X_MSB 0x1B
#define EUL_DATA_Y_LSB 0x1C
#define EUL_DATA_Y_MSB 0x1D
#define EUL_DATA_Z_LSB 0x1E
#define EUL_DATA_Z_MSB 0x1F

//Quaternions (quaternion units)
#define QUA_DATA_W_LSB 0x20
#define QUA_DATA_W_MSB 0x21
#define QUA_DATA_X_LSB 0x22
#define QUA_DATA_X_MSB 0x23
#define QUA_DATA_Y_LSB 0x24
#define QUA_DATA_Y_MSB 0x25
#define QUA_DATA_Z_LSB 0x26
#define QUA_DATA_Z_MSB 0x27

// Linear Acceleration
#define LIA_DATA_X_LSB 0x28
#define LIA_DATA_X_MSB 0x29
#define LIA_DATA_Y_LSB 0x2A
#define LIA_DATA_Y_MSB 0x2B
#define LIA_DATA_Z_LSB 0x2C
#define LIA_DATA_Z_MSB 0x2D

// Gravity Vector
#define GRV_DATA_X_LSB 0x2E
#define GRV_DATA_X_MSB 0x2F
#define GRV_DATA_Y_LSB 0x30
#define GRV_DATA_Y_MSB 0x31
#define GRV_DATA_Z_LSB 0x32
#define GRV_DATA_Z_MSB 0x33

// Temperature (default celsius)
#define TEMP 0x34
#define TEMP_SOURCE 0x40

// Calibration
#define CALIB_STAT 0x35

// Power On Self Test Result
#define ST_RESULT 0x36

class BNO055 {
  public:
    //Constructor
    BNO055();

    //Methods
    void  begin(uint8_t i2c_address);
    bool  Register_Write(uint8_t reg, uint8_t value);
    byte  SingleRegister_Read(uint8_t reg);
    byte* MultiRegister_Read(uint8_t reg, byte *arr, uint8_t len);
    float RegisterPair(char regist);
    byte  CheckStatus(void);
    void  Config(void);
    void  Calibrate(int *sys, int *gyr, int *acc, int *mag);
    int   getTemp(void);
    void  getIDs(byte *chip_add, byte *acce_add, byte *magn_add, byte *gyro_add);
    float readACC(char axis);
    float readGYR(char axis);
    float readMAG(char axis);
    float readEUL(char axis);
    float readQUA(char axis);
    float readLIA(char axis);
    float readGRV(char axis);
    float readQUA_EUL(char axis);

  private:
    uint8_t _ADDRESS;
};
