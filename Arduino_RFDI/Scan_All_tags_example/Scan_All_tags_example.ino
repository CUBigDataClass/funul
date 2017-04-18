/*
  Reading multiple RFID tags, simultaneously!
  By: Nathan Seidle @ SparkFun Electronics
  Date: October 3rd, 2016
  https://github.com/sparkfun/Simultaneous_RFID_Tag_Reader

  Single shot read - Ask the reader to tell us what tags it currently sees. And it beeps!

  If using the Simultaneous RFID Tag Reader (SRTR) shield, make sure the serial slide
  switch is in the 'SW-UART' position.
*/

#include <SoftwareSerial.h> //Used for transmitting to the device

SoftwareSerial softSerial(2, 3); //RX, TX

#include "SparkFun_UHF_RFID_Reader.h" //Library for controlling the M6E Nano module
RFID nano; //Create instance

#define BUZZER1 9
#define BUZZER1 0 //For testing quietly
#define BUZZER2 10
#define MAX_NUMBER_OF_ITEMS 100

//set up globals
int myEPClength = 12;
byte EPCS_arrarr[MAX_NUMBER_OF_ITEMS][myEPClength];
byte new_ECP_arr[myEPClength];

void setup()
{
  Serial.begin(115200);

  pinMode(BUZZER1, OUTPUT);
  pinMode(BUZZER2, OUTPUT);

  digitalWrite(BUZZER2, LOW); //Pull half the buzzer to ground and drive the other half.

  while (!Serial);
  Serial.println();
  Serial.println("Initializing...");

  if (setupNano(38400) == false) //Configure nano to run at 38400bps
  {
    Serial.println("Module failed to respond. Please check wiring.");
    while (1); //Freeze!
  }

  nano.setRegion(REGION_NORTHAMERICA); //Set to North America

  nano.setReadPower(500); //5.00 dBm. Higher values may cause USB port to brown out
  //Max Read TX Power is 27.00 dBm and may cause temperature-limit throttling
}
//inserts new_EPC_arr into EPCS_arrarr if new_EPC_arr does not exist returns true if inserted false if not inserted
boolean insert_into_array_if_unq(int cur_number_of_EPC) {
  bool not_equal;
  for (int i = 0; i < cur_number_of_EPC; ++i) {
    not_equal = false;
    for (int n = 0; ((n < myEPClength) && (not_equal == false)); ++n) {
      if (EPCS_arrarr[i][n] != new_ECP_arr[n]) {
        not_equal = true;
      }
    }
    if (not_equal == false) {
      return false;
    }
  }
  for (int n = 0; n < myEPClength; ++n) {
    EPCS_arrarr[cur_number_of_EPC][n] = new_ECP_arr[n];
  }
  return true;
}

void loop()
{
  Serial.read(); //Throw away the user's character

  int number_of_unq_EPC = 0;
  byte EPClength = myEPClength;
  byte responseType = 0;
  Serial.print("Starting Scan");
  while (0 != RESPONSE_SUCCESS)//RESPONSE_IS_TAGFOUND)
  {
    myEPClength = sizeof(new_ECP_arr); //Length of EPC is modified each time .readTagEPC is called
    responseType = nano.readTagEPC(new_ECP_arr, EPClength, 500); //Scan for a new tag up to 500ms
    if (responseType == RESPONSE_SUCCESS) {
      if (insert_into_array_if_unq(number_of_unq_EPC) == true) {
        //this means the EPC is unq. and has been added to the global array
        Serial.print(F(" epc["));
          for (byte x = 0 ; x < myEPClength ; x++)
          {
            if (EPCS_arrarr[number_of_unq_EPC][x] < 0x10) Serial.print(F("0"));
            Serial.print(EPCS_arrarr[number_of_unq_EPC][x], HEX);
            Serial.print(F(" "));
          }
        Serial.println(F("]")); 
        responseType = 0;
        number_of_unq_EPC++;
      }     
    }
  }
}

//Gracefully handles a reader that is already configured and already reading continuously
//Because Stream does not have a .begin() we have to do this outside the library
boolean setupNano(long baudRate)
{
  nano.begin(softSerial); //Tell the library to communicate over software serial port

  //Test to see if we are already connected to a module
  //This would be the case if the Arduino has been reprogrammed and the module has stayed powered
  softSerial.begin(baudRate); //For this test, assume module is already at our desired baud rate
  while(!softSerial); //Wait for port to open

  //About 200ms from power on the module will send its firmware version at 115200. We need to ignore this.
  while(softSerial.available()) softSerial.read();
  
  nano.getVersion();

  if (nano.msg[0] == ERROR_WRONG_OPCODE_RESPONSE)
  {
    //This happens if the baud rate is correct but the module is doing a ccontinuous read
    nano.stopReading();

    Serial.println(F("Module continuously reading. Asking it to stop..."));

    delay(1500);
  }
  else
  {
    //The module did not respond so assume it's just been powered on and communicating at 115200bps
    softSerial.begin(115200); //Start software serial at 115200

    nano.setBaud(baudRate); //Tell the module to go to the chosen baud rate. Ignore the response msg

    softSerial.begin(baudRate); //Start the software serial port, this time at user's chosen baud rate
  }

  //Test the connection
  nano.getVersion();
  if (nano.msg[0] != ALL_GOOD) return (false); //Something is not right

  //The M6E has these settings no matter what
  nano.setTagProtocol(); //Set protocol to GEN2

  nano.setAntennaPort(); //Set TX/RX antenna ports to 1

  return (true); //We are ready to rock
}

