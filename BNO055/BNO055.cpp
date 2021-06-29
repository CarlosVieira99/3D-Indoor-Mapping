/*
  BNO055.h - Library for using DRV8825 stepper driver.
  Created by Carlos Silva, May, 2020.
*/

#include "BNO055.h"

BNO055::BNO055()
{
}

// Define the I2C Address of the sensor
void BNO055::begin(uint8_t i2c_address)
{
  _ADDRESS = i2c_address;
}

/*
 * Read and Write process
 * 
 * The devide uses I2C or USART communication, the I2C will be used
 * 
 * Register write algorithm:
 * 1 - Begin transmission with the device
 * 2 - Write the address of the register
 * 3 - Write the value to the register
 * 4 - End transmission with the device
 * 
 * Single register read algorithm:
 * 1 - Begin transmission with the device
 * 2 - Write the address of the register
 * 3 - End transmission with the device
 * 4 - Begin transmission with the device
 * 5 - Read value of the register
 * 6 - End transmission
 *     Steps 4 to 6 can be simplified by a requestFrom() method
 * 
 * Multi register read algorithm (it increases register value at every read):
 * 1 - Begin transmission with the device
 * 2 - Write the address of the register
 * 3 - End transmission with the device
 * 4 - Begin transmission with the device
 * 5 - Read value of the register
 * 6 - End transmission
 *     Steps 4 to 6 can be simplified by a requestFrom() method
 */
 
bool BNO055::Register_Write(uint8_t reg, uint8_t value)
{
  Wire.beginTransmission(byte(_ADDRESS)); // Slave Address
  Wire.write(byte(reg));          // Register Address
  Wire.write(byte(value));
  Wire.endTransmission();
  return true;
}

byte BNO055::SingleRegister_Read(uint8_t reg)
{
  byte value = 0;
  Wire.beginTransmission(byte(_ADDRESS));
  Wire.write(byte(reg));
  Wire.endTransmission();
  Wire.requestFrom(byte(_ADDRESS), (byte)1);
  value = Wire.read();
  return value;
}

byte* BNO055::MultiRegister_Read(uint8_t reg, byte *arr, uint8_t len)
{
  uint8_t i;
  Wire.beginTransmission(byte(_ADDRESS));
  Wire.write(byte(reg));
  Wire.endTransmission();
  Wire.requestFrom(byte(_ADDRESS), byte(len));
  for (i = 0; i < len; i++) arr[i] = Wire.read();

  return arr;
}

float BNO055::RegisterPair(char regist)
{
  int16_t reading=0;
  byte arr[2]; 
  byte* ptr;
  
  ptr = MultiRegister_Read(regist, arr, 2);
  reading = ((uint16_t(ptr[1]) << 8) | uint16_t(ptr[0]));
  return float(reading);
}

/*
 * Check if any of the components of the device is damaged (not communicating)
 * Bit = 1 -> Component is okay
 * Bit = 0 -> Component is not okay
 * 
 * bit 0 - Accelerometer
 * bit 1 - Magnetometer
 * bit 2 - Gyroscope
 * bit 3 - Microcontroller
 */

byte BNO055::CheckStatus(void)
{
  // Power on test
  byte test = SingleRegister_Read(ST_RESULT);
  return test;
}

/*
 * Configure the device
 * 
 * 1 - Select units of measurement to use (check UNIT_SEL for more info)
 * 
 * Current Configuration:
 * Android Orientation Mode
 * Temperature - Celsius
 * Euler Angles - Degrees
 * Gyroscope - dps
 * Accelerometer - m/s²
 * 
 * 2 - Select Operating Mode
 * 
 * NDOF
 * Fusion mode with 9 degrees of freedom where the fused absolute orientation data is calculated  from:  
 * Accelerometer, gyroscope and magnetometer 
 * The  advantages  of combining all three sensors are:
 * Fast calculation, resulting in high output data rate, and high robustness from magnetic field distortions.   
 * 
 * 3 - Check if the components of the sensor are working
 * 
 * Accelerometer
 * Magnetometer
 * Gyroscope
 * Microcontroller
 */
 
void BNO055::Config(void)
{
  //Configuration of unit selection
  Register_Write(UNIT_SEL, 0x80);
  
  //Power-Mode normal pré-definido
  delay(1000);
  Register_Write(OPR_MODE, NDOF);
  delay(1000);

  CheckStatus();
}

/*
 * Calibration process
 * 
 * Accelerometer calibration:
 * - Put the device in 6 different stable positions
 * Gyroscope calibration:
 * - Hold the device stable
 * Magnetometer calibration:
 * - Make 8 shaped movements
 * System calibration:
 * - This is a combination of the calibration of all the components
 * 
 * Not calibrated value -> 0
 * Fully calibrated -> 3
 */

void BNO055::Calibrate(int *sys, int *gyr, int *acc, int *mag)
{
  byte calib = SingleRegister_Read(CALIB_STAT);
  
  *sys = (calib>>6) & 0x03;
  *gyr = (calib>>4) & 0x03;
  *acc = (calib>>2) & 0x03;
  *mag = calib & 0x03;
}

/*
 * Temperature from the accelerometer componenent
 * Can be changed to be read from the gyroscope component
 */

int BNO055::getTemp(void)
{
  byte temp = SingleRegister_Read(TEMP);
  return int(temp);
}

/*
 * Idenfitication values of each component:
 * Chip ID
 * Acelerometer ID
 * Magnetometer ID
 * Gyroscope ID
 */
 
void BNO055::getIDs(void)
{
  byte arr[4]; 
  byte* ptr = MultiRegister_Read(CHIP_ID, arr, 4);
  //Serial.print("Chip address: ");
  //Serial.println(ptr[0]);
  //Serial.print("Acelerometer address: ");
  //Serial.println(ptr[1]);
  //Serial.print("Magnetometer address: ");
  //Serial.println(ptr[2]);
  //Serial.print("Gyroscope address: ");
  //Serial.println(ptr[3]); 
}

/*
 * Read values from accelerometer (m/s)
 * It has 3 axis:
 * - X
 * - Y
 * - Z
 */

float BNO055::readACC(char axis)
{
  if(axis == 'x')       return RegisterPair(ACC_DATA_X_LSB)/100.0;
  else if(axis == 'y')  return RegisterPair(ACC_DATA_Y_LSB)/100.0;
  else if(axis == 'z')  return RegisterPair(ACC_DATA_Z_LSB)/100.0;
  //else Serial.println("Error ACC func!");
}

/*
 * Read values from gyroscope (rad/s)
 * It has 3 axis:
 * - X
 * - Y
 * - Z
 */

float BNO055::readGYR(char axis)
{
  if(axis == 'x')       return RegisterPair(GYR_DATA_X_LSB)/16.0;
  else if(axis == 'y')  return RegisterPair(GYR_DATA_Y_LSB)/16.0;
  else if(axis == 'z')  return RegisterPair(GYR_DATA_Z_LSB)/16.0;
  //else Serial.println("Error GYR func!");
}

/*
 * Read values from magnetometer (uTesla)
 * It has 3 axis:
 * - X
 * - Y
 * - Z
 */
 
float BNO055::readMAG(char axis)
{
  if(axis == 'x')       return RegisterPair(MAG_DATA_X_LSB)/16.0;
  else if(axis == 'y')  return RegisterPair(MAG_DATA_Y_LSB)/16.0;
  else if(axis == 'z')  return RegisterPair(MAG_DATA_Z_LSB)/16.0;
  //else Serial.println("Error MAG func!");
}

/*
 * Read values in Euler Angles
 * It has 3 axis:
 * - X
 * - Y
 * - Z
 */

float BNO055::readEUL(char axis)
{
  if(axis == 'x')       return RegisterPair(EUL_DATA_X_LSB)/16.0;
  else if(axis == 'y')  return RegisterPair(EUL_DATA_Y_LSB)/16.0;
  else if(axis == 'z')  return RegisterPair(EUL_DATA_Z_LSB)/16.0;
  //else Serial.println("Error EUL func!");
}

/*
 * Read values in Quaternions
 * It has 3 axis:
 * - X
 * - Y
 * - Z
 */

float BNO055::readQUA(char axis)
{
  const double scale = (1.0 / (1 << 14));
  if(axis == 'w')       return RegisterPair(QUA_DATA_W_LSB)*scale;
  else if(axis == 'x')  return RegisterPair(QUA_DATA_X_LSB)*scale;
  else if(axis == 'y')  return RegisterPair(QUA_DATA_Y_LSB)*scale;
  else if(axis == 'z')  return RegisterPair(QUA_DATA_Z_LSB)*scale;
  //else Serial.println("Error QUA func!");
}

/*
 * Read values in Linear Acceleration (without gravity component) (m/s)
 * It has 3 axis:
 * - X
 * - Y
 * - Z
 */

float BNO055::readLIA(char axis)
{
  if(axis == 'x')       return RegisterPair(LIA_DATA_X_LSB)/100.0;
  else if(axis == 'y')  return RegisterPair(LIA_DATA_Y_LSB)/100.0;
  else if(axis == 'z')  return RegisterPair(LIA_DATA_Z_LSB)/100.0;
  //else Serial.println("Error LIA func!");
}

/*
 * Read values in Gravity Vector (m/s^2)
 * It has 3 axis:
 * - X
 * - Y
 * - Z
 */

float BNO055::readGRV(char axis)
{
  if(axis == 'x')       return RegisterPair(GRV_DATA_X_LSB)/100.0;
  else if(axis == 'y')  return RegisterPair(GRV_DATA_Y_LSB)/100.0;
  else if(axis == 'z')  return RegisterPair(GRV_DATA_Z_LSB)/100.0;
  //else Serial.println("Error GRV func!");
}

/*
 * Read values in Gravity Vector (m/s^2)
 * It has 3 axis:
 * - X
 * - Y
 * - Z
*/
 
float BNO055::readQUA_EUL(char axis)
{
  float q0=0, q1=0, q2=0, q3=0;
  float roll=0, pitch=0, yaw=0;
  
  q0 = readQUA('w');
  q1 = readQUA('x');
  q2 = readQUA('y');
  q3 = readQUA('z');

  if(axis == 'x')
  {
    roll=-atan2(2*(q0*q1+q2*q3),1-2*(q1*q1+q2*q2));
    return roll;
  }
  else if(axis == 'y')
  {
    pitch=asin(2*(q0*q2-q3*q1));
    return pitch;
  }

  else if(axis == 'z')
  {
    yaw=atan2(2*(q0*q3+q1*q2), 1-2*(q2*q2+q3*q3));
    return yaw;
  }
}
