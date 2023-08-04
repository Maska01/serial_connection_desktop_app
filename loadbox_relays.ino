
#define times 200
#define high 0
#define low 1 
#define NPins 8
int Pins[]={2,3,4,5,6,7,9,10};
int data=8;

void setup() {
  configure_pins();
  turn_everything_off();
  Serial.begin(9600);
    while (!Serial) {
      ; // wait for serial port to connect. Needed for native USB
    }  
}

void loop() {

}

void configure_pins(){
  for(int i=0;i<NPins;i++){
    pinMode(Pins[i], OUTPUT);
  }
}

void turn_everything_off(){
  for(int i=0;i<NPins;i++){
    digitalWrite(Pins[i], low);
  }
}

void turn_everything_on(){
  for(int i=0;i<NPins;i++){
    digitalWrite(Pins[i], high);
  }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    data = Serial.read();
    if(data!=10){
      Serial.println(data-48);  
      switch (data-48) {
          case 0: //Turn V_BAT ON
            Serial.println("RELAY 1 ON");
            digitalWrite(Pins[0], high);
            break;

          case 1: //Turn IGNITION ON
            Serial.println("RELAY 2 ON");
            digitalWrite(Pins[1], high);
            break;

          case 2:  //Turn ACCESS ON
            Serial.println("RELAY 3 ON");
            digitalWrite(Pins[2], high);
            break;

          case 3: //Activate PCAN HI FOR CHANNEL 0
            Serial.println("RELAY 4 ON");
            digitalWrite(Pins[3], high);
            
            Serial.println("RELAY 5 ON");
            digitalWrite(Pins[4], high);
            break;

          case 4: //Activate SHORT FOR CAN BUS 0
            Serial.println("RELAY 6 ON");
            digitalWrite(Pins[5], high);
            break;

          case 5: //Activate SHORT FOR CAN BUS 1
            Serial.println("RELAY 7 ON");
            digitalWrite(Pins[6], high);
            break;

          /***************************************/

          case 6: //Turn V_BAT OFF
            Serial.println("RELAY 1 OFF");
            digitalWrite(Pins[0], low);
            break;

          case 7: //Turn IGNITION OFF
            Serial.println("RELAY 2 OFF");
            digitalWrite(Pins[1], low);
            break;

          case 8:  //Turn ACCESS OFF :
            Serial.println("RELAY 3 OFF");
            digitalWrite(Pins[2], low);
            break;

          case 9: //Activate PCAN HI ad LO FOR CHANNEL  1 ;
            Serial.println("RELAY 4 OFF");
            digitalWrite(Pins[3], low);
            Serial.println("RELAY 5 OFF");
            digitalWrite(Pins[4], low);
            break;

          case 10: //Deactivate SHORT FOR CAN BUS 0
            Serial.println("RELAY 6 OFF");
            digitalWrite(Pins[5], low);
            break;

          case 11: //Deactivate SHORT FOR CAN BUS 1
            Serial.println("RELAY 7 OFF");
            digitalWrite(Pins[6], low);
            break;
            
          default:                              
            Serial.println("command not identified");                             
            break;
        }

      }
                  
              
  }

  
}
