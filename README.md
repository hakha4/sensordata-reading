# sensordata-reading

This project was developed as part of a course in Python

and is to be considered as a newbie project according to coding style and elegance in programming in Python


Projekt idea : read different kind of sensordata from serial COM and broadcast in realtime over TCP port, save data for later use and plot data in realtime

Use with an Arduino ( pytest.ino compiled on an Arduino Nano ver.3 but any Arduino would be ok).

Incoming data formatted to select different sensors :

- 'T' = temperature sensor (eg. Dallas 18b20) in format: 

        T~1~1~26.00!0!28b3a47b030000b4
        
        - first parameter = 'T' for temperature (sensotype)

        - second parameter = 'ID' for connected microcontroller
        
        - third parameter = number of connected sensors
        
        - fourth parameter = temperature in Celcius
        
        - fifth parameter = sensor number (index 0)
        
        - sixth parameter = unique ROM -address for every connected  Dallas sensor
        
        
        
        
- 'H' = humidity (ToDo)
- etc.

For testing program:

1) Download 'pythontest.ino' to any Arduino. Dallas temp. sensor connected to pin 4 as default.
    There are numerious example how to connect the tempsensor to an Arduino. Google if unsure howto!

2) run main.py file:
    - Decide if You want to open a tcp port for showing sensordata, read instructions on screen

    - In menu at start select correct COM-port and Baudrate (115200 as default)

   Program at current state a frame to build on but may be developed further in the future
   
   Troubleshooting:
   - ModuleNotFoundError: No module named 'selectz'
        - program depends on this, see https://github.com/pdxjohnny/selectz
   - no serial data
        - check devicemanager (windows) for correct COM-port connected to Arduino




