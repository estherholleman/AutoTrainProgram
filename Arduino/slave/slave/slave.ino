
#include <Wire.h>

const int sensor1 = A0;  
const int sensor2 = A1;
const int sensor3 = A2;

int sensor = 9;

int sensor1Value = 0;
int sensor2Value = 0;
int sensor3Value = 0;

void setup() {  
  Wire.begin(4);
  Wire.onRequest(requestEvent);
  Serial.begin(9600);
}


void loop() {

  sensor1Value = analogRead(sensor1);
  sensor2Value = analogRead(sensor2);
  sensor3Value = analogRead(sensor3);
  
   if (sensor1Value < 150){
         //Serial.println("Nosepoke Sensor triggered!");
         sensor = 1;
   }
   
   if (sensor2Value < 150){
         //Serial.println("Apple Sensor triggered!");
         sensor = 2;
   }

   if (sensor3Value < 150){
         //Serial.println("Bacon Sensor triggered");
         sensor = 3;
   }
     
 }
 
 
void requestEvent() 
{
  Wire.write(sensor);
  sensor = 9;
}
