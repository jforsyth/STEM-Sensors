/******************************************************************************
  Example1_BasicReadings.ino
  Read values of x/y/z axis of the ADXL313 (via I2C), print them to terminal.
  This uses default configuration (1G range, full resolution, 100Hz datarate).

  SparkFun ADXL313 Arduino Library
  Pete Lewis @ SparkFun Electronics
  Original Creation Date: September 19, 2020
  https://github.com/sparkfun/SparkFun_ADXL313_Arduino_Library

  Do you like this library? Help support SparkFun. Buy a board!

    SparkFun 3-Axis Digital Accelerometer Breakout - ADXL313 (Qwiic)
    https://www.sparkfun.com/products/17241

  Development environment specifics:

  IDE: Arduino 1.8.13
  Hardware Platform: SparkFun Redboard Qwiic
  SparkFun 3-Axis Digital Accelerometer Breakout - ADXL313 (Qwiic) Version: 1.0

  Hardware Connections:
  Use a qwiic cable to connect from the Redboard Qwiic to the ADXL313 breakout (QWIIC).
  You can also choose to wire up the connections using the header pins like so:

  ARDUINO --> ADXL313
  SDA (A4) --> SDA
  SCL (A5) --> SCL
  3.3V --> 3.3V
  GND --> GND

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
******************************************************************************/

#include <Wire.h>
#include <SparkFunADXL313.h> //Click here to get the library: http://librarymanager/All#SparkFun_ADXL313
ADXL313 accel;

void setup()
{
  Serial.begin(115200);

  Wire.begin();

  if (accel.begin() == false) //Begin communication over I2C
  {
    Serial.println("The sensor did not respond. Please check wiring.");
    while (1); //Freeze
  }

  accel.setRange(ADXL313_RANGE_4_G);

  accel.measureModeOn(); // wakes up the sensor from standby and puts it into measurement mode
}

float get_acceleration()
{

  // read the accelerometer attached to the i2c bus
  accel.readAccel();

  // calculate the magnitude of acceleration sqrt(x^2 + y^2 + z^2)
  int magnitude = sqrt(accel.x * accel.x + accel.y * accel.y + accel.z * accel.z);

  // convert the magnitude to acceleration in g's (512/range)
  return (float) magnitude / 128;
}

void loop()
{

  //an array to hold sample readings
  const int num_samples = 200;
  float sensor_readings[num_samples];

  //hold the sum of the array
  float sum = 0;

  //loop through all sensor values
  for (int i = 0; i < num_samples; i++)
  {
    //pull the most recent sample from the array
    float acceleration = sensor_readings[i];

    //add the most recent value to the sum
    sum = sum + acceleration;
  }

  //divide the sum by the length
  float average = sum / (float)num_samples;


  // take a sample every 50ms (200 Hz)
  delay(50);
}
