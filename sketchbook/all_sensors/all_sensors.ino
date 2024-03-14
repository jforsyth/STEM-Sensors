
/*******************************************************************************************************************
** Declare all program constants                                                                                  **
*******************************************************************************************************************/
const uint32_t SERIAL_SPEED = 9600; ///< Set the baud rate for Serial I/O

/*******************************************************************************************************************
** Declare global variables and instantiate classes                                                               **
*******************************************************************************************************************/
//include the libraries for the BME (humdity, pressure, altitude, and temperature)
//and the CCS (CO2 and TVOC) sensors
#include "SparkFunCCS811.h"
#include "SparkFunBME280.h"

//include Wire Library to access i2c
#include <Wire.h>

//include the MMA8452 library
#include "SparkFun_MMA8452Q.h"

//create a handle to the accelerometer
MMA8452Q accel;

//define the default I2C address of the CCS. Is not needed for BME
//as is already in library
#define CCS811_ADDR 0x5B //Default I2C Address

//create handles to the two sensors
BME280 bmeSensor;
CCS811 ccsSensor(CCS811_ADDR);

// Include the SparkFun VEML6075 library.
// Click here to get the library: http://librarymanager/All#SparkFun_VEML6075
#include <SparkFun_VEML6075_Arduino_Library.h>

VEML6075 uv; // Create a VEML6075 object

void setup()
{
  /*!
    @brief    Arduino method called once at startup to initialize the system
    @details  This is an Arduino IDE method which is called first upon boot or restart. It is only called one time
            and then control goes to the main "loop()" method, from which control never returns
    @return   void
  */
  Serial.begin(SERIAL_SPEED); // Start serial port at Baud rate
#ifdef  __AVR_ATmega32U4__  // If this is a 32U4 processor, then wait 3 seconds to initialize USB port
  delay(3000);
#endif

  if (bmeSensor.beginI2C() == false) //Begin communication over I2C
  {
    Serial.println("Could not access the BME sensor. Please check wiring.");
    while (1); //Freeze
  }


  CCS811Core::status returnCode = ccsSensor.begin();
  if (returnCode != CCS811Core::SENSOR_SUCCESS)
  {
    Serial.println("Could not access the CCS sensor. Please check wiring.");
    while (1); //Hang if there was a problem.
  }


  if (uv.begin() == false)
  {

    while (1)
    {
      Serial.println("Unable to communicate with UV sensor. Check connection.");
      delay(1000);
    }
  }

  // initialize but set to 4gs
  accel.init(SCALE_4G);

  // Serial.println("Time(s)\tTemp\tHumidity\tPressure\t\tUV");

} // of method setup()

const int loop_delay = 100;
int loop_counter = 0;

float humidity;
float pressure;
float altitude;
float temp;
float xAccel;
float yAccel;
float zAccel;
float uv_index;
void loop()
{
  ////////Get Acceleration Data//////////
  if (accel.available())
  {
    xAccel = accel.getCalculatedX();

    yAccel = accel.getCalculatedY();


    zAccel = accel.getCalculatedZ();
  }


  ////////////////////// Get Data from the BME Board //////////////////////
  humidity = bmeSensor.readFloatHumidity();
  pressure = bmeSensor.readFloatPressure();
  altitude = bmeSensor.readFloatAltitudeFeet();
  temp = bmeSensor.readTempC();
  uv_index = uv.index();

  Serial.print(temp); Serial.print(",");
  Serial.print(humidity); Serial.print(",");
  Serial.print(pressure); Serial.print(",");
  Serial.print(uv_index);Serial.print(",");
  Serial.print(xAccel);Serial.print(",");
  Serial.print(yAccel);Serial.print(",");
  Serial.println(zAccel);

  delay(loop_delay);
  loop_counter++;
  // Wait 1s before repeating*/
} // of method loop()
