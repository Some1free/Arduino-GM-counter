// Author: Mateusz Wolniewicz
// Date: 04/06/2024
// Version: 1.0.1
// Licence: Open Source

// This Sketch counts the number of pulses during the time interval. 
// Time interval is being read via serial port.
// Number of counts is being sent vis serial port. 

//              CONNECTIONS 
// Connect the GND on Arduino to the GND on the Geiger counter.
// Connect the 5V on the Geiger counter to the 5V on Arduino OR connect the external power supply.
// Connect the VIN on the Geiger counter to the digital pin (f. ex. D2) on the Arduino.


unsigned long counts; //variable for counting GM Tube events
unsigned long previousMillis; //variable for measuring time
unsigned int logPeriod = 1000; //variable for definig lenght of counting period, 1000ms for default, [millis]
uint16_t GM_PIN = D2; //variable setting nb of pin where VIN pin on GM counter is conncected

void impulse() { //interrput function
  counts++;
  }

void setup() {
  counts = 0;
  Serial.begin(115200);
  delay(5000);
  while (Serial.available() == 0) {
    // Waiting for input 
  }
  
  logPeriod = Serial.parseInt();
  pinMode(GM_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(GM_PIN), impulse, FALLING); //defining external interrupts
}

void loop() { 
  if (Serial.available() > 0) { // Checking if data is available to read from the serial port
    logPeriod = Serial.parseInt();
  }

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis > logPeriod) {
    previousMillis = currentMillis;
    Serial.println(counts);
    counts = 0;
  }
}

