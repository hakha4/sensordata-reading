# This program reads sensordata from an Arduino or other microcontroller from serial port and :
# - save data for later use
# - plots data in realtime
# - broadcast data on TCP
# This program was made as part of a Phd course in Python programming.



#title           :main.py
#description     :This program reads sensordata from microcontroller and save / displays data
#author          :Håkan Hallberg
#date            :2018-05-24
#version         : 1.0
#usage           :python main.py
#notes           : needs connected microcontroller (Arduino) connected on serial port
#python_version  :3.6.4
#=======================================================================

# Import   modules needed
import os
import selectz
import socket
import sys
import serial
import time
import errno
from datetime import date
#import numpy as np
import matplotlib as plt
from drawnow import *
from array import array



# Define var/const
menu_actions  = {}  # global values for Menu routines
app_title = "*** R E A D  S E N S O R D A T A ***"
runMode = False # keeps Main running in infinite loop, False until settings OK
global BAUD
BAUD = 0 # default baudrate = 19200, set in Menu
global COM_port
COM_port = 'NOT SET' # serial port
global DEBUG # for check during development
DEBUG = True
plt.ion() #Plot live data
global cnt
cnt=0 # counter in plot function
temp_c = [] # holds serial data to plot

PORT = 20000 # TCP
HOST = ''
sel = selectz.Selector()# TCP
tcp_mode = False


# =======================
#     TCP options
# =======================
retval = input("Do You want to connect to TCP ? Y/N  >>")
if retval == 'Y' or retval == 'y':
    tcp_mode = True
print("==================================================================================================")
print("Open Putty or any terminal and set IP to 'localhost' if on the same machine as Python program")
print("or set a valid IP-adress")
print("select port 20000 and 'Telnet'")
print("MAKE SURE TO OPEN PUTTY OR TERMINAL BEFORE PROCEEDING !")
print("==================================================================================================")


# =======================
#     MENY FUNCTIONS
# =======================

# Main menu
def main_menu():
    global runMode

    print("************************************")
    print (app_title)
    print("************************************\n")
    print()
    print("To get the program to work, sensor controller must be connected and\nCOM-port and Baudrate MUST be set to proper values !\n")
    print ("Select option:")
    print ("1. Set COM-port")
    print ("2. Set Baudrate")
    print ("\n0. Quit Menu\n")

    if COM_port == 'NOT SET':
        print("COM port must be set before proceeding")
    else:
        print("COM port SET OK to " + COM_port)

    if BAUD == 0:
        print("Baudrate must be set before proceeding")
    else:
        print("Baudrate SET OK to " + str(BAUD))

    if COM_port != 'NOT SET' and BAUD != 0:
        # Exit Menu and Run
        global runMode
        runMode = True
        main()
        return





    choice = input(" >>  ")
    exec_menu(choice)

    return

# Execute menu
def exec_menu(choice):
    #os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Menu 1 - set COM-port
def menu1():
    # list port(s)
    d = serial_ports()
    no_ports = len(d)
    for key in d:
      print(key + "  " + str(d[key]) +"\n")


    if no_ports == 1:
        str_no_ports =  " ([ 1 ])"
    elif no_ports > 1:
        str_no_ports = " ([ 1 to " + str(no_ports) + " ])"
    else:
        # no ports avaliable - quit menu
        print("No port avaliable")
        exec_menu(0)


    retval = input("Select COM-port (E = Exit)  >>")
    if retval == "":
        print("-----------------")
        print(" Invalid option !")
        print("-----------------")
        exec_menu('1') # Try again
    elif retval == 'E' or retval == 'e':
        menu_actions['main_menu']()


    elif int(retval) < 1 or int(retval) > no_ports:
        print("-----------------")
        print(" Invalid option !")
        print("-----------------")
        exec_menu('1') # Try again

    else: # Valid option for port, set COM


        print()
        # save COM_port
        set_com(list(d.keys())[list(d.values()).index(int(retval))])

        if BAUD == 0:
             exec_menu('2') # Go to baudrate settings
        else:
             back() # return to Main Menu



    return


# Menu 2 - set Baudrate
def menu2():
    # define baudrate's
    baud_options = {9600:1,19200:2,38400:3,57600:4,115200:5}

    # list baudrate's
    d = baud_options

    for key in d:
      print(str(key) + "  " + str(d[key])+"\n")


    print()




    retval = input("Select Baudrate from list above (E=Exit) >> ")

    if retval == 'E' or retval == 'e':

        menu_actions['main_menu']()
    elif int(retval) < 1 or int(retval) > 5:
        print("Invalid Baudrate !")
        print("-----------------")

    else:
        set_baud(list(d.keys())[list(d.values()).index(int(retval))])
        back() # return to Main Menu

    return

# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit Meny
def exit():
    exit


# Menu definition's
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': exit,
}

# =======================
#     SERIAL FUNCTIONS
# =======================

# Find avaliable ports
def serial_ports():
    x = 0
    print("Scanning for avaliable port(s) ....")

    print()
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = {}
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            x = x + 1
            result[port]=x

        except (OSError, serial.SerialException):
            pass


    return(result)


# Set COM port
def set_com(com):
    global  COM_port
    COM_port = com
    print("COM-port set to: " + COM_port +'\n')

# Set Baudrate
def set_baud(baud):
    global  BAUD
    BAUD = baud
    print("Baudrate set to: " + str(BAUD) +'\n')





# Connect and Read from serial port
def read_serial():
    try:
        ser = serial.Serial(COM_port, BAUD)
    except (OSError, serial.SerialException):
         sys.exit("failed to open port: " + COM_port)

         return



    while True:

            # sent using Serial.println() on the Arduino
            reading = ser.readline().decode('utf-8')

            print(reading)
            parse_data(reading)

# ============================
#     DATA HANDLING FUNCTIONS
# ===========================


# Parse sensordata from serialport
def parse_data(tmpdata):
     # check first char to see what kind of sensor
    if tmpdata[0] == "#" and tmpdata[1] == "T":
        eval_temp(tmpdata)
    #elif tmpdata[0] == "#" and tmpdata[1] == "H" ==> Humidity ToDo

# Put temperature data in variables for later processing
def eval_temp(tempdata):

    '''#####################################################################################################################################
    Data is in format : #T_x_y_31.00!0!28b3a47b030000b4
    #T means temperature sensor
    x = id of connected Arduino, can be any number from 0 to 9
    y = number of connected temp. sensors
    31.00!0!28b3a47b030000b4 = temp. in Celcius, 0 = order of temp. sensor ( 0,1,2 .. to no. of connected), 28b3a47b030000b4 = ROM-address
     data separated by '!' and if there is more than one sensor connected they are separated by an asterix (*)
     ########################################################################################################################################'''



    d = {}  # holds sensordatastring for each sensor

    # split string to find out Arduino id, number of sensors and sensor data
    x_list = tempdata.split('_')
    arduino_id = x_list[1]
    numberof_sensors = x_list[2]
    sensor_data = x_list[3] # holds the entire sensordata string

    print("Arduino id: " + arduino_id)
    print("No. of sensor(s): " + numberof_sensors)
    print("Sensor data: " + sensor_data)

    # split sensordata for every sensor
    if int(numberof_sensors) > 1: # means we have to split by '*' first
        # create a list to store data in
        multi_list = sensor_data.split('*')
        for x in range(numberof_sensors-1): # save sensordata in a dictionary, index starts with '0' !
            d[x] = multi_list[x]
    else: # only one sensor
        d[0] = sensor_data


    # split sensordata in temperature, sensor no. and ROM-address
    for y in range (len(d)):
        tmp_str = d[y].split('!') # holds sensordata splitted in temp, sensor no and ROM-address

        temperature = tmp_str[0]
        sensor_no = tmp_str[1]
        rom_address = tmp_str[2]
        print("Temperature = " + temperature)
        print("Sensor no  = " + sensor_no)
        print("ROM address = " + rom_address)

    # save data in textfile
    save_data_tofile(temperature,sensor_no,rom_address)


    return


# get path to script for saving textfile
def get_app_path():
    txtFilePath = os.path.dirname(os.path.realpath(sys.argv[0]))
    return  txtFilePath + "\datalog"









# Save serial sensordata for later use in textfile
def save_data_tofile(var1,var2,var3):

    # ToDo fix timezone

    # get path to save to
    path_tosave = get_app_path()
    # make sure 'datalog' dir exists
    try:
        os.makedirs(path_tosave)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # add ime stamp to data
    ts = time.gmtime()
    time.strftime('%X %x %Z')


    akt_dt = time.strftime("%H:%M:%S", ts)
    # create filename from date
    filename = "Temperature_data_" + str(date.today()) + ".txt"

    try:
        with open(path_tosave + "/" + filename, 'a') as file:
            file.write(akt_dt + "," + var1 + "," + var2 + "," + var3  )

    except:
        print("Error saving to file")
        # plot temp
    plot_data(var1)

    return


# ============================
#     PLOT FUNCTIONS
# ============================
# Setup plot
def makeFig():
    plt.ylim(0, 40)  # Set y min and max values
    plt.title('Reading Sensor Data')  # Plot title
    plt.grid(True)  # Turn grid on
    plt.ylabel('Temp C')  # Set y-label
    plt.xlabel('Reading count')
    plt.plot(temp_c, 'ro-', label='C`')  # plot temperature
    plt.legend(loc='upper left')  # plot egend

    plt.autoscale()

# Plot data
def plot_data(tmp_temp):
    global cnt

    temp_c.append(tmp_temp)  # Append temp readings
    drawnow(makeFig)  # Update graph
    plt.pause(.000001)  # To keep drawnow from crashing
    cnt = cnt + 1
    if (cnt > 50):  # Show 50 pts and then erase from left
        temp_c.pop(0)
    if tcp_mode == True:
        # Convert string to byte
        s = tmp_temp + '\r'  # add CR
        b = s.encode('ascii')
        read(conn, b)


# ============================
#     TCP FUNCTIONS
# ============================
def accept(sock):
    global conn
    conn, addr = sock.accept()
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register('read', conn, read)

def read(conn,tmpstr):

    try:

     conn.send(tmpstr)  # Hope it won't block
    except:
     pass

sock = socket.socket()
sock.bind(('localhost', PORT))
sock.listen(100)
sock.setblocking(False)
sel.register('read', sock, accept)

# =======================
#      MAIN PROGRAM
# =======================


def main():
    while runMode:  # run main over and over. Check for better options
        if tcp_mode == True:
            sel.select()


        read_serial()


    main_menu()




if __name__ == '__main__': main()

