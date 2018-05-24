# sensordata-reading

This project was developed as part of a course in Python

and is to be considered as a newbie project according to coding style and elegance in programming in Python


Projekt idea : read different kind of sensordata from serial COM and broadcast in realtime over TCP port, save data for later use and plot data in realtime

Use with an Arduino (or any microcontroller with serial port).

Incoming data formatted to select different sensors :

- 'T' = temperature sensor (eg. Dallas 18b20) in format T!ROM-adress!temp.data
- 'H' = humidity (ToDo)
- etc.

For testing program:

1) Download 'pythontest.ino' to any Arduino. Dallas temp. sensor connected to pin 4 as default.
    There are numerious example how to connect the tempsensor to an Arduino. Google if unsure howto!

2) run main.py file:

    - In menu at start select correct COM-port and Baudrate (115200 as default)

   Program at current state a frame to build on but may be developed further in the future




