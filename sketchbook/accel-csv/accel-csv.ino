
#include <Wire.h>
#include <SparkFunADXL313.h> //Click here to get the library: http://librarymanager/All#SparkFun_ADXL313
ADXL313 myAdxl;

void setup()
{
  Serial.begin(9600);

  Wire.begin();

  if (myAdxl.begin() == false) //Begin communication over I2C
  {
    Serial.println("The sensor did not respond. Please check wiring.");
    while(1); //Freeze
  }

  myAdxl.setRange(ADXL313_RANGE_4_G);
  
  myAdxl.measureModeOn(); // wakes up the sensor from standby and puts it into measurement mode
}

void loop()
{
  if(myAdxl.dataReady()) // check data ready interrupt, note, this clears all other int bits in INT_SOURCE reg
  {
    myAdxl.readAccel(); // read all 3 axis, they are stored in class variables: myAdxl.x, myAdxl.y and myAdxl.z
    Serial.print(myAdxl.x);
    Serial.print(",");
    Serial.print(myAdxl.y);
    Serial.print(",");
    Serial.print(myAdxl.z);
    Serial.println();
  }
  else
  {
    Serial.println("Waiting for dataReady.");
  }  
  delay(50);
}
