#include <Wire.h>

int sensor = 9;
long unsigned t = millis();
void setup()
{
  Wire.begin(4);
  Wire.onRequest(requestEvent);
  Serial.begin(9600);
 
}

void loop()
{   
    if (millis()-t > 100);
    {
      sensor = 9;
      t = millis();
    
    }
    int sensorValue0 = analogRead(A0);
    int sensorValue1 = analogRead(A1);
    int sensorValue2 = analogRead(A2);
    float voltage0= sensorValue0 * (5.0 / 1023.0);
    float voltage1= sensorValue1 * (5.0 / 1023.0);
    float voltage2= sensorValue2 * (5.0 / 1023.0);
    if (voltage0 > 4)
    {
      Serial.print("A");
      Serial.println(voltage0);
      sensor = 1;
    }
     if (voltage1 > 4.5)
    {
      Serial.print("B");
      Serial.println(voltage1);
      sensor = 2;
    }
     if (voltage2 > 4.9)
    {
      Serial.print("C");
      Serial.println(voltage2);
      sensor = 3;
    }
}

void requestEvent() 
{
  Wire.write(sensor);
  sensor = 9;
}


