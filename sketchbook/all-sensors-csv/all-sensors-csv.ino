// Include the SparkFun VEML6075 library.
// Click here to get the library: http://librarymanager/All#SparkFun_VEML6075
#include <SparkFun_VEML6075_Arduino_Library.h>

VEML6075 uv; // Create a VEML6075 object

#include "Zanshin_BME680.h" // Include the BME680 Sensor library
BME680_Class BME680; ///< Create an instance of the BME680 class

float altitude(const int32_t press, const float seaLevel = 1013.25); ///< Forward function declaration with default value for sea level
float altitude(const int32_t press, const float seaLevel)
{
  /*!
    @brief     This converts a pressure measurement into a height in meters
    @details   The corrected sea-level pressure can be passed into the function if it is know, otherwise the standard
               atmospheric pressure of 1013.25hPa is used (see https://en.wikipedia.org/wiki/Atmospheric_pressure)
    @param[in] press    Pressure reading from BME680
    @param[in] seaLevel Sea-Level pressure in millibars
    @return    floating point altitude in meters.
  */
  static float Altitude;
  Altitude = 44330.0 * (1.0 - pow(((float)press / 100.0) / seaLevel, 0.1903)); // Convert into altitude in meters
  return (Altitude);
} // of method altitude()

#include <SparkFunADXL313.h> //Click here to get the library: http://librarymanager/All#SparkFun_ADXL313
ADXL313 myAdxl;

float accel_range = -1;
void setup() {

  Serial.begin(57600);

  Wire.begin();

  // the VEML6075's begin function can take no parameters
  // It will return true on success or false on failure to communicate
  if (uv.begin() == false)
  {

    while (1)
    {
      Serial.println("Unable to communicate with VEML6075. Check wiring.");
      delay(5000);

    }
  }

  while (!BME680.begin(I2C_STANDARD_MODE)) // Start BME680 using I2C protocol
  {
    Serial.print(F("-  Unable to find BME680. Trying again in 5 seconds. Please check wiring.\n"));
    delay(5000);
  } // of loop until device is located
  //Serial.print(F("- Setting 16x oversampling for all sensors\n"));
  BME680.setOversampling(TemperatureSensor, Oversample16); // Use enumerated type values
  BME680.setOversampling(HumiditySensor,   Oversample16); // Use enumerated type values
  BME680.setOversampling(PressureSensor,   Oversample16); // Use enumerated type values
  //Serial.print(F("- Setting IIR filter to a value of 4 samples\n"));
  BME680.setIIRFilter(IIR4); // Use enumerated type values
  //Serial.print(F("- Setting gas measurement to 320\xC2\xB0\x43 for 150ms\n")); // "�C" symbols
  BME680.setGas(320, 150); // 320�c for 150 milliseconds

  if (myAdxl.begin() == false) //Begin communication over I2C
  {
    Serial.println("The sensor did not respond. Please check wiring.");
    while (1); //Freeze
  }
  myAdxl.setRange(ADXL313_RANGE_4_G);

  myAdxl.measureModeOn(); // wakes up the sensor from standby and puts it into measurement mode

  accel_range = 4;

}

const int loop_delay = 200;
void loop() {

  /**
     Collect all data from UV sensor: UV-A, UV-B, and UV-Index
  */
  static float UVA = 0;
  static float UVB = 0;
  static float UV_Index = 0;

  UVA = uv.uva();
  UVB = uv.uvb();
  UV_Index = uv.index();

  /**
     Collect all data from the environmental board: temperature (C), humidity (%),
     pressure (hecto Pascals), and gas concentration (ppm). Derive altitude (meters) from pressure
  */

  static int32_t  _temp, _humidity, _pressure, _gas;
  static float alt;

  // get sensor data and calculate altitude
  BME680.getSensorData(_temp, _humidity, _pressure, _gas);
  alt = altitude(_pressure);

  // scale values to appropriate ranges
  float temp = _temp / 100.0;
  float humidity = _humidity / 1000.0;
  float pressure = _pressure / 100.0;

  /**
     Get Acceleration data
  */

  static float xAccel = 0;
  static float yAccel = 0;
  static float zAccel = 0;
  if (myAdxl.dataReady()) // check data ready interrupt, note, this clears all other int bits in INT_SOURCE reg
  {
    myAdxl.readAccel(); // read all 3 axis, they are stored in class variables: myAdxl.x, myAdxl.y and myAdxl.z

    int x_accel = myAdxl.x;
    int y_accel = myAdxl.y;
    int z_accel = myAdxl.z;

    xAccel = (float)x_accel / 512.0 * accel_range;
    yAccel = (float)y_accel / 512.0 * accel_range;
    zAccel = (float)z_accel / 512.0 * accel_range;
  }

  /**
     Print all data as CSV
  */
  Serial.print(temp); Serial.print(",");
  Serial.print(humidity); Serial.print(",");
  Serial.print(pressure); Serial.print(",");
  Serial.print(UV_Index); Serial.print(",");
  Serial.print(xAccel); Serial.print(",");
  Serial.print(yAccel); Serial.print(",");
  Serial.println(zAccel);
  delay(loop_delay);
}
