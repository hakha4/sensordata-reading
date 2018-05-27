





//-----------------------------------------------------------------------------------
//------------------- Test sketch for Py program Read sensordata --------------------
//-----------------------------------------------------------------------------------

// updated 180526
// Author : Håkan Hallberg
// ToDo : clean up some unused code and implement for more sensortypes
//--------------------------------------------------------------

//----- Includes -----------------------------------------------
#include <Arduino.h>
#include <stdlib.h> // for the atoi() function
#include <avr/io.h>
#include <avr/interrupt.h>
#include <Wire.h>
#include "RTClib.h"
#include <Time.h>
#include <DallasTemperature.h>
#include <OneWire.h>
//#include <dht.h>

//------------------ END INCLUDES ------------------------------

// -------------------- DEFINES --------------------------------
#define DEBUG 1// to serial port 

#define ONE_WIRE_BUS 4//default pin 4
#define TEMPERATURE_PRECISION 9 // lower precision for faster conversion
#define BOARD_ID 1
#define BOARD_NO 1
#define ID_STRING "Pytest"
//#define RTC_MODE 1
//dht DHT;//start DHT instance

 
//------------------ Setup Temp. sensors ---------------------------
// Setup a oneWire (ON PIN 4 as default) 
OneWire oneWire(ONE_WIRE_BUS);

// Pass oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);
//------------------ END 1-wire setup Setup ---------------------------

// ---- DECLARATIONS ---------------------------

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the inputstring is complete or not

int numberOfDevices; // Number of temperature devices found
DeviceAddress tempDeviceAddress; //  variable to store a found device address (1-Wire)
//int numberOfDHT11_sensors = 1;	// number of humidity sensors connected,default 1,max 

int numberOfSoil_sensors = 1;	// number of soil sensors connected,default 1,max 3?
int soil_sensorPin = 0;    // select the BASE (analog)input pin for the soil sensors, CHANGE FOR EACH TYPE OF BOARD!
int soil_sensorVCC = 13;//power pin to soil sensor
 

unsigned long DS1307Timer;//time in sec's since midnight
volatile byte TempTimer_interval;          // interval in secs between readings
boolean TempTimer;                 // flag to see if interval been reached

byte TempTimer_interval_Set = 10;     // user set of interval between readings
char* newtime;                      // current time


//---------------------- End Declarations------------------------------------------------------



#if defined RTC_MODE // if hardware RTC connected
  RTC_DS1307 RTC;         // constructor for I2C hardware clock
  
 #else // software RTC
 
 RTC_Millis RTC; // constructor for software clock

#endif  

void setup(void)
{
// *********************************************

	Serial.begin(115200);
 
  //start1-Wire
  Wire.begin(); // SDA = pin 20/SCL = pin 21 on Mega2560
  
  // start clock HW or SW
  #if defined RTC_MODE // hardware RTC
  RTC.begin(); 
  #else
  RTC.begin(DateTime(__DATE__, __TIME__));
  #endif
  
  // Start up Dallas 1-Wire library
    sensors.begin();

// setup software RTC 
  RTC.adjust(DateTime(__DATE__, __TIME__));
  Serial.println("__________________________________________"); 
  Serial.println("##### SW RTC is running #######");
  Serial.println("__________________________________________");
 // #endif
  //-------------------------------------------------------
  // Get a count of tempsensors
  numberOfDevices = sensors.getDeviceCount();
  OneWire_report();

init_avr_timer1(15624); // initialise timer1 for 1Hz
 }// end setup


      ISR(TIMER1_COMPA_vect)
{
    tempTimerIntRoutine();
}

//---------------------------------------------------------------------------------------------------------------
void loop(void){
DateTime now = RTC.now();
   
static unsigned int newsecs = 0;
static unsigned int oldsecs = 0;

serialEvent(); // poll serialevent for incoming requests
   
   if (stringComplete) {
     
     //check if it's for me, 110xx + cmd. In this case 11001x for 'whoami as example'
     String toEval = inputString.substring(5);
     int tmpID;
     char carray[6];
     inputString.substring(0,5).toCharArray(carray, sizeof(carray));
     tmpID = atoi(carray); 
     eval_Radiodata(toEval);     
       
     // clear inputstring:
     inputString = "";
     stringComplete = false;
  }

      
  // update time
     newsecs=now.second();
     if (newsecs != oldsecs) {
      char buf[6];
      sprintf(buf, "%02d:%02d:%02d", now.hour(), now.minute(), now.second());    
      newtime = buf;
     
      // Update DS1307Timer
      //***********************************************************************************
      //0 - 86400 -> 3600/hour (seconds since midnight)
     
      unsigned long tmpHour = now.hour();
      unsigned long tmpMin = now.minute();
      unsigned long tmpSecs = now.second();
  
      DS1307Timer = tmpHour * 3600 + tmpMin * 60 + tmpSecs;
            
    }
     oldsecs = newsecs;
    
    if(TempTimer) {
   
        Serial.println("Checking sensor status");
        Serial.println(newtime);
         
        eval_Radiodata ("T");// temperature sensors
       //  eval_Radiodata ("B");// soil sensors
       // eval_Radiodata ("H");// humidity sensor
       delay(100);
       TempTimer = false;
       
     } 


} //------------------------------ End void Loop ------------------------------------------




//----------- EVALUATE RADIO DATA -------------------------------------
void eval_Radiodata(String radioData)
{
 
  String tmpCmd;//A,B,C,D;E etc
  String tmpData="";//relaystatus etc
  String tmpdata_eval;//data to be sent/evaluated in routines
  unsigned int strLen;
  //EVALUATE new data and take action !!!!!!!!! 
  tmpCmd = radioData.substring(0,1);//strip off command id

  tmpData = radioData.substring(1,radioData.length());//strip off data part

  // just for debug
  //Serial.print("Incoming DATA : ");
 // Serial.println(radioData);
  strLen = tmpData.length();
 
  

  /////////////////////////////////////////////////////////////////////////
  ///////       Dispatch the command to the correct handler.  /////////////
  /////////////////////////////////////////////////////////////////////////
  
   
  if (tmpCmd.equals("H")) //read humidity sensors
  {
    
    Serial.println("Reading humidity data");
     
  //    Read_DHT11();
  }
   
  
  if (tmpCmd.equals("w")) //whoami
  {
   Serial.print("I am Node : ");
   Serial.println(BOARD_NO);
	 Serial.println(ID_STRING);
 
  }
  
 
//----------------- Check Temp. sensors  ---------------------------------------------------

  if (tmpCmd.equals("T"))   //Temperatures  NOT FINISHED!!!!!!!!!!!!!!!!!!!!!!!!!   
    {
     if(numberOfDevices > 0)// check temps if there were sensors detected
	{
       // Serial.println("Reading Temperature sensor(s)");
	Check_Temp();
	
	}
     else
     {
      // Serial.println("No Temperature sensor(s) connected");
     }
    }
//----------------- END Check Temp. sensors  ---------------------------------------------------



//----------------- Show systemtime -------------------------------------------------------------   
 if (tmpCmd.equals("t"))
   {
    showSystemTime();
   }  
//----------------- END Show systemtime -------------------------------------------------------------   


 //----------------- Set softRTC time -------------------------------------------------------------   

    if (tmpCmd.equals("y")) 
    {
      setSoftRTCTime(tmpData);
    }
//----------------- END softRTC time -------------------------------------------------------------   
 
 


 if (tmpCmd.equals("B")) 
        {
          String StringToSend;
         for (int i=1; i<numberOfSoil_sensors+1; i++)// 1 to number of devsoil sensors 
     {
  TempTimer = false;//disable eval data in main temporary
  String sens_value = Read_soilSensors(i);
  
 delay(100);//give time to catch up 
  StringToSend = StringToSend + i + sens_value +"*";
     }
     sendData("S~",BOARD_NO,String(numberOfSoil_sensors) + "~" + StringToSend.substring(0,StringToSend.length()-1));
        } 
  //----------------- END Read soil sensors 
 
  
 
  
}
//---------------------- END eval_Radiodata -------------------------------------------------


//-------------------------------------------------------------------------------
//--------------- ROUTINES FOR DALLAS temp. sensors ---------------------------------
//-------------------------------------------------------------------------------

//--------------------------- Read DS18b20 sensors and send to serial port --------------------------------

void Check_Temp()
{
 
  String StringToSend;
 String address;
 char tempBuf[6];
  sensors.requestTemperatures(); // Send the command to get temperature
  
  for(int i = 0;i<numberOfDevices; i++)
    {
    
  Serial.print("Temperature for sensor  ");
  Serial.print(i+1);
  Serial.print(" : ");
  float DS_temp = (sensors.getTempCByIndex(i));
  
  dtostrf(DS_temp,5,2,tempBuf);
  Serial.print(tempBuf);
  Serial.print(" C' ");
  
  if(sensors.getAddress(tempDeviceAddress, i))
	{
    address = printAddress(tempDeviceAddress);
    Serial.print(" ROM address : ");
   Serial.print(address);
          Serial.println();
        }
 
 StringToSend = StringToSend + tempBuf + "!" + i + "!" + address + "*";
 address="";
 
 }
                 
 
 sendData("T",BOARD_NO,String(numberOfDevices) + "~" + StringToSend.substring(0,StringToSend.length()-1));
 
   }
//--------------------END Read DS18b20 sensors and send to serial port -----------------------------------



//--------------------Find DS18b20 sensors on 1-Wire net -----------------------------------

void OneWire_report()
{
  // locate devices on the bus
 
 Serial.println("-------------------------------------------");
  Serial.println("Searching for 1-wire devices...");
  
  Serial.print("Found ");
  Serial.print(numberOfDevices, DEC);
  Serial.println(" devices.");

  // report parasite power requirements
  Serial.print("Parasite power is: "); 
  if (sensors.isParasitePowerMode()) Serial.println("ON");
  else Serial.println("OFF");
  Serial.println("-------------------------------------------");
 
  // Loop through each tempsensor
  for(int i = 0;i<numberOfDevices; i++)
    {
      // Search the wire for address
      if(sensors.getAddress(tempDeviceAddress, i))
	{
  String  tmpaddress =  printAddress(tempDeviceAddress);
    #if defined DEBUG
	  Serial.print("Found device ");
	  Serial.print(i + 1, DEC);
	  Serial.print(" with address: " + tmpaddress);
    
    #endif
	 
     // set the resolution to TEMPERATURE_PRECISION bit (Each Dallas/Maxim device is capable of several different resolutions)
    sensors.setResolution(tempDeviceAddress, TEMPERATURE_PRECISION);

    #if defined DEBUG
	  Serial.println();
	  Serial.print("Setting resolution to ");
	  Serial.println(TEMPERATURE_PRECISION, DEC);
    Serial.print("Resolution  set to: ");
	  Serial.print(sensors.getResolution(tempDeviceAddress), DEC); 
	  Serial.println();
	  #endif
	  
	 // Serial.print("D!W!");
	  //Serial.print(i);
	//  Serial.print("!");
	//  Serial.print(TEMPERATURE_PRECISION, DEC);
	//  Serial.print("!");
	//  printAddress(tempDeviceAddress);

	 // Serial.println("*");
		
	}
	else{
    #if defined DEBUG
	  Serial.print("Found ghost device at ");
	  Serial.print(i, DEC);
	  Serial.print(" but could not detect address. Check power and cabling");
    #endif
      }
    }

}
//-------------------- END Find DS18b20 sensors on 1-Wire net -----------------------------------


//-------------------- Print DS18b20 sensors temp to console -----------------------------------

// function to print the temperature for a device
String printTemperature(DeviceAddress deviceAddress)
{
 
  float tempC = sensors.getTempC(deviceAddress);
 
          char tempF[6]; // buffer for temp incl. decimal point & possible minus sign
          dtostrf(tempC, 6, 2, tempF); // Min. 6 chars wide incl. decimal point, 2 digits right of decimal

 return tempF;
  //Serial.print("Temp C: ");
 
}

// function to print a device address
String printAddress(DeviceAddress deviceAddress)
{
  String tmpadr;
  for (uint8_t i = 0; i < 8; i++)
    {
      if (deviceAddress[i] < 16) tmpadr = tmpadr + ("0");
       
       tmpadr = tmpadr + String(deviceAddress[i], HEX);
    }
    return tmpadr;
}
//-------------------- END Print DS18b20 sensor temp to console -----------------------------------


//--------------------- Send data to serial port -----------------------------------------
void sendData(String var,int varno, String val)
{
   
Serial.print(var);
Serial.print(varno);
Serial.print("~");
Serial.println(val);
 
 
}
//--------------------- END Send data to serial port -----------------------------------------


//----------------- Show SYSTEM time --------------------------------
void showSystemTime()
{
 
  Serial.print("Current time for Node ");
  Serial.print(BOARD_ID);
  Serial.print (" : ");
  Serial.println(newtime);
  Serial.println("-----------------------------");
  
  Serial.print("Seconds since midnight : ");
  Serial.println(DS1307Timer);
  
 }
//----------------- END Show SYSTEM time --------------------------------

//----------------- Set SYSTEM time --------------------------------
 
void setSoftRTCTime(String tmpDateTime){
 unsigned int tmpyear=stringToInt(tmpDateTime.substring(0,4));
 unsigned int tmpmonth=stringToInt(tmpDateTime.substring(5,7));
 unsigned int tmpday=stringToInt(tmpDateTime.substring(8,10));
 unsigned int tmphour=stringToInt(tmpDateTime.substring(11,13));
 unsigned int tmpminute=stringToInt(tmpDateTime.substring(14,16));
 unsigned int tmpsecond=stringToInt(tmpDateTime.substring(17,19));
 
  // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
 RTC.adjust(DateTime(tmpyear, tmpmonth, tmpday, tmphour, tmpminute, tmpsecond));

 
 char buf[11];
 sprintf(buf, "%02d-%02d-%02d %02d:%02d:%02d", tmpyear, tmpmonth, tmpday, tmphour, tmpminute, tmpsecond);
  
 Serial.print("Time for Node : ");
 Serial.print(BOARD_ID);
 Serial.print(" set to : ");
 Serial.println(buf);
 Serial.println();

}
//----------------- END Set SYSTEM time --------------------------------

//----------------------------- convert Time String to seconds --------------------------
unsigned long timeTosec(String tmptime)
{
// time in form HH:MM:SS
unsigned long result;
unsigned long tmpHour = stringToLong(tmptime.substring(0,2)) * 3600;
unsigned long tmpMin = stringToLong(tmptime.substring(3,5)) * 60;
unsigned long tmpSec = stringToLong(tmptime.substring(6,8));

result = tmpHour + tmpMin + tmpSec;
return result;
}
//------------------------- END timeTosec -------------------------------------

String secTotime(unsigned long tmptime)
{
String timesStr;
int tmpHour = (int)(tmptime/3600);
int tmpMin = (int)(tmptime - tmpHour*3600)/60;
int tmpSec = (int)(tmptime - tmpHour*3600 - tmpMin*60);
String Hour;
String Min;
String Sec;

if (tmpHour<10)
{
   Hour = "0" + String(tmpHour);
}
else
{
  Hour = String(tmpHour);
}

if (tmpMin<10)
{
   Min = "0" + String(tmpMin);
}
else
{
  Min = String(tmpMin);
}

if (tmpSec<10)
{
   Sec = "0" + String(tmpSec);
}
else
{
  Sec = String(tmpSec);
}


timesStr = Hour + ":" + Min + ":" + Sec;
return timesStr;
}
//--------------------------- End secToTime --------------------------------------

unsigned long stringToLong(String string){
  
  char char_string[string.length()+1];
  string.toCharArray(char_string, string.length()+1);
  
  return atol(char_string);
}
//--------------------------- END stringToLong -------------------------------------

//--------------------------  convert arduino String to integer ----------------------------

unsigned int stringToInt(String string){
  
  char char_string[string.length()+1];
  string.toCharArray(char_string, string.length()+1);
  
  return atoi(char_string);
}
//-------------------------- END stringToint  -------------------------------

//--------------------------------------------------------------------------



//---------------- read humidity sensors -----------------------------------
/*void Read_DHT11()
{
String StringToSend;

for (int i=1; i<numberOfDHT11_sensors+1; i++)// 1 to number of humidity devices 
 {
 // READ DATA
int DHT_pin=43; 

  Serial.print("DHT11, \t");
 int chk = DHT.read11(DHT_pin+i);//start pin 44
  switch (chk)
  {
    case DHTLIB_OK:  
		Serial.print("OK,\t"); 
		break;
    case DHTLIB_ERROR_CHECKSUM: 
		Serial.print("Checksum error,\t"); 
		break;
    case DHTLIB_ERROR_TIMEOUT: 
		Serial.print("Time out error,\t"); 
		break;
    default: 
		Serial.print("Unknown error,\t"); 
		break;
  }
 // DISPLAY DATA
  Serial.print(DHT.humidity,1);
  Serial.print(",\t");
  Serial.println(DHT.temperature,1);
  
            char DHT_buf[9];
  sfpf(DHT_buf, "%02d!%02d", DHT.humidity,DHT.temperature);
   
  
StringToSend = StringToSend + DHT_buf + "!" + i +"*";
 // The sensor can only be read from every 1-2s, and requires a minimum
  // 2s warm-up after power-on.
  delay(2000);
  
}
 //send data to  
sendData("H~",BOARD_NO,String(numberOfDHT11_sensors) + "~" + StringToSend);
 
}
//---------------- END read humidity sensors -----------------------------------
*/


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
  //#########################################################
}

String Read_soilSensors(int soil_sensorPin)
{
  int sensorValue;
 // power the sensor
  digitalWrite(soil_sensorVCC, HIGH);
  delay(100); //make sure the sensor is powered
  // read the value from the sensor:
  sensorValue = analogRead(soil_sensorPin); 
  //stop power 
  digitalWrite(soil_sensorVCC, LOW);  
  //wait
  delay(100);          
  Serial.print("sensor = " );                       
  Serial.println(sensorValue);
  return String(sensorValue);
}

 //////////////////////// INTERRUPT ROUTINES /////////////////////////////

void tempTimerIntRoutine()
{
// Update TempTimer_interval
TempTimer_interval ++;
  if(TempTimer_interval  == TempTimer_interval_Set) {
    TempTimer = true;
    TempTimer_interval  = 0;  
  }
}

void init_avr_timer1(uint16_t t1count)
{
  // initialize Timer1
  cli();          // disable global interrupts
  TCCR1A = 0;     // set entire TCCR1A register to 0
  TCCR1B = 0;     // same for TCCR1B
  // set compare match register to desired timer count:
  OCR1A = t1count;
  // turn on CTC mode:
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler:
  TCCR1B |= (1 << CS10);
  TCCR1B |= (1 << CS12);
  // enable timer compare interrupt:
  TIMSK1 |= (1 << OCIE1A);
  // enable global interrupts:
  sei();
}


//////////////////////////////////////////////////////////////////////////////


