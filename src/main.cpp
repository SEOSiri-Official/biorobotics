// firmware/robot_node/src/main.cpp
#include <Arduino.h>
#include <Servo.h>

Servo jointServo;
String inputString = "";

void parseGCode(String cmd);

void setup() {
  Serial.begin(115200);
  jointServo.attach(9); // Connect servo signal pin to Arduino Pin 9
  jointServo.write(0);  // Initialize servo at home position (0 degrees)
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      parseGCode(inputString);
      inputString = ""; // Reset buffer
    } else {
      inputString += inChar;
    }
  }
}

void parseGCode(String cmd) {
  cmd.trim();
  // Expecting standard G-code format: "G1 X[angle] F[feedrate]"
  if (cmd.startsWith("G1")) {
    int xIndex = cmd.indexOf('X');
    int fIndex = cmd.indexOf('F');
    if (xIndex != -1) {
      String angleStr = (fIndex != -1) ? cmd.substring(xIndex + 1, fIndex) : cmd.substring(xIndex + 1);
      float targetAngle = angleStr.toFloat();
      
      // Enforce physical boundary safety limits (0 to 180 degrees)
      targetAngle = max(0.0f, min(targetAngle, 180.0f));
      
      jointServo.write((int)targetAngle); // Actuate the physical joint
    }
  }
}