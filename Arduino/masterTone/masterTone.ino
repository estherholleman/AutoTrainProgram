#include <Wire.h>

// include libraries for music player
#include <SPI.h>
#include <Adafruit_VS1053.h>
#include <SD.h>

int sensor_nr = 9;
unsigned long int c = 0;
int n, f = 0;
unsigned long int t = 0;
unsigned long int t2 = 0;
unsigned long int settings[] = {0, 5000, 60000};
int reward = 0;

// Define all pins needed for music player
// These are the pins used for the breakout example
#define BREAKOUT_RESET  9      // VS1053 reset pin (output)
#define BREAKOUT_CS     10     // VS1053 chip select pin (output)
#define BREAKOUT_DCS    8      // VS1053 Data/command select pin (output)
// These are the pins used for the music maker shield
#define SHIELD_RESET  -1      // VS1053 reset pin (unused!)
#define SHIELD_CS     7      // VS1053 chip select pin (output)
#define SHIELD_DCS    6      // VS1053 Data/command select pin (output)

// These are common pins between breakout and shield
#define CARDCS 4     // Card chip select pin
// DREQ should be an Int pin, see http://arduino.cc/en/Reference/attachInterrupt
#define DREQ 3       // VS1053 Data request, ideally an Interrupt pin

Adafruit_VS1053_FilePlayer musicPlayer = 
  // create breakout-example object!
  // Adafruit_VS1053_FilePlayer(BREAKOUT_RESET, BREAKOUT_CS, BREAKOUT_DCS, DREQ, CARDCS);
  // create shield-example object!
  Adafruit_VS1053_FilePlayer(SHIELD_RESET, SHIELD_CS, SHIELD_DCS, DREQ, CARDCS);
  

void setup()
{
  Wire.begin();
  Serial.begin(115200);
  musicPlayer.begin();
  
//    if (! musicPlayer.begin()) { // initialise the music player
//     Serial.println(F("Couldn't find VS1053, do you have the right pins defined?"));
//     while (1);
//  }
//  Serial.println(F("VS1053 found"));
  
  SD.begin(CARDCS);    // initialise the SD card
  
  // Set volume for left, right channels. lower numbers == louder volume!
  musicPlayer.setVolume(20,20);

  // Timer interrupts are not suggested, better to use DREQ interrupt!
  //musicPlayer.useInterrupt(VS1053_FILEPLAYER_TIMER0_INT); // timer int

  // If DREQ is on an interrupt pin (on uno, #2 or #3) we can do background
  // audio playing
  musicPlayer.useInterrupt(VS1053_FILEPLAYER_PIN_INT);  // DREQ int
  
}

void loop()
{
  if (Serial.available() > 0) {
    f = Serial.parseInt();
    Serial.println(f);
    if (f == 0) {
      load_settings();
    }
    if (f == 1) {
      run_trial();
    }
    if (f == 2) {
          Wire.beginTransmission(n+2);
          Wire.write(1);
          Wire.endTransmission();
    }
  }
}

void load_settings() {
  for (int i = 0; i < 3; ++i) {
    while (1) {
      if (Serial.available() > 0) {
        c = Serial.parseInt();
        Serial.println(c);
        settings[i] = c;
        break;
      }
    }
  }
}

void run_trial() {
  while (1) {
    if (Serial.available() > 0) {
      n = Serial.parseInt();
      Serial.println(n);
      while (1) {
        if (Serial.available() > 0) {
          int w = Serial.parseInt();
          if(w==2){
              Wire.beginTransmission(n);
              Wire.write(1);
              Wire.endTransmission();
              break;
          }
        }
        Wire.requestFrom(4, 1);
        int sensor_nr = Wire.read();
        if (sensor_nr == 1) {
        
//          Wire.beginTransmission(n);
//          Wire.write(1);
//          Wire.endTransmission();

            if (n == 0) {
              musicPlayer.playFullFile("tone7.wav");
            }
            if (n == 1) {
              musicPlayer.playFullFile("tone14.wav");
            }
          break;
        }
      }
      t = millis();
      while (1) {
        t2 = millis() - t;
        if (t2 > settings[2]) {
          Serial.println(2);
          Serial.println(t2);
          Serial.println(0);
          break;
        }
        if (Serial.available() > 0) {
          int w = Serial.parseInt();
          if(w==2){
              Wire.beginTransmission(n+2);
              Wire.write(1);
              Wire.endTransmission();
              delay(100);
              Serial.println(n);
              Serial.println(t2);
              Serial.println(0);
              break;
          }
          if(w==3){
              delay(100);
              Serial.println(n);
              Serial.println(t2);
              Serial.println(0);
              break;
          }
        }
        Wire.requestFrom(4, 1);
        int sensor_nr = Wire.read();
        if (sensor_nr == n + 2) {
          if (t2 < settings[0]) {
            reward = 3;
          }
          if (t2 < settings[1]) {
            reward = 2;
          }
          else {
            reward = 1;
          }
          Wire.beginTransmission(n + 2);
          Wire.write(reward);
          Wire.endTransmission();
          Serial.println(n);
          Serial.println(t2);
          Serial.println(reward);
          break;
        }
        if (sensor_nr == abs(n - 3)) {
          Serial.println(abs(n - 1));
          Serial.println(t2);
          Serial.println(0);
          break;
        }
      }
      break;
    }
  }
}

