#include <Wire.h>

int n = 10;

void setup()
{
  Wire.begin();
  Serial.begin(9600);
}

void loop()
{
  if (Serial.available() > 0) {
    n = Serial.parseInt();
    
    Serial.println(n);
    
    Serial.print(F("beginning transmission to feeder  ")); 
    Serial.println(n);
    Wire.beginTransmission(n);
    Serial.println(F("Transmission accomplished"));

    Serial.println(F("writing to feeder"));
    Wire.write(2);
    Serial.println(F("writing done"));
    Serial.println(F("Now ending transmission"));
    Wire.endTransmission();
    Serial.println(F("Transmission ended"));
  }
}



