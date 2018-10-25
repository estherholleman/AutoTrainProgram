#include <Servo.h>
#include <Wire.h> //for i2c (communication)library
Servo s;
int n = 0; //counter for number of motor turns
int spd = 0; //msg to start motor
int give = 0; //msg sent from master containing amount of reward
int incomingByte = 0;
int one;
int two;
int total;
unsigned long int t; // will be used to store time


void setup() {
  Serial.begin(9600); //baud rate/speed of communication
  s.attach(9);
  Serial.println(F("servo attached"));
  s.write(90);
  Serial.println(F("Set servo to 90 degrees"));
  pinMode(13, OUTPUT);
  Serial.println(F("about to execute wire.begin"));
  Wire.begin(2); //join serial bus with address 2
  Serial.println(F("wire.begin executed"));
  Serial.println(F("waiting to recieve event"));
  Wire.onReceive(receiveEvent);
  Serial.println(F("event recieved"));
}

void receiveEvent(int bytes) {
  Serial.println(bytes);
  Serial.println(F("About to read wire"));
  give = Wire.read();    // read one character from the I2C
  Serial.println(F("wire read"));
  Serial.print(F("give: "));
  Serial.println(give);
}

void loop() {
  t = millis(); //set the time
  while (give>0){
    digitalWrite(13, HIGH);
    s.write(spd); //start motor
    delay(1);
    int sensorValue = analogRead(A0); //read sensors
    float voltage= sensorValue * (5.0 / 1023.0);
    if (voltage > 4) // if beam is broken
    {
      Serial.println(voltage);
      Serial.println(give);
      give = give-1;
      delay(50);
      t = millis();
    }
    if (millis()-t>800){
      spd = abs(spd-180);
      t = millis();
    }; //when motor is stuck change direction of turning
    n = n +1;
    digitalWrite(13, LOW);
    s.write(90);
  }
}
