
//include SoftwareSerial to remove Xbee from built-in RX and TX lines
#include <SoftwareSerial.h>

//new RX line to receive from Xbee
const int XBEE_RX_PIN = 2;

//new TX line to send to Xbee
const int XBEE_TX_PIN = 3;

//instantiate SoftwareSerial for Xbee
SoftwareSerial Xbee (XBEE_RX_PIN,XBEE_TX_PIN);


void setup() 
{
  Serial.begin(9600);

  Xbee.begin(9600);

}

void loop() 
{
  Xbee.print("!");
  delay(1000);
}
