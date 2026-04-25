#include <Servo.h>

Servo panServo;
Servo tiltServo;

void setup() {
  Serial.begin(115200);
  panServo.attach(9);
  tiltServo.attach(10);
  panServo.write(90); 
  tiltServo.write(165);
}

void loop() {
  if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      
      int xIndex = data.indexOf('X');
      int yIndex = data.indexOf('Y');
      
      if (xIndex != -1 && yIndex != -1) {
        int xVal = data.substring(xIndex + 1, yIndex).toInt();
        int yVal = data.substring(yIndex + 1).toInt();
        
        if (xVal >= 0 && xVal <= 180) panServo.write(90 + -1*xVal);
        if (yVal >= 0 && yVal <= 180) tiltServo.write(165 + -1*yVal);
      }
    }
}
