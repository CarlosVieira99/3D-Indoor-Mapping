/*
  3D LIDAR Indoor Mapping

  The goal of this software is to send data about the exact coordinates
  of a 3 dimentional point in space and send it via Wifi Sockets
  
  The circuit:
  * ESP32 Microcontroller
  * BNO055 9-Axis IMU
  * TFmini-S Lidar TOF Distance Sensor
  * DRV8825 Stepper Motor Driver 1/32 Max MicroStep

  Created [February-June] 2020
  By Carlos Silva 1160628@isep.ipp.pt
*/

// Libraries
#include "DRV8825.h"
#include "LIDAR.h"
#include "BNO055.h"
#include <WiFi.h>

// Hardware objects
LIDAR tfmini;
BNO055 imu;
DRV8825 baseStepper;
DRV8825 sideStepper;

// Motor Pre-definitions
#define ANGLE_PER_STEP 1.8
int step_mode = 1;
int timeStep = 25000;  //25 ms

//Pin Interrupts
portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;
int SW_B = 34;
int SW_S = 35;
volatile bool SW_B_Flag = false;
volatile bool SW_S_Flag = false;

// Timer Interrupts
volatile bool stepperFlag = false;
hw_timer_t * timer = NULL;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

// Wifi settings
WiFiClient client;
const char* ssid;
const char* password;
uint16_t port;
const char * host;

// Pin Interrupts Functions
void IRAM_ATTR end_B() {
  portENTER_CRITICAL(&mux);
  SW_B_Flag=true;
  portEXIT_CRITICAL(&mux);
}
void IRAM_ATTR end_S() {
  portENTER_CRITICAL(&mux);
  SW_S_Flag=true;
  portEXIT_CRITICAL(&mux);
}

// Timer Interrupts Functions
void IRAM_ATTR onTimer() {
  portENTER_CRITICAL_ISR(&timerMux);
  stepperFlag = true;
  portEXIT_CRITICAL_ISR(&timerMux);
}

// Semaphore of the stepper motors, to give them time to lock in place
void waitStepTime(void){
  while(!stepperFlag);
  portENTER_CRITICAL(&timerMux);
  stepperFlag = false;
  portEXIT_CRITICAL(&timerMux);

  timer = timerBegin(0, 80, true); // Pre-scaler divide by 80, so it will be 1MHz
  timerAttachInterrupt(timer, &onTimer, true);
  timerAlarmWrite(timer, timeStep/step_mode, true);
  timerAlarmEnable(timer);
}

// Homing of the scanner
void homing() {
  while(!SW_B_Flag){
    waitStepTime();
    baseStepper.takeStep();
  }
  while(!SW_S_Flag){
    waitStepTime();
    sideStepper.takeStep();
  }

  portENTER_CRITICAL(&mux);
  SW_B_Flag=false;
  portEXIT_CRITICAL(&mux);
  portENTER_CRITICAL(&mux);
  SW_S_Flag=false;
  portEXIT_CRITICAL(&mux);

  waitStepTime();
  sideStepper.changeDir();

  // 116 was an experimental taken value
  for(int sal=0; sal<116; sal++)
  {
    waitStepTime();
    sideStepper.takeStep();
  }
  waitStepTime();
  sideStepper.changeDir();
  baseStepper.changeDir();
}

// Send the Status of the IMU
void sendCheckStatus()
{
  byte statusRes;
  statusRes = imu.CheckStatus();
  
  // Accelerometer Test
  if(bitRead(statusRes, 0))   client.print("ACC_OK");
  else                        client.print("ACC_NOK");

  while(!client.available());
  while(client.available()) client.read();
  
  // Magnetometer Test
  if(bitRead(statusRes, 1))   client.print("MAG_OK");
  else                        client.print("MAG_NOK");

  while(!client.available());
  while(client.available()) client.read();
  
  // Gyroscope Test
  if(bitRead(statusRes, 2))   client.print("GYR_OK");
  else                        client.print("GYR_NOK");

  while(!client.available());
  while(client.available()) client.read();
  
  // Microcontroller Test
  if(bitRead(statusRes, 3))   client.print("MIC_OK");
  else                        client.print("MIC_NOK");

  while(!client.available());
  while(client.available()) client.read();
}

// Send the calibration of the IMU
void sendCalibration()
{
  int sys, gyr, acc, mag;
  String out;

  while(true)
  {
    imu.Calibrate(&sys, &gyr, &acc, &mag);
  
    out = String(sys) + " " + String(gyr) + " " + String(acc) + " " + String(mag);
    client.print(out);
    
    while(!client.available())
    {
      if(!client.connected())
        {
          client.stop();
          ESP.restart();
        }
    }
    while(client.available())
    {
      if(client.read() == 'S') 
      {
        client.print("END_CALIBRATE");
        return;
      }
    }
  }
}

// North Pole scan of the room
void scan()
{
  // -----------------------
 
    float sideStepper_dir = 1; // float type to be compatible with float operations
    float baseStepper_dir = 1; // float type to be compatible with float operations

    float dtheta = float((float(ANGLE_PER_STEP)/float(step_mode)))*PI/180.0; 
    float dphi = dtheta;

    float theta = 0.0;  // rad
    float phi = 0.0;    // rad

    int N = (100*step_mode);  // Number of steps for the base motor
    int M = (100*step_mode);  // Number of steps for the side motor

    // -----------------------

    // Lidar Sensor Variables
    float dist;                 // Distance in mm
    float strength;             // Strength of the signal
    float celsius;              // Temperature of the sensor

    // Lidar tries to measure distance
    int i;
  
    // Quaternions of the IMU Sensor
    float q0, q1, q2, q3;
  
    // Data sent to the Server
    float pointX, pointY, pointZ;
    String dataPoints;
    
  /*
   * This loop will scan top sphere
   * 
   * Algorithm for the motors movement:
   * 1 - Side Stepper Motor (Pitch Control) goes back 180 degrees
   *     100 is 50% of 200 full-steps (full rotation) so it's 180 degrees
   *
   * 2 - Base Stepper Motor (Yaw Control) takes one step
   *     50 is 25% of 200 full-steps (full rotation) so it's 90 degrees
   *     
   * 3 - Side Stepper Motor goes forward 180 degrees
   * 
   * This goes one until the Base Stepper has completed 360 degrees
   */
   
  for(int baseStep=0; baseStep < N; baseStep++)
  {
    for(int sideStep=0; sideStep <= M; sideStep++)
    { 
      /*
       * Get the distance value from LIDAR (in mm)
       * Also possible to get strength of the signal and sensor temperature values
       * Filter non usable data (out of range) 100mm - 12000mm
       */
      i=0;
      do{
        tfmini.readData();
        dist = float(tfmini.getDistance());
 
        i++;
        if(i==5){
          dist = 0;
          break;
        }
        strength = tfmini.getStrength();
        celsius  = tfmini.getCelsius();
      } while(dist<100 && dist>12000);

      // Get the euler angles (in radians) converted from quaternions from the IMU
      q0  = imu.readQUA('w');
      q1  = imu.readQUA('x');
      q2  = imu.readQUA('y');
      q3  = imu.readQUA('z');

      // Send data to the server separated by blank spaces
      // Tempo, theta, phi, dist, strength, temp, roll_imu, pitch_imu, yaw_imu
      dataPoints  = String(millis());
      dataPoints += " " + String(theta, 10) + " " + String(phi, 10);
      dataPoints += " " + String(dist)  + " " + String(strength)  + " " + String(celsius); 
      dataPoints += " " + String(q0)    + " " + String(q1)        + " " + String(q2)        + " " + String(q3);
      client.print(dataPoints);

      // Restart the microcontroller in case the connection is lost
      while(!client.available())
      {
        if(!client.connected())
        {
          client.stop();
          ESP.restart();
        }
      }

      // Wait for client message
      while(client.available())
        { // Read ACK and clear input buffer
          if(client.read() == 'S') // Cancel scan
              return; 
        }

      // Don't take the last step
      if(sideStep != M)
    {
      // Go to the next position
      waitStepTime();
      sideStepper.takeStep();
      phi += sideStepper_dir*dphi;
    }
      
    }
    
    // Correct point cloud offset
    waitStepTime();
    sideStepper.changeDir();
    sideStepper_dir *= -1;
//    for(int k = 0; k<step_mode; k++)
//    {
//      waitStepTime();
//      sideStepper.takeStep();
//      waitStepTime();
//      sideStepper.takeStep();
//    }

    waitStepTime();
    baseStepper.takeStep();
    waitStepTime();
    theta += baseStepper_dir*dtheta;
  }
  client.print("END_SCAN");
}

void setup() {
  String ssid_data, pwd_data, port_data, host_data;
  int i = 0;
  
  // Start serial communcation for debug purposes
  Serial.begin(115200);
  while(!Serial);

  // Limit switches setup
  pinMode(SW_B, INPUT);
  pinMode(SW_S, INPUT);
  attachInterrupt(digitalPinToInterrupt(SW_B), end_B, RISING);
  attachInterrupt(digitalPinToInterrupt(SW_S), end_S, RISING);

  // Stepper Motor Drivers Configuration
  sideStepper.begin(14, 13, 23, 4, 18, 19);   //  enablePin, dirPin, stepPin, M0, M1, M2
  sideStepper.setMode(step_mode);               
  baseStepper.begin(12, 32, 33, 27, 26, 25);  //  enablePin, dirPin, stepPin, M0, M1, M2
  baseStepper.setMode(step_mode);

  // Lidar Sensor Configuration
  tfmini.begin(115200);

  // IMU Configuration and Calibration
  Wire.begin();
  imu.begin(0x28);
  imu.Config();

  // Timer setup
  timer = timerBegin(0, 80, true); // Pre-scaler divide by 80, so it will be 1MHz
  timerAttachInterrupt(timer, &onTimer, true);
  timerAlarmWrite(timer, timeStep/step_mode, true);
  timerAlarmEnable(timer);
  
  homing();
  //timeStep = 15000;  //15 ms
  //timeStep = 200000;
  
  /*
   * Converts the contents of a String as a C-style, null-terminated string.
   * Note that this gives direct access to the internal String buffer and 
   * should be used with care. In particular, you should never modify the string 
   * through the pointer returned. When you modify the String object, or when it 
   * is destroyed, any pointer previously returned by c_str() becomes invalid and 
   * should not be used any longer.
   */
   
  while(true)
  {
    if(Serial.available())
    { 
      if(i==0)
      {
        ssid_data = Serial.readString();
        ssid = ssid_data.c_str();
        Serial.println("SSID_OK");
      }
      else if(i==1)
      {
        pwd_data = Serial.readString();
        password = pwd_data.c_str();
        Serial.println("PWD_OK");
      }
      else if(i==2)
      {
        host_data = Serial.readString();
        host = host_data.c_str();
        Serial.println("HOST_OK");
      }
      else if(i==3)
      {
        port_data = Serial.readString();
        port = port_data.toInt();
        Serial.println("PORT_OK");
        break;
      }
      i++;
    }
  }
 
  // Wifi Configuration
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  i=0;
  while (WiFi.status() != WL_CONNECTED){
    if(i == 5) 
    {
      Serial.println("CONNECTION_NOK");
      ESP.restart();
    }
    delay(1000);
    i++;
  }
  Serial.println("CONNECTION_OK");
  Serial.println(WiFi.localIP());
  while(!client.connect(host, port));
  Serial.println("CONNECTION_OK");
}

void loop() {
  String temp="";
  char msg;

  // Restart the microcontroller in case the connection is lost
  while(!client.available()){
    if(!client.connected()){
      client.print("Disconnect");
      client.stop();
      ESP.restart();
    }
  }

  // Read message
  while(client.available()>0){
    msg = client.read();
    temp = temp + msg;
  }

  // Message reading and actuation
  switch (temp[0]) {
  // IMU
  case 'I':
    // Check Status
    if(temp[1] == 'S') sendCheckStatus();
    // Calibrate
    else if(temp[1] == 'C') sendCalibration();
    break;
  // Motors
  case 'M':
     // Full Step
    if(temp[1] == 'F')      step_mode = 1;
     // Half Step
    else if(temp[1] == 'H') step_mode = 2;
     // Quarter Step
    else if(temp[1] == 'Q') step_mode = 4;
     // Eight Step
    else if(temp[1] == 'E') step_mode = 8;
     // Sixteenth Step
    else if(temp[1] == 'S') step_mode = 16;
     // Thirty-Second Step
    else if(temp[1] == 'T') step_mode = 32;

    // Update step mode of the drivers
    sideStepper.setMode(step_mode);
    baseStepper.setMode(step_mode);

    // Update timer setup
    timer = timerBegin(0, 80, true); // Pre-sclaer divide by 80, so it will be 1MHz
    timerAttachInterrupt(timer, &onTimer, true);
    timerAlarmWrite(timer, timeStep/step_mode, true); // 100ms
    timerAlarmEnable(timer);
  
    client.print("MOTORS_CHANGED");
    break;
    
  // Start the Scan
  case 'S':
    scan();
    break;
  // Disconnection from the server
  case 'D':
    client.print("DISCONNECTED");
    client.stop();
    ESP.restart();
    break;
  default:
    // statements
    break;
  }
}
