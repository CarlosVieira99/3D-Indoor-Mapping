#include "LIDAR.h"

LIDAR tfmini;

void setup() {
  Serial.begin(115200);
  while(!Serial);
  tfmini.begin(115200);
}

void loop() {
  float dist, strength;

  for(int i=0; i<50; i++)
  {
    tfmini.readData();
    dist = float(tfmini.getDistance());
    strength = float(tfmini.getStrength());
  
    Serial.print(dist); Serial.print(','); Serial.println(strength); 
    //delay(10);
  }

  while(!Serial.available());
  Serial.read();

    //tfmini.readData();
    //dist = float(tfmini.getDistance());
    //strength = float(tfmini.getStrength());
    //Serial.print("Distancia: "); Serial.print(dist);
    //Serial.print(" Forca: "); Serial.println(strength);

    //delay(100);
}
