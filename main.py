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
import sys
import serial
import time

# Define var/const
menu_actions  = {}  # global values for Menu routines
app_title = "*** R E A D  S E N S O R D A T A ***"
runMode = False # keeps Main running in infinite loop, False until settings OK
global BAUD
BAUD = 0 # default baudrate = 19200, set in Menu
global COM_port
COM_port = 'NOT SET' # serial port



# =======================
#     MENY FUNCTIONS
# =======================

# Main menu
def main_menu():

    print("************************************")
    print (app_title)
    print("************************************\n")
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







    retval = input("Select COM-port  >>")
    if retval == "":
        print("-----------------")
        print(" Invalid option !")
        print("-----------------")
        exec_menu('1') # Try again


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




    retval = input("Select Baudrate from list above  >> ")
    if int(retval) < 1 or int(retval) > 5:
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

# ============================
#     DATA HANDLING FUNCTIONS
# ===========================

# get path to script for saving textfile
def get_app_path():
    txtFilePath = os.path.dirname(os.path.realpath(sys.argv[0]))
    return  txtFilePath + "\datalog"

# Get date-time to save with data
def get_timestamp():
    return datetime.datetime.now()


# Parse sensordata from serialport
def parse_data(tmpdata):
# ToDo
    pass





# Plot incoming serial data
def plot_data():
# ToDo
    pass

# Save serial sensordata for later use
def save_data_toFile():
# ToDo
    pass
    a = open('test.txt', 'w')
    a.write('theunixdisaster\t 05')
    a.close()


# =======================
#      MAIN PROGRAM
# =======================


def main():
    while runMode: # run main over and over. Check for better options
         read_serial()


main_menu()


if __name__ == '__main__': main()

