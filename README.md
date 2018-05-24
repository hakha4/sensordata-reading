# sensordata-reading
Read sensordata from serial port and broadcast on TCP
Python kurs 2018
Håkan Hallberg

Projekt idea : read different kind of sensordata from serial COM and broadcast in realtime over TCP port, save data for later use and plot data in realtime

Use with an Arduino (or any microcontroller with serial port).

Incoming data formatted to select different sensors :

- 'T' = temperature sensor (eg. Dallas 18b20) in format T!ROM-adress!temp.data
- 'H' = humidity (ToDo)
- etc.
For testing program:

1) Download 'pythontest.ino' to any Arduino. Dallas temp. sensor connected to pin 4 as default.
2) run main.py file:
    - In menu at start select correct COM-port and Baudrate (115200 as default)

   Program at current state a frame to build on and will be developed further in the future




