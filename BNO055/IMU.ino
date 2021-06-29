#include "BNO055.h"
BNO055 imu;

void sendCheckStatus()
{
  byte statusRes;
  statusRes = imu.CheckStatus();
  
  // Accelerometer Test
  if(bitRead(statusRes, 0))   Serial.print("ACC_OK");
  else                        Serial.print("ACC_NOK");
  
  // Magnetometer Test
  if(bitRead(statusRes, 1))   Serial.print("MAG_OK");
  else                        Serial.print("MAG_NOK");
  
  // Gyroscope Test
  if(bitRead(statusRes, 2))   Serial.print("GYR_OK");
  else                        Serial.print("GYR_NOK");
  
  // Microcontroller Test
  if(bitRead(statusRes, 3))   Serial.print("MIC_OK");
  else                        Serial.print("MIC_NOK");
}

void sendCalibration()
{
  int sys, gyr, acc, mag;
  String out;

  while(true)
  {
    imu.Calibrate(&sys, &gyr, &acc, &mag);
  
    out = String(sys) + " " + String(gyr) + " " + String(acc) + " " + String(mag);
    Serial.print(out);

    delay(10);
    if(Serial.available())
    {
      Serial.read();
      break;
    }
  }
}

float radian2deg(float radian)
{
  return (radian*180/PI);
}

void setup() {
  Serial.begin(115200);
  while(!Serial);
  // IMU Configuration and Calibration
  Wire.begin();
  imu.begin(0x28);
  imu.Config();

  sendCalibration();
}

void loop() {
  // put your main code here, to run repeatedly:
  float roll, pitch, yaw, roll2, pitch2, yaw2;
  float x, y, z;

  //x = imu.readACC('x');
  //y = imu.readACC('y');
  //z = imu.readACC('z');
  
  //x = imu.readGYR('x');
  //y = imu.readGYR('y');
  //z = imu.readGYR('z');
  
  x = imu.readMAG('x');
  y = imu.readMAG('y');
  z = imu.readMAG('z');

  //x = imu.readLIA('x');
  //y = imu.readLIA('y');
  //z = imu.readLIA('z');

  //x = imu.readGRV('x');
  //y = imu.readGRV('y');
  //z = imu.readGRV('z');

  //roll  = imu.readEUL('x');
  //pitch = imu.readEUL('z');
  //yaw   = imu.readEUL('y');

  //roll  = imu.readQUA('x');
  //pitch = imu.readQUA('y');
  //yaw   = imu.readQUA('z');

  //roll2  = imu.readQUA_EUL('z')*-1;
  //pitch2 = imu.readQUA_EUL('x');
  //yaw2   = imu.readQUA_EUL('y')*-1;

  //roll2  = radian2deg(roll2);
  //pitch2 = radian2deg(pitch2);
  //yaw2   = radian2deg(yaw2);

  //psi = atan2(Ym, Xm)/(2*3.14)*360;
  
  Serial.print(millis()); Serial.print(',');
  Serial.print(x); Serial.print(','); Serial.print(y); Serial.print(','); Serial.println(z);
  //Serial.print(roll); Serial.print(','); Serial.print(pitch); Serial.print(','); Serial.print(yaw);
  //Serial.print(','); Serial.print(roll2); Serial.print(','); Serial.print(pitch2); Serial.print(','); Serial.println(yaw2);
  delay(10);
}
