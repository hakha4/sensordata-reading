# sensordata-reading
Read sensordata from serial port and broadcast on TCP
Python kurs 2018
Håkan Hallberg
Projektide’ : read sensordata from serial COM and broadcast in realtime over TCP and save data for later use

P-code
Create a Class that handles serial port
-	Check for available ports
-	Open port with correct Baud etc
-	When opened check if interrupted and take action
At programstart ask user for com properties,later in ini.file?
Handle incoming data
-	Check what type of sensor: T = temp, H = humidity etc
-	Parse data to correct format for saving/sending over TCP
Create a Class that saves data for later use
-	Save with timestamp
-	Save in text or database ??
Create a TCP-server Class that accepts multiple connections
-	At programstart ask user for port to use for connections
-	Handle incoming requests for data
-	Send to connected clients as soon as new data arrives
Error handling

EXTRA ! plot incoming data
Todo:
-	Check for existing Classes that could be used as a template
-	Check what technique to use for keeping the program ‘alive’. Some kind of threading ?


